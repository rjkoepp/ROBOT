import string

def get_user(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user

def get_message(line):
    separate = line.split(":", 2)
    print separate
    if(len(separate) < 3):
        return "".join(separate)
    message = separate[2]
    return message
