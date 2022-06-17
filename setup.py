import os,platform
if platform.system() == "Darwin":
    os.system('pip3 install -r requirements.txt')
elif platform.system() == "Windows":
    os.system('pip install -r requirements.txt')
elif platform.system() == 'Linux':
    os.system('pip3 install -r requirements.txt')

