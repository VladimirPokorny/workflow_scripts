import os
import sys
import shutil


working_dir = os.getcwd()
project_name = input('Enter project name: ')

if project_name == '':
    print('Project name cannot be empty')
    exit()

project_path = os.path.join(working_dir, project_name)

try:
    os.makedirs(project_path, exist_ok=True)
except FileNotFoundError:
    print('Invalid project name or path')
    exit()

os.chdir(project_path)

os.system('python -m venv .venv')

with open('requirements.txt', 'w') as file:
    file.write('')

with open('README.md', 'w') as file:
    file.write(f'# {project_name}')

source_gitignore_dir = os.path.join(os.path.dirname(sys.argv[0]), 'source_gitignore')
print(source_gitignore_dir)

print(source_gitignore_dir)

shutil.copy(source_gitignore_dir, '.gitignore')

os.system('git init')
os.system('git add .')
os.system('git commit -m "Initial commit"')

os.system('code .')

print(f'Project **{project_name}** created successfully!')
