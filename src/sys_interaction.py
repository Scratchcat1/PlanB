import subprocess
import os
import shutil
import shlex
import checksumdir
import defaults
import utils

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
    process = subprocess.Popen( shlex.split("sudo useradd %s" % (username,)), stderr = subprocess.PIPE)
    utils.check_exception(process.communicate()[1])

    print("Attempting to set password for %s" % (username,))
    process = subprocess.Popen( shlex.split(" sudo smbpasswd -a %s" % (username,)), stdin = subprocess.PIPE, stderr = subprocess.PIPE)
    utils.check_exception(process.communicate((password+"\n"+password).encode()))

def remove_user(username):
    print("Removing user %s" % (username,))
    process = subprocess.Popen(shlex.split("sudo userdel %s" % (username,)), stderr = subprocess.PIPE)
    utils.check_exception(process.communicate()[1])


def rsync_directories(source, target):
    process = subprocess.Popen(shlex.split("rsync -vz --delete --info=progress2 %s %s" % (source, target)), stderr = subprocess.PIPE)
    utils.check_exception(process.communicate()[1])
    
def clone_directory(source_dir, target_dir):
    rsync_directories(source_dir, target_dir)
    if defaults.VALIDATE_RSYNC_ENABLED:
        validate_checksums(source_dir, target_dir)

def validate_checksums(source_dir, target_dir):
    source_dir_hash = checksumdir.dirhash(source_dir)
    target_dir_hash = checksumdir.dirhash(target_dir)
    if source_dir_hash != target_dir_hash:
        raise Exception("Directory hash mismatch from source %s to target %s Hashes: Source: %s Target: %s" % (source_dir, target_dir, source_dir_hash, target_dir_hash))