import os
from pathlib import Path
import subprocess

if __name__ == "__main__":
    try:
        os.remove("./sql_app.db")
    except:
        pass
 
    # 要删除文件的目录
    directory = 'iceslog/alembic/versions'
    
    # 列出目录下所有文件和文件夹
    files_and_folders = os.listdir(directory)
    
    # 过滤出所有.txt文件
    txt_files = [file for file in files_and_folders if file.endswith('.py')]
    
    # 删除每一个.txt文件
    for txt_file in txt_files:
        file_path = os.path.join(directory, txt_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    file_path = Path(__file__).parent.joinpath('iceslog')
    print(file_path)
    ret = subprocess.run("alembic revision --autogenerate -m bypy")
    ret = subprocess.run("alembic upgrade head")