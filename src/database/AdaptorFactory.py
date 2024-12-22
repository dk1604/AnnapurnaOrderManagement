from src.database.MySQLAdapterImpl import MySQLAdapterImpl


class AdapterFactory:

    @staticmethod
    def create_adapter(db_type, host, port, user, password, database):
        """Create the appropriate database adapter based on the database type."""
        if db_type.lower() == "mysql":
            print("\n1..............")
            return MySQLAdapterImpl(host, port, user, password, database)
        elif db_type.lower() == "postgres":
            return ValueError(f"Postgres database not supported")
        else:
            raise ValueError(f"Unsupported database type: {db_type}")