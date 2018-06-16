# 这是一个用来负责和数据库连接，并处理和数据库相关的函数

import pymysql
import re
if __name__=='__main__':
    from file import File
    from file_folder import Filefolder
else:
    from model.file import File
    from model.file_folder import Filefolder



class My_Mysql:
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "123456",
                                  "crazy_coder", charset="utf8")
        self.cursor = self.db.cursor()

    def close(self):

        self.cursor.close()
        self.db.close()

# 用户表——————————————————————————————————————————
    def create_user_table(self):
        self.cursor.execute(
            'create table user(id int primary key auto_increment,username char(20) unique,password char(30))default charset=utf8;')
        self.db.commit()
    # 增加用户

    def add_user(self, username, password):
        sql = 'insert into user(username,password) values("%s","%s");' % (
            username, password)
        self.cursor.execute(sql)
        self.db.commit()

    # 查询用户
    def select_user(self, username):
        sql = 'select * from user where username = "%s"' % (username)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
# 用户查询表———————————————————————————————————————

    def create_userlog_table(self):
        self.cursor.execute('create table userlog(id int primary key auto_increment,\
                                                  user_id int,\
                                                  file_id int,\
                                                  log_time datetime,\
                                                  operation enum("upload","download"),\
                                                  foreign key(user_id) references user(id) \
                                                  on delete cascade \
                                                  on update cascade,\
                                                  foreign key(file_id) references file(id)\
                                                  on delete cascade\
                                                  on update cascade)default charset=utf8;')
    # 增加用户查询条目

    def add_userlog(self, user_log):
        sql = 'insert into userlog(user_id,file_id,operation,log_time) values(%d,%d,"%s",%d);' % user_log
        self.cursor.execute(sql)
        self.db.commit()

    # 查询用户查询条目
    def select_userlog(self):
        sql = '	select user.username,file.filename,userlog.operation,userlog.log_time from userlog \
				inner join user on userlog.user_id = user.id\
				inner join file on userlog.file_id = file.id'
        self.cursor.execute(sql)
        return self.cursor.fetchall()
# 文件表——————————————————————————————————————————

    def create_file_table(self):
        self.cursor.execute(
            'create table file(id int primary key auto_increment,\
                               filename char(50),\
                               filesize int,\
                               file_path_on_server char(50),\
                               last_modified_time datetime,\
                               first_create_time datetime)default charset=utf8;')

    def add_file(self, file):
        sql = 'insert into file(filename,filesize,file_path_on_server,\
                                last_modified_time,first_create_time)\
                                 values("%s",%d,"%s","%s","%s");' % file.get_info()
        self.cursor.execute(sql)
        self.db.commit()
    #程序刚开始时读取全部文件信息,返回文件夹
    def select_all_files(self):
        sql = 'select * from file'
        self.cursor.execute(sql)
        file_folder = Filefolder()
        while True:
            _ = self.cursor.fetchone()
            if not _:
                break
            file_info =(_[1],_[2],_[3],_[4].strftime('%Y-%m-%d %H:%M:%S'),_[5].strftime('%Y-%m-%d %H:%M:%S'))
            file = File(*file_info)
            file_folder.add_file(file)
        return file_folder
#在数据库通过id查找相关文件返回file
    def select_file_by_id(self, id):
        sql = 'select * from file where id = %d' % id
        self.cursor.execute(sql)
        _ = self.cursor.fetchone()
        if not _:
            return None
        else:
            file_info =(_[1],_[2],_[3],_[4].strftime('%Y-%m-%d %H:%M:%S'),_[5].strftime('%Y-%m-%d %H:%M:%S'))
            file = File(*file_info)
            return file
#在数据库通过文件名查找相关文件返回file

    def select_file_by_filename(self, filename):
        sql = 'select * from file where filename = "%s"' %filename
        self.cursor.execute(sql)
        _ = self.cursor.fetchone()
        if not _:
            return None
        else:
            file_info =(_[1],_[2],_[3],_[4].strftime('%Y-%m-%d %H:%M:%S'),_[5].strftime('%Y-%m-%d %H:%M:%S'))
            file = File(*file_info)
            return file


def main():
    my_mysql = My_Mysql()
    # my_mysql.create_user_table()
    # my_mysql.create_file_table()
    # my_mysql.create_userlog_table()
    # my_mysql.add_user('jason','12345')
    # print(my_mysql.select_user('jason'))
    # f = File()
    # f.create_file('database_handler.py')
    # f.set_last_mtime(20180101101010)
    # f.set_file_create_time(20180101101010)
    # print(f.get_info())
    # my_mysql.add_file(f)
    print(my_mysql.select_file_by_id(1).pack())
    # my_mysql.add_userlog((1,1,'upload',10200912000000))
    # print(my_mysql.select_userlog())

    my_mysql.close()


if __name__ == '__main__':
    main()
