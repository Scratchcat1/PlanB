import subprocess
import os
import shlex

def add_share(share_name, directory_path, comment, acls, guest_ok = "n"):
    #acls - tuple in form (username,permission) where permission is "F","R" or "D"
    # print("sudo net usershare add %s \"%s\" \"%s\" %s guest_ok=%s" % (share_name, directory_path, comment, acls, guest_ok))
    process = subprocess.Popen( shlex.split("sudo net usershare add %s \"%s\" \"%s\" %s guest_ok=%s" % (share_name, directory_path, comment, acls, guest_ok)))
    output, error = process.communicate()

def remove_share(share_name):
    process = subprocess.Popen( shlex.split("sudo net usershare delete %s" % (share_name,)))
    output, error = process.communicate()
    
def mount_share(server_identifier, share_name, mount_directory, username, password):
    if not os.path.exists(mount_directory):
        os.makedirs(mount_directory)
    process = subprocess.Popen( shlex.split("sudo mount -r -t cifs -o username=%s,password=%s //%s/%s %s" % (username, password, server_identifier, share_name, mount_directory)))
    output, error = process.communicate()

def unmount_share(mount_directory):
    process = subprocess.Popen( shlex.split("sudo umount -f -l %s" % (mount_directory,)))
    output, error = process.communicate()

def mount_all_shares(config):
    mounted_shares = {}

    for share_name in config.get_share_names():
        share_dir = os.path.join("temp_mnt", share_name)
        mount_share(config.get_samba_server_identifier(), share_name, share_dir, "BLANK", "BLANK")

        if os.path.ismount(share_dir):
            mounted_shares[share_name] = share_dir

    return mounted_shares

def unmount_all_shares(config):
    for share_name in config.get_share_names():
        share_dir = os.path.join("/mnt", "temp", share_name)
        unmount_share(share_dir)

    

def netshare_acls_to_tuple(netshare_acls):
    #Converts netshare acls -> "Everyone:R,Cat:F" to tuple storage format [("Everyone","R"),("Cat","F")]
    tuple_acls = []

    for netshare_acl in netshare_acls.split(","):
        username, permission = netshare_acl.split(":")
        tuple_acls.append((username, permission))

    return tuple_acls

def tuple_acls_to_netshare(tuple_acls):
    #Converts tuple storage format acls [("Everyone","R"),("Cat","F")] to netshare acls -> "Everyone:R,Cat:F"
    netshare_acls = ""

    for tuple_acl in tuple_acls:
        if netshare_acls != "":
            netshare_acls += ","
        netshare_acls += tuple_acl[0] + ":" + tuple_acl[1]

    return netshare_acls
