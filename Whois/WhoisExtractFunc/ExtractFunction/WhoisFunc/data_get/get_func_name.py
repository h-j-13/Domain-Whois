# /usr/bin/python
# encoding:utf8

# 获取whois服务器对应的函数名称
# @version 1.0
# @author wangkai
# 2015.12.5

import static
import shelve

class FuncName:

    def __init__(self):
        server_function = shelve.open(static.path_shelve_file, 'r')
        self.server_function_dict = server_function['server_function_dict']
        server_function.close()

    # 获取处理函数名称
    def get_func_name(self, server_addr):
        return self.server_function_dict.get(server_addr, None)

if __name__ == '__main__':
    test = FuncName()
    print test.get_func_name('whois.crsnic.net')
        




