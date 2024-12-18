import os
import sys
from collections import defaultdict
from pprint import pprint


class Walker:
    def __init__(self, path):
        self.path = path
        self.root = os.path.basename(path)
        self.dirs_to_ignore = [
            '.git',
            '__pycache__',
            'build',
            'dist',
            '.idea',
            '.vscode',
            '.pytest_cache',
            '.mypy_cache',
            '.ipynb_checkpoints',
            '.DS_Store'
        ]

        self.dirs_suffices_to_ignore = (
            '.egg-info',
            '.egg',
            '.dist-info'
        )

        self.files_extensions_to_ignore = (
            '.pyc',
            '.pyo',
            '.pyd',
            '.egg-info',
            '.xlsx',
            '.csv',
            '.txt',
            '.log',
            '.ini',
            '.json',
            '.docx',
            '.pdf',
            '.doc',
            '.md'
        )

    def walk(self, path=None, root=None):
        project_hierarchy = dict()
        if path is None:
            path = self.path

        if root is None:
            root = self.root

        dirs = [
            dir_name
            for dir_name in os.listdir(path)
            if (os.path.isdir(os.path.join(path, dir_name))
                and dir_name not in self.dirs_to_ignore)
            and not dir_name.endswith(self.dirs_suffices_to_ignore)
        ]

        files = [
            file_name
            for file_name in os.listdir(path)
            if os.path.isfile(os.path.join(path, file_name)) and not file_name.endswith(self.files_extensions_to_ignore)
            ]

        project_hierarchy['files'] = files

        if len(dirs) > 0:
            i = 0
            while i < len(dirs):
                selected_dir = dirs[i]
                project_hierarchy[selected_dir] = self.walk(os.path.join(path, selected_dir), selected_dir)
                i += 1

        if root is self.root:
            project_hierarchy = {root: project_hierarchy}

        return project_hierarchy

