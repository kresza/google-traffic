import mysql.connector

class Database:
    def __init__(self, db_user, db_password, db_name, db_host, db_port):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.connection = None

    def connect_to_database(self):
        self.connection = mysql.connector.connect(
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            database=self.db_name,
            port=self.db_port
        )

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
