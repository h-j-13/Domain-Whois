#!/usr/bin/python
#encoding:utf-8

#
# 添加或更新域名记录
# @author wangkai 
# 

import static
import whois_connect
from random import choice
import datetime
import whois_info_deal


_DB = static.main_DB # 数据库操作对象
_server_addr = static.server_addr # server_addr服务器地址 获取对象
_func_name = static.func_name # func_name 获取对象

# 增加新的域名记录
# @param do_an 域名分析对象
# @return 域名whois信息字典
def add_record(do_an):
    global _DB
    domain_whois = whois_info_get(do_an)
    if domain_whois:
        domain_whois["insert_time"] = str(datetime.datetime.now()).split(".")[0]
        _DB.db_insert(**domain_whois) # 新的数据插入 
        return domain_whois
    else:
        return

# 更新域名记录
# @param do_an 域名分析对象
# @return 域名whois信息字典
def update_record(do_an):
    global _DB
    domain_whois = whois_info_get(do_an)
    if domain_whois:
        domain_whois["insert_time"] = str(datetime.datetime.now()).split(".")[0]
        _DB.db_update(**domain_whois) # 数据库数据更新
        return domain_whois
    else:
        return
        
# whois信息获取及处理
# @param do_an 域名分析对象
# @return 域名whois信息字典
def whois_info_get(do_an):

    global _server_addr, _func_name

    domain_punycode = do_an.get_punycode_domain()
    tld = do_an.get_tld() # 域名后缀
    server_addr = _server_addr.get_server_addr('.' + tld) # 获取whois服务器地址
    # 没有该后缀信息
    if not server_addr:
        return 'error info: not have whois_server info'
    func_name = _func_name.get_func_name(server_addr) # 获取处理函数名称
    
    # 该顶级域名处理尚未完成
    if not func_name:
        domain_whois = {"domain": domain_punycode,            # 域名
                        "flag": -5,                           # 表示该域名提取函数尚未完成
                        "domain_status": "",                  # 域名状态
                        "sponsoring_registrar": "",           # 注册商
                        "top_whois_server": "",               # 顶级域名服务器
                        "sec_whois_server": "",               # 二级域名服务器
                        "reg_name": "",                       # 注册姓名
                        "reg_phone": "",                      # 注册电话
                        "reg_email": "",                      # 注册email
                        "org_name": "",                       # 注册公司名称
                        "creation_date": "",                  # 创建时间
                        "expiration_date": "",                # 到期时间
                        "updated_date": "",                   # 更新时间
                        "insert_time": "",                    # 信息插入时间
                        "details": "",                        # 细节
                        "hash_value": 0,                      # 哈希值
        }
        return domain_whois

    recv_whois_info = whois_connect.get_recv_info.get_recv_info(domain_punycode, server_addr)
    domain_whois = whois_info_deal.info_deal.get_result(domain_punycode, server_addr, func_name, recv_whois_info)
    return domain_whois

# 根据域名状态判断域名是否注册
# @param domain_status 域名状态值
# @return true or false
def is_exist(domain_status):
    return False if domain_status == '29' else True
        
        

