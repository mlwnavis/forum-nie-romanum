"""
Test program for forum database interaction
"""

import re

import sqlite3
import sys

global conn
global cur






def create_db_connection(dbfile):
    """
    Creates database connection and apropriate cursor

    Initializes global variables conn and cur
    """
    global conn
    conn = sqlite3.connect(dbfile)
    global cur
    cur = conn.cursor()

def is_safe_username(name):
    """
    Checks user name for consistency with forum requirements
    """
    mch = re.match('^[A-Za-z][A-Za-z0-9]{4,9}$', name)
    return mch != None

def user_id(name):
    """
    Returns user id associated with given user name or
    None if user with given name not defined
    """
    urow = cur.execute("SELECT `userid` FROM `users` WHERE `name`=?", (name,))
    uids = urow.fetchone()
    if uids is None:
        return None
    else:
        return uids[0]


    
# odczytywanie danych z plików


def theme_set(theme):
    theme_set = open("theme_set.txt", "w")
    theme_set.write(theme)
    theme_set.close()

def theme_get():
    theme_get = open("theme_set.txt", "r")
    theme_get.read()
    theme_get.close()

def theme_clear():
    theme_clear = open("theme_set.txt", "w")
    theme_clear.close()

def user_set(user):
    user_set = open("user_set.txt", "w")
    user_set.write(user)
    user_set.close()
    
def user_get():
    user_get = open("user_set.txt", "r")


def user_clear():
    user_clear = open("user_set.txt", "w")
    user_clead.close()

#operacje na postach

def insert_post(user, theme, text):
    userid = user_id(user)
    time = str(datetime.now())
    cur.execute("INSERT INTO `posts` (`userid`,`theme`,`text`,`time`) VALUES (?, ?, ?, ?)",
        (userid, theme, text, time))
    conn.commit()
    rowid = cur.execute("SELECT last_insert_rowid() AS rowid")
    return rowid.fetchone()

def safe_insert_post(user, theme, text):
    if is_safe_username(user):
        uid = user_id(user)
        
        if uid is None:
            print("You must be logged user to add posts.")
        else:
            insert_post(uid, theme, sanificate_post(text))
    else:
        print("Invalid username")

def delete_post(postid):
    cur.execute("DELETE FROM `posts` WHERE `postid`=?" ,(postid,))
    conn.commit()

def posts_list(theme):
    uids = posts_list_db(theme)
    cnt = 0
    for x in uids:
        cnt += 1
        print("%d. %s"%(cnt, x[0]))

def posts_list_db(theme):
    list = cur.execute("SELECT `text` FROM `posts` WHERE `theme`=?", (theme,))
    uids = list.fetchall()
    return uids

def post_show(pattern):
    theme = open("theme_set.txt", "r")
    cur.execute("SELECT FROM `posts` WHERE `theme`=? AND `text` LIKE ?", (theme, pattern))
    conn.commit()
    theme.close()

#operacje na użytkownikach

def insert_user(name):
    """
    Inserts user into database. Returns new user id
    """
    cur.execute("INSERT INTO `users` (`name`) VALUES (?)", (name,))
    conn.commit()
    return user_id(name)

def safe_insert_user(user):
    if is_safe_username(user):
        uid = user_id(user)
        if uid is None:
            return insert_user(user)
        else:
            print('User name "{0:s}" not available'.format(user))
            return None
    else:
        print('Invalid user name "{0:s}"'.format(user))
        return None

def safe_delete_user(user):
    if is_safe_username(user):
        uid = user_id(user)
        if uid is None:
            print('User "{0:s}" not found')
        else:
            cur.execute("DELETE FROM `posts` WHERE `userid`=?", (uid,))
            conn.commit()
            cur.execute("DELETE FROM `users` WHERE `userid`=?", (uid,))
            conn.commit()

def list_users(namepart):
    data = cur.execute("SELECT `name` FROM `users` WHERE `name` LIKE ?", (namepart,))
    if data is None:
        print('"No user name match "{0:s}"'.format(namepart))
    else:
        print("Users:")
        for row in data:
            print(row[0])

def user_available(user):
    if is_safe_username(user):
        uid = user_id(user)
        if uid is None:
            print('User name "{0:s}" is available'.format(user))
            return None
        else:
            print('User name "{0:s}" not available'.format(user))
            return None
    else:
        print('User name "{0:s}" not available'.format(user))
        return None
#operacje na tematach

def delete_theme(theme, user):
    userid = user_id(user)
    cur.execute("DELETE FROM `posts` WHERE `theme`=? AND `userid`=?" ,(theme, userid))
    conn.commit()

def theme_list(pattern):
    list = cur.execute("SELECT DISTINCT `theme` FROM `posts` WHERE `theme` LIKE ?", (pattern,))
    post = list.fetchone()
    while not post is None:
        if post is None:
            return None
        else:
            print(post[0])
            post = list.fetchone()


def top_theme():
    topp = top_theme_db()
    cnt = 0
    for x in topp:
        cnt += 1
        print("%d. %s"%(cnt, x[0]))
    d = top_theme_choice()
    theme_set(topp[int(d)-1][0])
    
def top_theme_db():
    top = cur.execute("SELECT DISTINCT `theme` FROM `posts` ORDER BY `postid` DESC LIMIT 6")
    topp = top.fetchall()
    return topp
    
def top_theme_choice():
    choice = input("Select theme to activate, select 0 to leave: ")
    while choice not in ["0", "1", "2", "3", "4", "5", "6"]:
        print ("Invalid command")
        top_theme_choice()
    else:
        if choice == "0":
            pass
        else:
            return choice