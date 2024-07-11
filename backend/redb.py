import os
from pathlib import Path
import subprocess
import time

if __name__ == "__main__":
    db_name = "./sql_app.db"
    while os.access(db_name, 1):
        
        try:
            os.remove(db_name)
        except:
            print("删除失败, 等待下次重试")
            pass
        
        time.sleep(0.4)
 
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
    
    from iceslog import initial_data
    initial_data.init()