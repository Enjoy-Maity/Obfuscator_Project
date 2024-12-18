import os
import sys
from Project_Walker import Walker
from Database_reader_and_writer import DataBase_Handler
from pprint import pprint


class Import_checker_and_data_maker:
    def __init__(self, path, project_name=None):
        self.path = path
        self.root = os.path.basename(path)

        if project_name is None:
            self.project_name = os.path.basename(path)

        else:
            self.project_name = project_name

        self.database_handler = DataBase_Handler(self.project_name)
        self.project_file_hierarchy = {}
        self.venv_folder = ""

        self.project_hierarchy()

    def project_hierarchy(self):
        walker = Walker(self.path)
        self.project_file_hierarchy = walker.walk()

    def import_database_maker(self):
        pass

    def data_maker(self):
        pass

    @staticmethod
    def scripts_folder_finder(path) -> bool:
        result = False
        if "Scripts" in os.listdir(path):
            files_and_folders = os.listdir(
                os.path.join(path, "Scripts")
            )
            if any(file_.endswith(".exe") and
                   file_.startswith("python")
                   for file_ in files_and_folders):
                result = True

        return result

    def venv_finder(self):
        dirs = list(
            self.project_file_hierarchy[self.root].keys()
        )

        venv_found = False
        # Finding the venv folder in the project folders
        i = 0
        while i < len(dirs):
            selected_dir = str(dirs[i])
            list_of_folders = [dir_ for dir_ in os.listdir(
                os.path.join(self.path, selected_dir)
            ) if os.path.isdir(os.path.join(self.path, selected_dir, dir_))]

            if len(list_of_folders) > 0:
                j = 0
                while j < len(list_of_folders):
                    neo_selected_dir = os.path.join(selected_dir, list_of_folders[j])
                    venv_found = self.scripts_folder_finder(os.path.join(self.path, neo_selected_dir))
                    if venv_found:
                        self.venv_folder = os.path.join(self.path, selected_dir)
                        break
                    j += 1
                if venv_found:
                    break
            i += 1

        if not venv_found:
            pass


Import_checker_and_data_maker(r"C:\CLI_Automation\Main_application").venv_finder()
