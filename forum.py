import config
import sys



def user_command(data):
    if data[0] == 'add':
        config.safe_insert_user(data[1])
    elif data[0] == 'del':
        config.safe_delete_user(data[1])
    elif data[0] == 'list':
        config.list_users(data[1])
    elif data[0] == 'set':
        config.user_set(data[1])
    elif data[0] == "available":
        config.user_available(data[1])
    elif data[0] == "unset":
        config.user_clear()
    else:
        print("Invalid user operation: {0:s}".format(data[0]))

def post_command(data):
    if data[0] == 'delete':
        config.delete_post(data[1])
    elif data[0] == 'add':
        user_set = open("user_set.txt", "r")
        theme_set = open("theme_set.txt", "r")
        config.insert_post(user_set.read(),theme_set.read(), data[1])
        theme_set.close()
        user_set.close()
    elif data[0] == 'list':
        config.posts_list(data[1])
    else:
        print("Invalid user operation: {0:s}".format(data[0]))
    


def theme_command(data):
    if data[0] == "list":
        config.theme_list(data[1])
    elif data[0] == "set":
        config.theme_set(data[1])
    elif data[0] == 'add':
        config.theme_set(data[1])
        user_set = open("user_set.txt", "r")
        theme_set = open("theme_set.txt", "r")
        config.safe_insert_post(user_set.read(), theme_set.read(), data[2])
        theme_set.close()
        user_set.close()
    elif data[0] == 'delete':
        user_set = open("user_set.txt", "r")
        config.delete_theme(data[1], user_set.read())
    elif data[0] == 'top':
        config.top_theme()
    else:
        print("Invalid user operation: {0:s}".format(data[0]))
   
DBFILE = './_db/forum.sqlite'

config.create_db_connection(DBFILE)

if len(sys.argv) > 1:
    command = sys.argv[1]

    if command == "user":
            user_command(sys.argv[2:4])
    elif command == "post":
        post_command(sys.argv[2:])
    elif command == "theme":
        theme_command(sys.argv[2:])
    else:
        print("Invalid command")
else:
     print ("Give some arguments")