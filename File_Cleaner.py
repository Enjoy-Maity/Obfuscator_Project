import os
import re
from tkinter import messagebox


class File_cleaner:
    def __init__(self, file_path, destination_path):
        self.file_path: str = file_path
        self.destination_path: str = destination_path
        self.file_lines_start_with_comment_pattern = re.compile(
            r'\A\s*#'
        )
        self.docstring_pattern = re.compile(
            r'\A\s*\"{3}|\A\s*\'{3}|[\w\s]*\'{3}\Z|[\w\s]*\"{3}'
        )
        self.file_lines: list = []
        self.indices_to_remove: list = []

    def file_checks(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError

        except FileNotFoundError:
            messagebox.showerror(title="Error!! File not found!!!",
                                 message=f"{os.path.basename(self.file_path)} not found\
                                            in the given folder path \
                                            {os.path.basename(os.path.dirname(self.file_path))}")

    def remove_docstrings(self):
        i = 0
        while i < len(self.file_lines):
            if re.search(self.docstring_pattern, str(self.file_lines[i])):
                self.indices_to_remove.append(i)
                j = 0
                while j < len(self.file_lines[i+1:]):
                    if re.search(self.docstring_pattern, str(self.file_lines[i+j])):
                        self.indices_to_remove.append(i+j)
                        j += 1
            i += 1

    def clean_file(self):
        with open(self.file_path, 'r') as file:
            self.file_lines = file.readlines()

        i = 0
        while i < len(self.file_lines):
            if len(str(self.file_lines[i]).strip()) == 0:
                self.indices_to_remove.append(i)

            elif re.search(self.file_lines_start_with_comment_pattern, str(self.file_lines[i])):
                self.indices_to_remove.append(i)

            i += 1

        self.remove_docstrings()
