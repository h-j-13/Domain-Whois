# !/usr/bin/python
# encoding:utf-8

# 
# 初始数据建立
# @author wangkai
#

import static
import domain_analyse
import update_record
import time
import datetime
import Queue
import threading
import gc


_DB = static.main_DB #　数据库操作对象

domain_queue = Queue.Queue(-1) #　域名队列
whois_addr_dict = {} #　whois_addr字典

DOMAIN_COUNT = 1 # 域名计数

lock_domain = threading.Lock() # 域名锁

# 工作线程
class WorkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        
        global domain_queue, lock_domain

        while True:
            if lock_domain.acquire():
                if not domain_queue.empty():
                    domain = domain_queue.get()
                    lock_domain.release()
                    data_deal(domain)
                else:
                    lock_domain.release()
                    break

# 域名队列监控线程   
class DomainQueue(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    
    def ru


 # 进程调度
def build_init_data():

    global domain_queue

    get_domains() # 初次获取域名

    while not domain_queue.empty():
        work_thread_list = []
        for i in range(static.PROCESS_MAX):
            work_thread = WorkThread()
            work_thread.start()
            work_thread_list.append(work_thread)
            
        for work_thread in work_thread_list:
            work_thread.join()

        print str(datetime.datetime.now()).split(".")[0], ' commit'
        _DB.db_commit()
        get_domains() # 再次获取域名

# 域名处理
def data_deal(domain):
    do_an = domain_analyse.DomainAnalyse(domain)
    update_record.update_record(do_an)
    gc.collect()

# 从数据库中获得初始需要处理的域名
def get_domains():
    global _DB, domain_queue
    for table in static.INIT_TABLES:
        domains = _DB.db_select("domains", table)
        for domain in domains:
            if static.TEST_COUNT != -1 and static.DOMAIN_COUNT > static.TEST_COUNT:
                return 
            domain_queue.put(domain[0])
            DOMAIN_COUNT += 1

if __name__ == '__main__':

    print str(datetime.datetime.now()).split(".")[0], "Start"
    _DB.get_connect()

    build_init_data()

    _DB.db_close()
    print str(datetime.datetime.now()).split(".")[0], "End"
