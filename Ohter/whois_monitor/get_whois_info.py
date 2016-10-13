# coding:utf-8

#
# Whois检测程序
# func  : 获取数据库中的domain/whois信息
# time  : 2016.10.4
# author: @`13
#

from db_opreation import DataBase


TABLE_NUM = 100

def GetWhoisInfo(tld = None):
    """
    :param tld: 需要获取的tld的数据 / 不支持列表
    :return: 此tld在数据库的数据信息
    """
    db = DataBase()
    db.get_connect()
    finsh_num = 0
    for table_num in range(1, TABLE_NUM+1):
        SQL = """SELECT COUNT(*) FROM domain_whois.domain_whois_{num} WHERE`tld` = '{tld}' AND `flag` > 0""".format(
                num='1', tld=tld)
        finsh_num += db.execute(SQL)[0][0]
    print finsh_num

    un_finsh_num = 0
    for table_num in range(1, TABLE_NUM + 1):
        SQL = """SELECT COUNT(*) FROM domain_whois.domain_whois_{num} WHERE`tld` = '{tld}' AND `flag` < 0""".format(
            num='1', tld=tld)
        un_finsh_num += db.execute(SQL)[0][0]
    print un_finsh_num


if __name__ == "__main__":
    GetWhoisInfo('cn')
