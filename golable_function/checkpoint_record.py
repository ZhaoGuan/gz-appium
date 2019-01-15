# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import sqlite3
import os
import time
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
try:
    os.PATH.exists(PATH + '/../checkpoint_record_data') == False
    os.mkdir(PATH + '/../checkpoint_record_data' % PATH)
except:
    pass


def create_table(table_name):
    conn = sqlite3.connect(PATH + '/../checkpoint_record_data/checkpoint_record_data.db')
    print("Opened database successfully")
    try:
        # id 展示用日期view_date,比较用时间戳date,图片pic,初始比较值Initial_pic_comparison，上次图比较值last_pic_comparison
        c = conn.cursor()
        c.execute(
            'create table %s ('
            'id integer primary key autoincrement,'
            'view_date text,'
            'date integer,'
            'pic text,'
            'Initial_pic_comparison integer,'
            'last_pic_comparison integer)' % table_name)
        conn.commit()
        conn.close()
        print('create')
        return table_name
    except Exception as e:
        print(e)


def insert_table(table_name, view_date, date, pic, initial_pic, last_pic):
    conn = sqlite3.connect(PATH + '/../checkpoint_record_data/checkpoint_record_data.db')
    print("Opened database successfully")
    instert_c = conn.cursor()
    instert_c.execute(
        "INSERT INTO %s (view_date, date , pic,Initial_pic_comparison,last_pic_comparison) VALUES (?,?,?,?,?)" %
        table_name, (view_date, date, pic, initial_pic, last_pic))
    conn.commit()
    conn.close()


def query_initial_last(table_name):
    conn = sqlite3.connect(PATH + '/../checkpoint_record_data/checkpoint_record_data.db' )
    print("Opened database successfully")
    c = conn.cursor()
    i_pic = c.execute('SELECT pic FROM %s WHERE id=1' % table_name)
    i_pic_location = i_pic.fetchone()[0]
    l_pic = c.execute('SELECT pic FROM %s WHERE id=(SELECT max(id) FROM %s)' % (table_name, table_name))
    l_pic_location = l_pic.fetchone()[0]
    print(l_pic_location)
    conn.commit()
    conn.close()
    return {'Initial': i_pic_location, 'last': l_pic_location}


def query_the_fist(table_name):
    conn = sqlite3.connect(PATH + '/../checkpoint_record_data/checkpoint_record_data.db')
    print("Opened database successfully")
    c = conn.cursor()
    no = c.execute('SELECT max(id) FROM %s' % table_name).fetchone()[0]
    print(type(no))
    if no == None:
        return False
    else:
        return True


if __name__ == "__main__":
    # create_table('text')
    insert_table('test', time.strftime('%Y%m%d%H%M%S', time.localtime()), '2', 'gsas', 'NULL', '5')
    # query_Initial_last('text')
