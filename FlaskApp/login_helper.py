def login_check(username, password):
    users = {
        "fmars": "aaaa",
        "mumu": "lalala",
    }
    if username in users:
        if users[username] == password:
            return True
    return False
