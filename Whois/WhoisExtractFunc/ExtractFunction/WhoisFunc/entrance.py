# !/usr/bin/python
# encoding:utf-8

#
# whois信息获取入口
# @author wangkai
#

import static
import domain_analyse
import update_record
import json


# 获取whois信息
# @param raw_domain 输入域名
# @return json格式响应

def get_domain_whois(raw_domain = ""):

    #返回信息初始化
    domain_whois = {"domain": "",             # 域名
        "flag": 0,                            # 状态标记
        "status": "",                         # 域名状态
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
        "name_server": "",                    # 域名服务器
        "hash_value": 0,                      # 哈希值
    }
    
    DB = static.main_DB # 数据库操作对象
    DB.get_connect()
    
    do_an = domain_analyse.domain_analyse.DomainAnalyse(raw_domain)
    domain_utf8 = do_an.get_utf8_domain() # 用于返回显示的域名（utf8格式）
    domain_punycode = do_an.get_punycode_domain() # punycode编码域名
    tld = do_an.get_tld() # 域名的tld

    # 判断数据库中是否有该域名记录
    result = DB.db_select(nature = 'domain_whois', domain = domain_punycode)

    # 表示存在该记录
    if result:
        special_tld = ['com', 'net', 'cc', 'jobs', 'tv'] # 存在二级服务器的顶级后缀

        if result[0][1] <= 122: # 表示数据库存储为故障信息
            domain_whois = update_record.update_record(do_an) # 数据更新
        elif tld in special_tld and result[0][1] <= 122: # 对有二级服务器的进行子啊次处理
            domain_whois = update_record.update_record(do_an) # 数据更新
        else: # 储存信息正常，直接读取
            result = result[0]
            domain_whois['domain'] = result[0]
            domain_whois['flag'] = result[1]
            domain_whois['domain_status'] = result[2]
            domain_whois['top_whois_server'] = result[3]
            domain_whois['sec_whois_server'] = result[4]
            domain_whois['reg_name'] = result[5]
            domain_whois['reg_phone'] = result[6]
            domain_whois['reg_email'] = result[7]
            domain_whois['org_name'] = result[8]
            domain_whois['sponsoring_registrar'] = result[9]
            domain_whois['name_server'] = result[10]
            domain_whois['creation_date'] = result[11]
            domain_whois['expiration_date'] = result[12]
            domain_whois['updated_date'] = result[13]
            domain_whois['insert_time'] = result[14]
            domain_whois['domain_details'] = result[15]
            domain_whois['hash_value'] = result[16]
    # 没有该记录，进行添加
    else:
        domain_whois = update_record.add_record(do_an) # 数据添加
    DB.db_commit()
    DB.db_close()

    if domain_whois:
        domain_whois['domain'] = domain_utf8 # utf8格式域名
        return domain_whois
    else:
        return None

if __name__ == '__main__':

    # domain = raw_input("domain: ")
    domain = 'baidu.cn'
    result = get_domain_whois(domain)

    if result:
        print "---------------domain_whois-----------------"    
        print "domain:           ", result['domain']
        print "flag:             ", result['flag']
        print "domain_status:    ", result['domain_status']
        print "sponsoring_registrar:", result['sponsoring_registrar']
        print "top_whois_server: ", result['top_whois_server']
        print "sec_whois_server: ", result['sec_whois_server']
        print "reg_name:         ", result['reg_name']
        print "reg_phone:        ", result['reg_phone']
        print "reg_email:        ", result['reg_email']
        print "org_name:         ", result['org_name']
        print "updated_date:     ", result['updated_date']
        print "creation_date:    ", result['creation_date']
        print "expiration_date:  ", result['expiration_date']
        print "insert_time:      ", result['insert_time']
        print "hash_value:       ", result['hash_value']
        print "name_server:      ", result['name_server']
        print
        print "-----------------details--------------------"
        print result['details']
        print "--------------------------------------------"
        
