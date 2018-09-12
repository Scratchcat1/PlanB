import subprocess
import os
import shlex
import defaults
import utils

def add_share(share_name, directory_path, comment, acls, guest_ok = "n"):
    #acls - tuple in form (username,permission) where permission is "F","R" or "D"
    # print("sudo net usershare add %s \"%s\" \"%s\" %s guest_ok=%s" % (share_name, directory_path, comment, acls, guest_ok))
    process = subprocess.Popen( shlex.split("sudo net usershare add %s \"%s\" \"%s\" %s guest_ok=%s" % (share_name, directory_path, comment, acls, guest_ok)))
    utils.check_exception(process.communicate()[1])

def remove_share(share_name):
    process = subprocess.Popen( shlex.split("sudo net usershare delete %s" % (share_name,)))
    utils.check_exception(process.communicate()[1])
    
def mount_share(server_identifier, share_name, mount_directory, username, password):
    if not os.path.exists(mount_directory):
        os.makedirs(mount_directory)
    process = subprocess.Popen( shlex.split("sudo mount -r -t cifs -o username=%s,password=%s //%s/%s %s" % (username, password, server_identifier, share_name, mount_directory)))
    utils.check_exception(process.communicate()[1])

def unmount_share(mount_directory):
    process = subprocess.Popen( shlex.split("sudo umount -f -l %s" % (mount_directory,)))
    utils.check_exception(process.communicate()[1])

def mount_all_shares(config):
    mounted_shares = {}
    for share_name in config.get_share_names():
        share_dir = os.path.join(defaults.MOUNT_POINT_PATH, share_name)
        mount_share(config.get_samba_server_identifier(), share_name, share_dir, "BLANK", "BLANK")

        if os.path.ismount(share_dir):
            mounted_shares[share_name] = share_dir

    return mounted_shares

def unmount_all_shares(config):
    for share_name in config.get_share_names():
        share_dir = os.path.join(defaults.MOUNT_POINT_PATH, share_name)
        unmount_share(share_dir)
