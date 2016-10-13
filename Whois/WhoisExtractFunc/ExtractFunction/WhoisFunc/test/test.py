# !usr/bin/python
# encoding:utf8




a = 1

def out():
    a += 1
    print a

if __name__ == '__main__':
    out()






























# import shelve
# import re


# a = """addPeriod
# autoRenewPeriod
# inactive
# ok
# pendingCreate
# pendingDelete
# pendingRenew
# pendingRestore
# pendingTransfer
# pendingUpdate
# redemptionPeriod
# renewPeriod
# serverDeleteProhibited
# serverHold
# serverRenewProhibited
# serverTransferProhibited
# serverUpdateProhibited
# transferPeriod
# clientDeleteProhibited
# clientHold
# clientRenewProhibited
# clientTransferProhibited
# clientUpdateProhibited
# ACTIVE
# REGISTRY-LOCK
# REGISTRAR-LOCK
# REGISTRY-HOLD
# REGISTRAR-HOLD
# REDEMPTIONPERIOD
# PENDINGRESTORE
# PENDINGDELETE"""
# i = 1
# for line in a.split('\n'):
#     while line.find(' ') != -1:
#         line = line.replace(' ', '')
#     while line.find('-') != -1:
#         line = line.replace('-', '')
#     print '\'' + line.upper() + '\': \'' + str(i) + '\','
#     i += 1









# a = """1月 JANUARY JAN.
# 2月 FEBRUARY FEB.
# 3月 MARCH MAR.
# 4月 APRIL APR.
# 5月 MAY MAY.
# 6月 JUNE JUNE
# 7月 JULY JULY
# 8月 AUGUST AUG.
# 9月 SEPTEMBER SEP.
# 10月 OCTOBER OCT.
# 11月 NOVEMBER NOV.
# 12月 DECEMBER DEC."""

# i = 1
# for line in a.split('\n'):
#     print '\'' + line.split(' ')[2].upper().strip('.'),
#     # for char in line:
#     #     if char.isalpha():
#     #         print char,

#     print '\': ',
#     print '\'' + str(i) + '\','
#     i += 1
























# a = """
# OK  1
# INACTIVE    2
# CLIENTTRANSFERPROHIBITED   3
# CLIENTDELETEPROHIBITED    4
# CLIENTRENEWPROHIBITED    5
# CLIENTUPDATEPROHIBITED  6
# PENDINGTRANSFER    7
# PENDINGUPDATE   8
# PENDINGRENEW    9
# PENDINGDELETE  10
# SERVERHOLD   11
# CLIENTHOLD   12
# SERVERDELETEPROHIBITED    13
# SERVERUPDATEPROHIBITED    14
# SERVERTRANSFER PROHIBITED    15
# SERVERRENEW PROHIBITED   16
# SERVERLOCK   17
# CLIENTDELETEPROHIBITED   18
# CLIENTUPDATEPROHIBITED    19
# CLIENTTRANSFERPROHIBITED  20
# CLIENTLOCK   21
# REDEMPTIONPERIOD   22
# PENDINGRESTORE   23
# ACTIVE   24
# REGISTRYLOCK   25
# REGISTRARLOCK  26
# REGISTRYHOLD   27
# REGISTRARHOLD  28
# REDEMPTIONPERIOD    29
# PENDINGRESTORE  30
# PENDINGDELETE   31
# """

# for line in a.split('\n'):
#     out = ''
#     infos = re.split(r' ', line)
#     out += '\''
#     i = 0
#     while i < len(infos) - 2:
#         out += infos[i]
#         out += ' ' 
#         i += 1
#     out = out.strip()
#     out += '\': \''
#     out += infos[len(infos) - 1]
#     out += '\''
#     print out + ','

        


