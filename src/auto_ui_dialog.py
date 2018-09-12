import auto_ui
import configuration_store
import actions
import defaults

class App:
    def __init__(self, render):
        self._render = render
        self._config = configuration_store.Configuration_Store() 
        
    def create_menu(self, title, menu_options, descriptions = []):
        form = auto_ui.UI_Form()
        form.set_title(title)
        
        for description in descriptions:
            form.add_description(description)
        for i, menu_option in enumerate(menu_options):
            form.add_description(str(i) + "." + menu_option)

##        get_option_func = lambda number : menu_options[int(number)]    
        form.add_query("option", "Enter menu option number", int)
        return form

    def main_menu_dialog(self):
        form = self.create_menu("Main menu", [
                                               "Users",
                                               "Shares",
                                               "Backup location",
                                               "Set default share name",
                                               "Load configuration",
                                               "Save configuration",
                                               "Run backup"
                                            ])
        self._render.run(form)
        results = self._render.get_results()
        
        if results["option"] == 0:
            self.users_menu_dialog()
        elif results["option"] == 1:
            self.shares_menu_dialog()
        elif results["option"] == 2:
            self.backup_locations_menu_dialog()
        elif results["option"] == 3:
            self.set_private_share_directory()
        elif results["option"] == 4:
            self.load_configuration_dialog()
        elif results["option"] == 5:
            self.save_configuration_dialog()
        elif results["option"] == 6:
            self.run_backup_dialog()

    def users_menu_dialog(self):
        form = self.create_menu("Users", [
            "Add user",
            "View users",
            "Remove user",
            ])

        self._render.run(form)
        results = self._render.get_results()
        
        if results["option"] == 0:
            self.add_user_dialog()
        elif results["option"] == 1:
            self.view_users_dialog()
        elif results["option"] == 2:
            self.remove_user_dialog()
        

    def shares_menu_dialog(self):
        form = self.create_menu("Shares", [
            "Add share",
            "View shares",
            "Remove share",
            ])

        self._render.run(form)
        results = self._render.get_results()
        
        if results["option"] == 0:
            self.add_share_dialog()
        elif results["option"] == 1:
            self.view_shares_dialog()
        elif results["option"] == 2:
            self.remove_share_dialog()
        

    def backup_locations_menu_dialog(self):
        form = self.create_menu("Backup locations", [
            "Add location",
            "View backup location",
            "Remove location",
            ])

        self._render.run(form)
        results = self._render.get_results()
        
        if results["option"] == 0:
            self.add_backup_location_dialog()
        if results["option"] == 1:
            self.view_backup_locations_dialog()
        elif results["option"] == 2:
            self.remove_backup_location_dialog()

    def add_user_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Add a user")
        form.add_query("username", "Enter username")
        form.add_query("password", "Enter password")
        form.add_query("private_share", "Add private share (Y/N)?", lambda choice:choice.upper() == "Y")
        form.add_query("master_password", "Enter the master password")
        
        self._render.run(form)
        results = self._render.get_results()
        
        actions.add_user(
            self._config,
            results["username"],
            results["password"],
            results["private_share"],
            results["master_password"])

    def view_users_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("View users")
        form.add_query("master_password", "Enter master password to view passwords, else press enter", default_value = "")

        self._render.run(form)
        results = self._render.get_results()

        form = auto_ui.UI_Form()
        form.add_description("Use 'sudo pdbedit -L -v' in terminal to list all active samba accounts")
        for username in self._config.get_usernames():
            user = self._config.get_user(username, results["master_password"])
            form.add_description(username + ": " + str(user))
            
        self._render.run(form)

    def remove_user_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Remove a user")
        form.add_query("username", "Enter username")
        form.add_query("delete_private_share", "Delete the private share folder of the user (Y/N)?", lambda choice:choice.upper() == "Y")

        self._render.run(form)
        results = self._render.get_results()
        
        actions.remove_user(
            self._config,
            results["username"],
            results["delete_private_share"])
        
    def add_share_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Add a share")
        form.add_query("share_name", "Share name")
        form.add_query("share_dir", "Share directory")
        form.add_query("share_comment", "Share Comment")
        form.add_query("acl", "Share access control list(ACL)")
        form.add_query("guest_access", "Guest access (Y/N)", lambda value: value.lower())

        self._render.run(form)
        results = self._render.get_results()
        
        actions.add_share(
            self._config,
            results["share_name"],
            results["share_dir"],
            results["share_comment"],
            results["acl"],
            results["guest_access"])


    def view_shares_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("View shares")
        form.add_description("To view all shares recognised by samba run 'sudo net usershare info' in terminal")
        
        for share_name in self._config.get_share_names():
            form.add_description(share_name + ": " + str(self._config.get_share(share_name)))

        self._render.run(form)
        self._render.get_results()

    def remove_share_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Delete share")
        form.add_query("share_name", "Share name")
        form.add_query("delete_share_folder", "Delete the share folder (Y/N)?", lambda choice:choice.upper() == "Y")

        self._render.run(form)
        results = self._render.get_results()
        
        actions.remove_share(
            self._config,
            results["share_name"],
            results["delete_share_folder"])

    def add_backup_location_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Add backup location")
        form.add_query("location_name", "Name of backup location")
        form.add_query("directory", "Backup directory")

        self._render.run(form)
        results = self._render.get_results()
        
        actions.add_backup_location(
            self._config,
            results["location_name"],
            results["directory"])

    def view_backup_locations_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("View backup locations")

        for backup_location_name in self._config.get_backup_location_names():
            form.add_description(backup_location_name + ": " + str(self._config.get_backup_location(backup_location_name)))
        
        self._render.run(form)

    def remove_backup_location_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Remove backup location")
        form.add_query("location_name", "Name of backup location")

        self._render.run(form)
        results = self._render.get_results()
        
        actions.remove_backup_location(
            self._config,
            results["location_name"])


    ######

    def set_private_share_directory(self):
        form = auto_ui.UI_Form()
        form.set_title("Set default share directory")
        form.add_query("directory", "Directory")

        self._render.run(form)
        results = self._render.get_results()
        
        actions.set_private_share_directory(
            self._config,
            results["directory"])

    def load_configuration_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Load configuration")
        form.add_query("file_path", "File path of config", default_value = defaults.CONFIG_DEFAULT_FILEPATH)

        self._render.run(form)
        results = self._render.get_results()

        actions.load_configuration(
            self._config,
            results["file_path"])

    def save_configuration_dialog(self):
        form = auto_ui.UI_Form()
        form.set_title("Save configuration")
        form.add_query("file_path", "File path of config", default_value = defaults.CONFIG_DEFAULT_FILEPATH)

        self._render.run(form)
        results = self._render.get_results()

        actions.save_configuration(
            self._config,
            results["file_path"])        

    ######

    def run_backup_dialog(self):
        errors = actions.run_backup(self._config)

        form = auto_ui.UI_Form()
        form.set_title("Backup complete")
        for dirs, error in errors.values():
            form.add_description("Error from source %s to target %s. Error: %s" % (dirs[0], dirs[1], error))

        self._render.run(form)



