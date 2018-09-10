import json
import Crypto.Cipher.AES
from Crypto.Protocol.KDF import PBKDF2
import base64_System
import os

    
        
class Configuration_Store:
    """
    Stores configuration for Plan B including shares, users and locations
    """
    def __init__(self):
        self.reset()
        
    def reset(self):
        self._default_share_directory = os.getcwd()
        self._samba_server_ip = "127.0.0.1"
        self._users = {}
        self._shares = {}
        self._backup_locations = {}

    def save_configuration(self, filename):
        configuration = {}
        configuration["default_share_directory"] = self._default_share_directory
        configuration["samba_server_ip"] = self._samba_server_ip
        configuration["users"] = self._users
        configuration["shares"] = self._shares
        configuration["backup_locations"] = self._backup_locations
        with open(filename,"w") as file_handle:
            json.dump(configuration, file_handle)

    def load_configuration(self, filename):
        try:
            with open(filename,"r") as file_handle:
                configuration = json.load(file_handle)
            self._default_share_directory = configuration["default_share_directory"]
            self._samba_server_ip = configuration["samba_server_ip"]
            self._users = configuration["users"]
            self._shares = configuration["shares"]
            self._backup_locations = configuration["backup_locations"]
        except:
            print("Unable to load file %s. Keeping current state" % (filename,))

    def get_default_share_directory(self):
        return self._default_share_directory
    def set_default_share_directory(self, directory):
        self._default_share_directory = directory
    def get_samba_server_ip(self):
        return self._samba_server_ip
    def set_samba_server_ip(self, ip):
        self._samba_server_ip = ip

    #################################
    def add_user(self, username, password, master_password):
        salt = base64_System.str_to_b64(os.urandom(16))
        iv  = base64_System.str_to_b64(os.urandom(16))  #Generate base64 salt for key derivation and iv
        
        key = PBKDF2(master_password.encode(), base64_System.b64_to_bstr(salt))

        aes_obj = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_GCM, base64_System.b64_to_bstr(iv))
        encrypted_password = base64_System.str_to_b64(aes_obj.encrypt(password.encode()))
        self._users[username] = {"password":encrypted_password, "salt":salt, "iv":iv}

    def get_user(self, username, master_password = ""):
        #Get the information about the user - if master is set
        #to "" the password will be returned in encrypted form
        if master_password != "":
            key = PBKDF2(master_password.encode(), base64_System.b64_to_bstr(self._users[username]["salt"]))
            aes_obj = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_GCM, base64_System.b64_to_bstr(self._users[username]["iv"]))
            password = aes_obj.decrypt(base64_System.b64_to_bstr(self._users[username]["password"])).decode()
        else:
            password = self._users[username]["password"]

        cloned_user = dict(self._users[username])
        cloned_user["password"] = password
        return cloned_user

    def get_usernames(self):
        return self._users.keys()

    def remove_user(self, username):
        return self._users.pop(username, None)
    #################################

    def add_share(self, share_name, directory, comment, allowed_users, guest_ok):
        self._shares[share_name] = {
            "directory":directory,
            "comment":comment,
            "allowed_users":allowed_users,
            "guest_ok":guest_ok }

    def get_share(self, share_name):
        return self._shares[share_name]

    def get_share_names(self):
        return self._shares.keys()

    def remove_share(self, share_name):
        return self._shares.pop(share_name, None)
    ################################

    def add_backup_location(self, name, directory):
        # Name stores human readable identification of directory e.g. "Plan B External Drive"
        # directory must be mounted/available already
        self._backup_locations[name]= {"directory":directory}

    def get_backup_location(self, name):
        self._backup_locations[name]

    def get_backup_location_names(self):
        return self._backup_locations.keys()

    def remove_backup_location(self, name):
        return self._backup_locations.pop(name, None)
    ################################


            
