
class PostgresRouter(object):
    """A router that sets up a simple master/slave configuration"""

    def db_for_read(self, model, **hints):
        return 'postgresql'

    def db_for_write(self, model, **hints):
        return 'postgresql'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        "Explicitly put all models on all databases."
        return True

