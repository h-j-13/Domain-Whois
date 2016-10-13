# !usr/bin/python
# encoding:utf8


#
# whois信息标志确定
# @author wangkai
# @version 1.0
# 2015.11.30
#

def flag_manage(domain_whois):
    if domain_whois['details'] == 'ERROR -1': #连接超时
        flag = -1
    elif domain_whois['details'] == 'ERROR -2': #解析失败 Temporary failure in name resolution
        flag = -2
    elif domain_whois['details'] == 'ERROR -3': #无法连接
        flag = -3
    elif domain_whois['details'] == 'ERROR OTHER': #其他错误
        flag = -4
    elif domain_whois['details'] == '': #没有任何返回数据
        flag = 0
    else:
        if domain_whois['reg_name'] and domain_whois['reg_phone'] and domain_whois['reg_email'] and \
            domain_whois['org_name']: # 注册者信息完整
            flag_a = 2
        elif domain_whois['reg_name'] or domain_whois['reg_phone'] or domain_whois['reg_email'] or \
            domain_whois['org_name']: # 注册者信息不完善
            flag_a = 1
        else: # 无注册者信息
            flag_a = 0

        if domain_whois['creation_date'] and domain_whois['updated_date'] and domain_whois['expiration_date']:
            # 注册日期信息完整
            flag_b = 2
        elif domain_whois['creation_date'] or domain_whois['updated_date'] or domain_whois['expiration_date']:
            # 注册日期信息不完善
            flag_b = 1
        else: # 无注册日期信息
            flag_b = 0

        flag = 100 + flag_a * 10 + flag_b
    if flag < 0:
        domain_whois['details'] = ''

    domain_whois['flag'] = flag
    return domain_whois
