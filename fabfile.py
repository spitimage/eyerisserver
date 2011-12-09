
# globals
from fabric.api import env, require, local, sudo, run, put, cd, settings

# environments

def set_env():
    "Use the local virtual server"
#    env.hosts = ['twins']
    env.user = 'ubuntu'
    env.password = 'password'
    env.home = '/mnt/projects'
    env.projname = 'eyerisserver'
    env.projpath = '%(home)s/%(projname)s' % env
    env.datadir = '/mnt/data'
    env.ebs = 'none' != 'none'
    # Postgresql version
    env.pg_ver = '9.1'

    # FYI this controls the failure behavior
    env.warn_only = False

    # You can also do this for temporary failure handling:
    with settings(warn_only=True):
        pass

def create_fs():
    if env.ebs:
        sudo('mkfs -t ext3 /dev/xvdc')

def mount_data():
    if env.ebs:
        sudo('mkdir -p %(datadir)s' % env)
        # Do it this way so it mounts on reboot too
        sudo('echo /dev/xvdc %(datadir)s ext3 defaults >> /etc/fstab' % env)
        sudo('mount -a')

    # Make sure the home directory exists
    sudo('mkdir -p %(home)s' % env)
    sudo('chown -R %(user)s:%(user)s %(home)s' % env)

    # Add www-data user to ubuntu group
    sudo('addgroup www-data ubuntu')

    # Allows logging from anyone
    sudo('chmod g+w %(home)s' % env)

def do_updates():
    # Because M2Crypto is currently broken, install the fixed version sitewide (from debian guys)
    # Here we are importing a new debian repo (adding the public key for it first)
    sudo('gpg --keyserver pgpkeys.mit.edu --recv-key  AED4B06F473041FA')
    sudo('gpg -a --export AED4B06F473041FA | sudo apt-key add -')
    sudo('echo deb http://ftp.us.debian.org/debian sid main >> /etc/apt/sources.list')

    sudo('apt-get -y update')
    sudo('apt-get -y upgrade')

def install_db():
    sudo('apt-get -y install postgresql-%(pg_ver)s' % env)
    sudo('apt-get -y install postgresql-contrib-%(pg_ver)s' % env)
    sudo('apt-get -y install postgresql-%(pg_ver)s-postgis' % env)
    sudo('apt-get -y install libgdal1-1.7.0')

    stop_db()

    # Replace config files with our settings
    put('pg_hba.conf', '/etc/postgresql/%(pg_ver)s/main/pg_hba.conf' % env, use_sudo=True)
    put('postgresql.conf', '/etc/postgresql/%(pg_ver)s/main/postgresql.conf' % env, use_sudo=True)

    # Postgresql driver
    sudo('apt-get -y install python-dev')
    sudo('apt-get -y install libpq-dev')


def create_db():
    sudo('mkdir -p %(datadir)s' % env)
    sudo('chown postgres:postgres %(datadir)s' % env)
    pg('/usr/lib/postgresql/%(pg_ver)s/bin/initdb -D %(datadir)s' % env)
    pg('cp /var/lib/postgresql/%(pg_ver)s/main/server.crt %(datadir)s' % env)
    pg('cp /var/lib/postgresql/%(pg_ver)s/main/server.key %(datadir)s' % env)

    start_db()

    change_db_password('postgres', 'password')
    pg('createuser -d -R -S django')
    change_db_password('django', 'password')

    # Create the PostGIS template database
    put('create_template_postgis-1.5.sh', '/tmp')
    with cd('/tmp'):
        pg('sh create_template_postgis-1.5.sh')

def create_db_project():
    pg('createdb -T template_postgis -O django %(projname)s' % env)


def install_web():
    sudo('apt-get -y install nginx')
    sudo('apt-get -y install python-virtualenv')
    # swig is needed for M2Crypto
    sudo('apt-get -y install swig')

    # Because M2Crypto is currently broken, install the fixed version sitewide (from debian guys)
    sudo('apt-get -y install python-m2crypto=0.21.1-2')

    # Unzip is a handy thing to have
    sudo('apt-get -y install unzip')

    # Remove default nginx site
    sudo('rm -f /etc/nginx/sites-enabled/default')

def create_domain():
    create_fs()
    mount_data()
    do_updates()
    install_db()
    create_db()
    create_db_project()
    install_web()
    create_web_project()

def create_domain_local():
    sudo('mkdir -p %(datadir)s' % env)
    sudo('mkdir -p %(home)s' % env)
    sudo('chown -R %(user)s:%(user)s %(home)s' % env)
    sudo('addgroup www-data ubuntu')
    sudo('chmod g+w %(home)s' % env)
    do_updates()
    install_db()
    create_db()
    create_db_project()
    install_web()
    create_web_project()

def create_web_project():
    '''
    Sets up the environment and directory structure for a project
    '''
    require('projpath', provided_by=[set_env])

    run('mkdir -p %(projpath)s/env' % env)
    run('mkdir -p %(projpath)s/media' % env)
    run('mkdir -p %(projpath)s/static' % env)

    put('upstart', '/etc/init/%(projname)s.conf' % env, use_sudo=True)
    put('nginx', '/etc/nginx/sites-available/%(projname)s' % env, use_sudo=True)
    put('requirements.txt', '%(projpath)s/env' % env)

    with cd('%(projpath)s/env' % env):
        run('virtualenv .')
        run('bin/pip -E . install -r requirements.txt')

    sudo('ln -sf /etc/nginx/sites-available/%(projname)s /etc/nginx/sites-enabled' % env)

    deploy_web_project()

    with cd('%(projpath)s/releases/current/%(projname)s' % env):
        wd('sh prep.sh')

def migrate():
    with cd('%(projpath)s/releases/current/%(projname)s' % env):
        wd('sh migrate.sh')

def deploy_web_project():
    """
    Deploy the latest version of the site to the servers
    """
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')

    upload_tar_from_git()
    symlink_current_release()
    restart_webserver()

    with cd('%(projpath)s/releases/current/%(projname)s' % env):
        run('chmod ug+x ./manage.py')

def upload_tar_from_git():
    require('release', provided_by=[deploy_web_project])
    require('projpath', provided_by=[set_env])
    "Create an archive from the current Git master branch and upload it"
    local('git archive --format=tar master | gzip > %(release)s.tar.gz' % env)
    run('mkdir -p %(projpath)s/releases/%(release)s/%(projname)s' % env)
    run('mkdir -p %(projpath)s/packages' % env)
    put('%(release)s.tar.gz' % env, '%(projpath)s/packages' % env)
    with cd('%(projpath)s/releases/%(release)s/%(projname)s' % env):
        run('tar zxf ../../../packages/%(release)s.tar.gz' % env)
        run('chmod u+x gunicorn.sh')
    local('rm %(release)s.tar.gz' % env)


def symlink_current_release():
    with cd('%(projpath)s/releases' % env):
        run('rm -f current')
        run('ln -sf %(release)s current' % env)

def restart_webserver():
    with settings(warn_only=True):
        sudo('service %(projname)s stop' % env)
        sudo('service %(projname)s start' % env)
    sudo('service nginx restart')

# Runs commands as lesser privileged user
def wd(cmd):
    return sudo(cmd, user='www-data')

# Runs commands as postres user
def pg(cmd):
    return sudo(cmd, user='postgres')


def change_db_password(user, pw):
    cmd = 'psql postgres -c "ALTER USER %s WITH PASSWORD \'%s\';"' % (user, pw)
    pg(cmd)


def stop_db():
    sudo('service postgresql stop')

def start_db():
    sudo('service postgresql start')

