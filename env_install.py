import os
pip_list = ['Django','CherryPy','openpyxl','xlrd','pymysql','pythoncom','pywin32']
for one in pip_list:
    cmds = 'pip install ' + one
    print(cmds)
    req = os.system(cmds)
    print(req)
    print('#'*50)