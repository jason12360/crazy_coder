import os
import time


class File(object):
    def __init__(self, filename='', filesize=0, server_path='', file_last_mtime='', file_create_time=''):
        self.filename = filename
        self.filesize = filesize
        self.server_path = server_path
        self.file_last_mtime = file_last_mtime
        self.file_create_time = file_create_time

    def create_file(self, file_path):
        self.filename = os.path.split(file_path)[-1]
        self.filesize = os.path.getsize(file_path)
        self.filelocal_path = os.path.split(file_path)[0]
        self.filetype = None
        self.usrid = None

    def get_info(self):
        return (self.filename, self.filesize, self.file_last_mtime, self.file_create_time, self.server_path)

    def get_info_for_pack(self):
        return (self.filename, str(self.filesize), self.file_last_mtime, self.file_create_time, self.server_path)

    def get_name(self):
        return self.filename

    def get_size(self):
        return self.filesize

    def get_local_path(self):
        return self.filelocal_path

    def get_type(self):
        pass

    def get_usrid(self):
        pass

    def set_server_path(self, serverPath):
        self.server_path = serverPath

    def get_server_path(self):
        return self.server_path
# 关于时间的格式规定:
# 直接加入数据库的字符串yyyy-mm-dd hh:mm:ss

    def set_last_mtime(self, last_mtime):
        self.file_last_mtime = last_mtime

    def get_last_mtime(self):
        return self.file_last_mtime

    def set_file_create_time(self, create_time):
        self.file_create_time = create_time

    def get_creat_time(self):
        return self.file_create_time

    def pack(self):
        result = ','.join(list(self.get_info_for_pack()))
        result = '['+result+']'
        return result
    def unpack(self,string):
        self.filename, \
        self.filesize, \
        self.file_last_mtime,\
        self.file_create_time,\
        self.server_path= string[1:-1].split(',')
    	


# 以下代码用于测试
def main():
    import time
    f = File()
    f.create_file('./file.py')
    f.set_last_mtime('2108-01-01 07:22:22')
    f.set_file_create_time('2108-01-01 07:22:22')
    f.set_server_path('')
    print(f.pack())
    f1 = File()
    f1.unpack(f.pack())
    print(f1.pack())


if __name__ == '__main__':
    main()
