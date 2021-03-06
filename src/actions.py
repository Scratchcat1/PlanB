import configuration_store
import sys_interaction
import samba_cfg
import os
import defaults

def reset(config):
    config = configuration_store.Configuration_Store()

#####

def add_user(config, username, password, add_private_share, master_password):
    sys_interaction.add_user(username, password)
    config.add_user(username, password, master_password)

    if add_private_share:
        directory = os.path.join(config.get_private_share_directory(), username)
        share_name = username + "_private_share"
        comment = username + "s private share"
        acls = username + ":f"
        add_share(config, share_name, directory, comment, acls, "n")

def remove_user(config, username, delete_private_share):
    sys_interaction.remove_user(username)
    config.remove_user(username)            #Remove the user

    share_name = username + " private share"
    remove_share(config, share_name, delete_private_share)


def add_share(config, share_name, directory, comment, acls, guest_ok = "n"):
    sys_interaction.create_directory(directory)
    samba_cfg.add_share(share_name, directory, comment , acls)
    config.add_share(share_name, directory, comment, acls)

def remove_share(config, share_name, delete_share_folder):
    samba_cfg.remove_share(share_name)
    share = config.remove_share(share_name)
    if delete_share_folder:    #If I should delete the share folder
        sys_interaction.delete_directory(share["directory"])
    

def add_backup_location(config, location_name, directory):
    sys_interaction.create_directory(directory)
    config.add_backup_location(location_name, directory)

def remove_backup_location(config, name):
    config.remove_backup_locations(name)

#####

def set_private_share_directory(config, directory):
    config.set_private_share_directory(directory)

def load_configuration(config, filename):
    config.load_configuration(filename)

def save_configuration(config, filename):
    config.save_configuration(filename)

#########

def run_backup(config, master_password):
    # Rsync all shares to each backup destination available. Ignore shares/destinations which cannot be mounted.
    failed_shares = samba_cfg.mount_all_shares(config, master_password)
    backup_locations_used = []

    for backup_location_name in config.get_backup_location_names():
        backup_directory = config.get_backup_location(backup_location_name)["directory"]

        if os.path.exists(backup_directory):
            backup_locations_used.append(backup_location_name)
            for share_name in filter(lambda share_name : share_name not in failed_shares, config.get_share_names()):
                
                print("Copying from %s to %s" % (share_name, backup_location_name))
                source_dir = samba_cfg.get_mount_point(share_name)
                sys_interaction.clone_directory(source_dir, backup_directory)
    
    samba_cfg.unmount_all_shares(config)
    return backup_locations_used, failed_shares

                