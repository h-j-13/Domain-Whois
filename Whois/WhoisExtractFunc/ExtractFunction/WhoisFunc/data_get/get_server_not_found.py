# !usr/bin/python
# encoding:utf-8

# 获取whois服务器查找不到的标志信息
# @version 
#

import shelve
import static


class ServerNotFound:

    def __init__(self):
       shelve_file = shelve.open(static.path_shelv_file, 'r')
       self.server_not_found_dict = shelve_file['server_not_found_dict']
       shelve_file.close()
       
    def get_server_not_found_sign(whois_server):
        return self.server_not_found_dict.get(whois_server, None)


if '__name__' == '__main__':
    pass