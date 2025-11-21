import os

def combine_python_files(root_dir, output_file, excluded_dirs=None):
    if excluded_dirs is None:
        excluded_dirs = {'venv', '__pycache__', '.git', 'env', 'logs', 'alembic', '.ini', 'sb.py'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(root_dir):
            # Исключаем указанные директории
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    # Записываем комментарий с именем файла
                    outfile.write(f'\n# --- {relative_path} ---\n')
                    
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                    outfile.write('\n\n')

if __name__ == '__main__':
    project_dir = '.'  # Текущая директория (можно изменить)
    output_filename = 'combined_code.py'
    combine_python_files(project_dir, output_filename)