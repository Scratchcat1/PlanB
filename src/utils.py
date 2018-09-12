def check_exception(error):
    if error:
        raise Exception(error)

def find_permission_user(acl, min_permission):
    users = acl.split(",")

    for user in users:
        username, permission = user.split(":")
        if min_permission == "f" and permission in ["f"]:
            return username
        elif min_permission == "r" and permission in ["r", "f"]:
            return username
    