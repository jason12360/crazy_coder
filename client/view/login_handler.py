#导入MD5加密模块
import hashlib
import sys
#导入正则表达式模块
import re
# 导入自定义异常模块
from view_exception import *
# 这是一个控制器类,用来控制视图的IO响应


class Login_handler:
    def __init__(self, page):
        self.page = page

    def bind(self,comment_handler,client):
        self.comment_handler = comment_handler
        self.client = client
    # 定义当登录子界面登录按钮被触发时执行的事件

    def do_login(self):
        username = self.page.login_view.e1.get()
        password = self.page.login_view.e2.get()
        password2 = password
        # 检测用户名
        try:
            self.islegal(username, password,password2)
            password = self.encode(password)
            command = "login+"+username+'+'+password+"+@end"
            response = self.comment_handler(command,self.client)
            if response == 'Y':
                self.page.close()
            else:
                raise UsrnameOrPasswdNotExistException()

        except UsrnameOrPasswdBlankException:
            self.page.login_view.show_error_message('用户名或密码不能为空')
        except UsrnameOrPasswdNotExistException:
            self.page.login_view.show_error_message('用户名或密码不存在')
        except UsrnameNotMeetRequirements:
            self.page.login_view.show_error_message('用户名必须为英文字母开头\n长度必须为8到16位\n不能包含除数字字母下划线以外的其他字符')
        except PasswdNotMeetRequirements:
            self.page.login_view.show_error_message('密码长度必须为8到16位\n不能包含除数字字母下划线以外的其他字符')
    # 定义当登录子界面注册按钮被触发时执行的事件

    def login_do_register(self):
        self.page.close_login_view()
        self.page.create_register_view()

    def register_do_register(self):
        username = self.page.register_view.e1.get()
        password = self.page.register_view.e2.get()
        password2= self.page.register_view.e3.get()
        # 检测用户名
        try:
            self.islegal(username, password,password2)
            password = self.encode(password)
            command='reg+'+username+'+'+password+'+@end'
            response = self.comment_handler(command,self.client)
            if response == 'Y':
                self.page.close()
            else:
                raise UsrnameOrPasswdAlreadyExistException()

        except UsrnameOrPasswdBlankException:
            self.page.register_view.show_error_message('用户名或密码不能为空')
        except UsrnameOrPasswdAlreadyExistException:
            self.page.register_view.show_error_message('用户名已被注册,请重新输入')
        except UsrnameNotMeetRequirements:
            self.page.register_view.show_error_message('用户名必须为英文字母开头\n长度必须为8到16位\n不能包含除数字字母下划线以外的其他字符')
        except PasswdNotMeetRequirements:
            self.page.register_view.show_error_message('密码长度必须为8到16位\n不能包含除数字字母下划线以外的其他字符')
        except ConfirmedPasswdNotMatch:
            self.page.register_view.show_error_message('确认密码与密码不吻合')
    def do_cancel(self):
        
        command = 'quit+ + +@end'
        self.comment_handler(command,self.client)
        self.page.close()
        sys.exit()

    def islegal(self, username, password,password2):
        '''
        这个方法用来判断用户名是否符合规定
        规定:用户名和密码不为空
                用户名必须是由字母或数字或下划线组成
        '''
        if (not username) or (not password):
            raise UsrnameOrPasswdBlankException()
        if not re.findall(r'^[a-zA-Z]\w{7,15}$',username):
            raise UsrnameNotMeetRequirements()
        if not re.findall(r'^\w{8,16}$',password):
            raise PasswdNotMeetRequirements()
        if password2 != password:
            raise ConfirmedPasswdNotMatch()

    #加密使用md5协议
    def encode(self,password):
        obj = hashlib.md5()
        obj.update(password.encode())
        return obj.hexdigest()

