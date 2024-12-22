from src.database.MySQLAdapterImpl import MySQLAdapterImpl
from src.database.PSQLAdapterImpl import PSQLAdapterImpl


class AdapterFactory:

    @staticmethod
    def create_adapter(db_type, host, port, user, password, database):
        """Create the appropriate database adapter based on the database type."""
        if db_type == "mysql":
            print("\ncreate_adaptor called for mysql")
            return MySQLAdapterImpl(host, port, user, password, database)
        elif db_type == "postgres":
            print("\ncreate_adaptor called for psql")
            return PSQLAdapterImpl(host, port, user, password, database)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
