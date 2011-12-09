from boto.ec2.connection import EC2Connection
from boto.ec2.elb import ELBConnection
import time

securityGroups = ['ssh', 'elb', 'apache']
# This is alestic ubuntu 11.10 oneiric instance-store image (us-east region)
image = 'ami-3962a950'
instanceType = 'm1.small'
keyName = 'apache'
zone = 'us-east-1b'
# EBS volume for database (in zone b)
volumeName = 'none'

# AWS_ACCESS_KEY_ID - Your AWS Access Key ID AWS_SECRET_ACCESS_KEY - Your AWS Secret Access Key. Then you cann connect without constructor params.
conn = EC2Connection()

res = conn.run_instances(image, security_groups=securityGroups, instance_type=instanceType, key_name=keyName, placement=zone)

instance = res.instances[0]

for i in xrange(120):
    instance.update()
    if instance.state == 'running': break
    print instance.state
    time.sleep(1)

print 'Public/Private/Zone:', instance.public_dns_name, instance.private_dns_name, instance.placement

# Attach the EBS volume (it actually shows on /dev/xvdc)
if volumeName != 'none':
    ret = conn.attach_volume(volumeName, instance.id, '/dev/sdc')

# Maybe ELB will be fixed someday
if 0:
    # Associate with load balancer
    elbConn = ELBConnection()
    elb = elbConn.get_all_load_balancers()[0]
    # Make sure the appropriate availability zone is enabled
    elb.enable_zones([instance.placement])
    elb.register_instances(instance.id)

