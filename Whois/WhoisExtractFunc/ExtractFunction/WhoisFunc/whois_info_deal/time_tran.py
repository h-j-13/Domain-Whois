# !usr/bin/python
# encoding:utf8


#
# 时间测试的统一
# @author wangkai
# @version 1.0
# 2015.11.30
#

import re



month = {'JANUARY ':  '01',
        'FEBRUARY ':  '02',
        'MARCH ':  '03',
        'APRIL ':  '04',
        'MAY ':  '05',
        'JUNE ':  '06',
        'JULY ':  '07',
        'AUGUST ':  '08',
        'SEPTEMBER ':  '09',
        'OCTOBER ':  '10',
        'NOVEMBER ':  '11',
        'DECEMBER ':  '12',
        'JAN':  '01',
        'FEB':  '02',
        'MAR':  '03',
        'APR':  '04',
        'MAY':  '05',
        'JUNE':  '06',
        'JULY':  '07',
        'AUG':  '08',
        'SEP':  '09',
        'OCT':  '10',
        'NOV':  '11',
        'DEC':  '12'
        }


# @param time 原始输入时间string
# @return 统一后的时间格式string 2014-11-04T06:00:45Z(标准格式)
def time_tran(raw_time):
    pattern_ = re.(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ')
    if pattern.findall(raw_time):
        return raw_time

# 2003-03-17 12:20:05

    
    
    
    
    
    
if '__name__' == '__main__':
    
    
  
    