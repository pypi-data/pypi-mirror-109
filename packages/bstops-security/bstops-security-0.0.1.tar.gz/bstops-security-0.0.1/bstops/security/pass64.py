#!/usr/bin/env python

"""
加解密功能
"""

from bstops.tool import Base64

base64 = Base64()
base64.table = 'DswBaG0R1T=JIj/FkybzrqMOWHSeCNp9nYlZhEQgx53f+7Uuo8PVcLvdiA46Kt2m'
base64.padding = 'X'


def pass_encode(user, pwd, split='の'):
    """
    :param user(str): user
    :param pwd(str): password
    :return: key(str)
    """
    string = f'{user}{split}{pwd}'
    key = base64.encode(string)
    return key.strip()


def pass_decode(key, split='の'):
    """
    :param key(str): 
    :return: user(str), pwd(str)
    """
    string = base64.decode(key)
    user, pwd = string.split(split)
    return user, pwd
