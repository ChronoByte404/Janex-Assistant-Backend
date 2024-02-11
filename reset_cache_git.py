import os

os.system("git rm -rf --cached .")
os.system("git add .")
os.system("python3 upload.py")