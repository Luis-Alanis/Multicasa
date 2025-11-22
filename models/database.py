from mysql.connector import pooling

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_pool()
        return cls._instance

    def _init_pool(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host="localhost",
            user="root",
            password="",
            database="casas"
        )

    def get_connection(self):
        return self.pool.get_connection()
