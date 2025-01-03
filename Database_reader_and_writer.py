import sqlite3


class DataBase_Handler:
    def __init__(self, project_name):
        self.conn = sqlite3.connect(f'obfuscator_{project_name}.db')
        self.cursor = self.conn.cursor()
        self.table_name = project_name
        self.import_table = "Import_Table"
        self.packages_table = "Packages_Table"

    def db_checker(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='?';", (self.table_name,))
        return self.cursor.fetchone() is not None

    def create_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"package_name TEXT, "
                            f"obfuscated_package_name TEXT, "
                            f"obfuscation_status TEXT, "
                            f"obfuscation_time TEXT, "
                            f"error_message TEXT);")

    def create_import_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.import_table} ("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"package_name TEXT, "
                            "method_name TEXT, "
                            "class_name TEXT, ")

    def db_writer(self, query):
        self.cursor.execute(query)

    def db_reader(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit_transaction(self):
        self.cursor.execute("COMMIT;")

    def start_transaction(self):
        self.cursor.execute("BEGIN TRANSACTION;")

    def rollback_transaction(self):
        self.cursor.execute("ROLLBACK;")

    def database_cleaner(self):
        self.cursor.execute(f"DROP obfuscator_{self.table_name}.db;")
