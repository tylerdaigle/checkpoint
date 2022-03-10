import shelve
import sys

fs = shelve.open('filesystem.fs', writeback=True)
current_dir = []

# using files_created list to separate directories from files being created
files_created = []

def install(fs):
    # Create the System and Users/username directories 
    username = input('What is your first name? ')

    fs[""] = {"System": {}, "Users": {username: {}}}
    print("Created the /Users/%s directory" % username)

def current_entries():
    """Return a dictionary representing the files in the current directory"""
    d = fs[""]
    for key in current_dir:
        d = d[key]
    return d

def ls(args):
    print('Contents of directory', "/" + "/".join(current_dir) + ':')
    for i in current_entries():
        print(i)

def cd(args):
    if len(args) != 1:
        print("Usage: cd <directory>")
        return

    # I'm keeping track of all files being created
    this_dir = "/" + "/".join(current_dir)
    for entry in files_created:
        abs_arg = this_dir + "/" + args[0]
        if entry == abs_arg:
            print("Error: %s is a file" % args[0])
            return

    if args[0] == "..":
        if len(current_dir) == 0:
            print("Cannot go above root")
        else:
            current_dir.pop()
    elif args[0] not in current_entries():
        print("Directory " + args[0] + " not found")
    else:
        current_dir.append(args[0])


def mkdir(args):
    if len(args) != 1:
        print("Usage: mkdir <directory>")
        return
    # create an empty directory there and sync back to shelve dictionary!
    d = current_entries()[args[0]] = {}
    fs.sync()

def touch(args):
    this_dir = "/" + "/".join(current_dir)
    #print("this_dir is : %s" % str(this_dir))
    if len(args) != 1:
        print("Usage: touch <filename>")
        return
    # create an empty file there and sync back to shelve dictionary!
    d = current_entries()[args[0]] = {}
    files_created.append(this_dir + "/" + args[0])
    fs.sync()

COMMANDS = {'touch' : touch, 'ls' : ls, 'cd': cd, 'mkdir': mkdir}

install(fs)

while True:
    raw = input('> ')
    if not raw:
        break
    cmd = raw.split()[0]
    if cmd in COMMANDS:
        COMMANDS[cmd](raw.split()[1:])
    #print("files_created is : %s" % str(files_created))

#Use break instead of exit, so you will get to this point.
input('Press the Enter key to shutdown...')
