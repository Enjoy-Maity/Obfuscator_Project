import ast
import os


def get_imports_from_file(file_path):
    """Extract imports and their aliases from a given Python file."""
    with open(file_path, "r") as file:
        node = ast.parse(file.read(), filename=file_path)

    imports = {}

    for item in node.body:
        if isinstance(item, ast.Import):
            for alias in item.names:
                imports[alias.name] = alias.asname if alias.asname else alias.name
        elif isinstance(item, ast.ImportFrom):
            module = item.module if item.module else ''
            for alias in item.names:
                full_name = f"{module}.{alias.name}" if module else alias.name
                imports[full_name] = alias.asname if alias.asname else alias.name

    return imports


def get_all_imports(package_path):
    """Recursively get all imports from Python files in a package or subpackage."""
    all_imports = {}

    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                file_imports = get_imports_from_file(file_path)
                all_imports[file_path] = file_imports

    return all_imports


# Example usage
if __name__ == "__main__":
    package_directory = "/home/enjoym/Projects/CLI/Main_application/"  # Replace with your package path
    imports_dict = get_all_imports(package_directory)

    # Print the dictionary of imports
    for file, imports in imports_dict.items():
        print(f"File: {file}")
        for module, alias in imports.items():
            print(f"  {module} as {alias}")
