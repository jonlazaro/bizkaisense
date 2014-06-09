from django import template

def replace(value, arg):
    s = arg.split(':')
    return value.replace(s[0], s[1])
