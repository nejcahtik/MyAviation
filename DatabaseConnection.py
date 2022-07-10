import mysql.connector
from config import config

class DatabaseConnection:

    def __init__(self):

        dbConfig = config["sql"]

        self.connection = mysql.connector.connect(
            host=dbConfig["host"],
            user=dbConfig["user"],
            password=dbConfig["password"],
            db=dbConfig["db"],
            port=dbConfig["port"]
        )

        self.cursor = self.connection.cursor(buffered=True)

    def query(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor
        except Exception as e:
            print("Failed to execute: " + str(query))
            print(e)
            raise e

    def close(self):
        self.connection.close()
