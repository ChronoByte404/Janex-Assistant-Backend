import os

os.system("git rm -rf --cached .")
os.system("git add .")

os.system("git add *")
os.system("git commit -m 'Automation'")
os.system("git push")