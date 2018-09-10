import subprocess
import os
import shutil
import shlex

def display_title():
    print("Welcome to Plan B")

def create_directory(main_directory_path, *directory_paths):
    #Creates a directory with the given directory path
    #The used directory path will be derived from the merger
    # of directory path with the contents of directory_paths
    # using os.path.join
    directory_path = os.path.join(main_directory_path, *directory_paths)
    #If the directory already exists the program will ask
    #if it should delete or ignore the folder
    create_folder = True
    if os.path.exists(directory_path):
        create_folder = input("File path %s already exists. Delete (Y) or Ignore (N)?" % (directory_path,)).upper() == "Y"
        if create_folder:
            delete_directory(directory_path)
    if create_folder:
        os.makedirs(directory_path)

def delete_directory(directory_path):
    print("Deleting directory %s" % (directory_path,))
    shutil.rmtree(directory_path)
    

def add_user(username, password):
    print("Adding user %s" % (username,))
    process = subprocess.Popen( shlex.split("sudo useradd %s" % (username,)))
    output, error = process.communicate()
    print("Attempting to set password for %s" % (username,))
    process = subprocess.Popen( shlex.split(" sudo smbpasswd -a %s" % (username,)), stdin = subprocess.PIPE)
    output, error = process.communicate((password+"\n"+password).encode())
    ### may need to add smbpasswd command instead

def remove_user(username):
    print("Removing user %s" % (username,))
    process = subprocess.Popen( shlex.split("sudo userdel %s" % (username,)))
    output, error = process.communicate()
