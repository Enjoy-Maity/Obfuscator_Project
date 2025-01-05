import sqlite3
from tkinter import messagebox


class DataBase_Handler:
    def __init__(self, project_name):
        self.conn = sqlite3.connect(f'obfuscator_{project_name}.db')
        self.cursor = self.conn.cursor()
        self.table_name = project_name
        self.import_table = "Import_Table"
        self.packages_table = "Packages_Table"
        self.modules_table = "Modules_Table"
        self.methods_table = "Methods_Table"
        self.classes_table = "Classes_Table"
        self.variables_table = "Variables_Table"
        self.create_packages_table()
        self.create_modules_table()
        self.create_import_table()

    def db_checker(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='?';", (self.table_name,))
        return self.cursor.fetchone() is not None

    def create_packages_table(self):
        try:
            self.start_transaction()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.packages_table} ("
                                f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"package_name TEXT, "
                                "package_path TEXT, "
                                "parent_package TEXT,"
                                "obfuscated_name TEXT, );")
            self.commit_transaction()
        except sqlite3.Error as e:
            messagebox.showerror(f"Error ({e.__class__.__name__})", f"Error while creating packages table: {e}")
            self.rollback_transaction()

    def create_modules_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.modules_table} ("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"module_name TEXT, "
                            "module_path TEXT, "
                            "parent_package TEXT, "
                            "package_id INTEGER, "
                            "obfuscated_module_name TEXT, "
                            "FOREIGN KEY (package_id) REFERENCES {self.packages_table}(id))")

    def create_import_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.import_table} ("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"package_name TEXT, "
                            "method_name TEXT, "
                            "class_name TEXT, ")

    def create_methods_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.methods_table} ("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"method_name TEXT, "
                            f"module_name TEXT, "
                            "parent_package TEXT, "
                            "package_name TEXT, "
                            "obfuscated_method_name TEXT, "
                            "FOREIGN KEY (package_name) REFERENCES {self.packages_table}(package_name),"
                            "FOREIGN KEY (module_name) REFERENCES {self.modules_table}(module_name))")

    def create_classes_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.classes_table} ("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"class_name TEXT, "
                            f"module_name TEXT, "
                            "parent_package TEXT, "
                            "package_name TEXT, "
                            "obfuscated_class_name TEXT, "
                            "FOREIGN KEY (package_name) REFERENCES {self.packages_table}(package_name),"
                            "FOREIGN KEY (module_name) REFERENCES {self.modules_table}(module_name))")

    def create_variables_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.variables_table} ("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"variable_name TEXT, "
                            f"class_name TEXT, "
                            "module_name TEXT, "
                            "method_name TEXT, "
                            "variable_type TEXT, "
                            "parent_package TEXT, "
                            "package_name TEXT, "
                            "obfuscated_variable_name TEXT, "
                            "FOREIGN KEY (package_name) REFERENCES {self.packages_table}(package_name),"
                            "FOREIGN KEY (module_name) REFERENCES {self.modules_table}(module_name))")

    def db_writer(self, query):
        try:
            self.start_transaction()
            self.cursor.execute(query)
            self.commit_transaction()

        except sqlite3.Error as e:
            messagebox.showerror(f"Error ({e.__class__.__name__})", f"Error while writing to database: {e}")
            self.rollback_transaction()

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
