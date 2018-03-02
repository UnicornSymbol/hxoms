#coding: utf-8

def get_quarter(dt):
    if dt.month%3 == 0:
        return dt.month/3
    else:
        return dt.month/3+1
