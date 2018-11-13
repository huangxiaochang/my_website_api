import os
import re

if __name__ == '__main__':
   os.system("..\\venv\Scripts\python3.exe manage.py runserver 0.0.0.0:8000")

# 更新数据库
# python3.exe manage.py makemigrations
# python3.exe manage.py migrate

# 使用pip freeze > ./requirements.txt  可以自动生成项目中依赖的库(在根目录下执行), 然后使用pip install -r requirements.txt就可以安装项目中的所有的依赖

# admin :  root  hxc123456

# python3.6安装MySQLdb不成功，可以使用PyMySQL来代替，python2安装MySQLdb时，可以从其他项目的虚拟环境中的Lib\site-packages中把所有的
# MYSQL,_mysql, mysql开头的文件复制到虚拟环境的相应文件夹中