# /usr/bin/python
# encoding:utf8

import re

def general_manage(data, domain_whois):

def data_deal(data, domain_whois):

    sign_not_exist_list = ['No match for', 'Available\nDomain', 'The queried object does not exist:',\
     'Requested Domain cannot be found', 'The queried object does not exist: Domain name',\
     'No Data Found', 'Domain Status: No Object Found', 'Domain not found.', 'no matching objects found', \
     'No matching record.', 'No match', '\" is available for registration', '\"  not found', \
     'This domain name has not been registered.', 'NOT FOUND', 'Status: Not Registered',\
     'The queried object does not exists'

     ]
    for sign_not_exist in sign_not_exist_list:
        if data.find(sign_not_exist) != -1:
            domain_whois['status'] = 'NOTEXIST'
            return domain_whois
            
    status = ''
    name_server = ''
        
    pattern = re.compile(r'(Last updated Date ?:.*|Last Updated On ?:.*\
|Update Date ?:.*|Registrant Phone ?:.*|Registrant Name ?:.*\
|Registrant Organization ?:.*|Registrant Email ?:.*\
|Registrant Phone Number ?:.*|Updated Date ?:.*\
|Creation Date ?:.*|Expiration Date ?:.*|Expires On ?:.*\
|Creation date ?:.*|Created Date ?:.*|Registrant Organisation ?:.*\
|Registrant E-mail ?:.*|Update date ?:.*|Created On ?:.*\
|Expiration date ?:.*|Updated date ?:.*|Updated On ?:.*\
|Registrant Firstname ?:.*\nRegistrant Lastname ?:.*|Expiry Date ?:.*\
|Create Date ?:.*|Status:.*|Registrar:.*|Name Server:.*)')
    
    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Registrant Phone' or \
            match.split(':')[0].strip() == 'Registrant Phone Number':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        
        elif match.find('Firstname') != -1 and match.find('Lastname') != -1:
            reg_name = match.split('\n')[0].split(':')[1].strip() + ' ' + \
                match.split('\n')[1].split(':')[1].strip()
            domain_whois['reg_name'] = match.split(':')[1].strip()
        
        elif match.split(':')[0].strip() == 'Registrant Email' or \
               match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        
        elif match.split(':')[0].strip() == 'Registrant Organization' or \
            match.split(':')[0].strip() == 'Registrant Organisation':
            domain_whois['org_name'] = match.split(':')[1].strip()
        
        elif match.split(':')[0].strip() == 'Updated Date' or \
            match.split(':')[0].strip() == 'Update Date' or \
            match.split(':')[0].strip() == 'Last updated Date' or \
            match.split(':')[0].strip() == 'Update date' or \
            match.split(':')[0].strip() == 'Last Updated On' or \
            match.split(':')[0].strip() == 'Updated date' or \
            match.split(':')[0].strip() == 'Updated On':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
       
        elif match.split(':')[0].strip() == 'Creation Date' or \
            match.split(':')[0].strip() == 'Creation date' or \
            match.split(':')[0].strip() == 'Created Date' or \
            match.split(':')[0].strip() == 'Created On' or \
            match.split(':')[0].strip() == 'Create Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
       
        elif match.split(':')[0].strip() == 'Expiration Date' or \
            match.split(':')[0].strip() == 'Expiration date' or \
            match.split(':')[0].strip() == 'Expiry Date' or \
            match.split(':')[0].strip() == 'Expires On':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
       
        elif match.split(':')[0].strip() == 'Status':
            status += match.split(':', 1)[1].strip().split(' ')[0].strip().upper()
            status += ';'

        elif match.find('Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';' 

    domain_whois['status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)
    return domain_whois
            
            
def cn_manage(domain_whois, data):
        
    if data.find('No matching record.') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois
    
    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain Status:.*|Registrant:.*|Registrant Contact Email:.*\
|Registration Time:.*|Expiration Time:.*|Sponsoring Registrar:.*|Name Server:.*)')
     
    for match in pattern.findall(data):
        if match.find('Domain Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('Registrant:') != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.find('Registrant Contact Email:') != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.find('Registration Time:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('Expiration Time:') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('Sponsoring Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)
    
    return domain_whois
    
def ac_manage(domain_whois, data):
    
    if re.search(r'(Domain .+? is available for purchase)', data) != None:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois
            
    status = ''
    name_server = ''
    pattern = re.compile(r'(Status(\s)+?:.*|Expiry(\s)+?:.*|NS.*|Owner(.*\n)+?\n)')
    for match in pattern.findall(data):
        match = match[0]
        print match
        if match.split(':')[0].strip() == 'Status':
            status += match.split(':')[1].strip()
            status += ';'
        elif match.split(':')[0].find('NS') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].find('Expiry') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.find('Owner') != -1:
            infos = match.split('\n')
            domain_whois['reg_name'] = infos[0].split(':')[1].strip()
            domain_whois['org_name'] = infos[1].split(':')[1].strip()
         
    domain_whois['status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)
    return domain_whois


def ae_manage(domain_whois, data):
    if data.find('No Data Found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois
        
    pattern = re.compile(r'(Status:.*|Registrant Contact Name:.*|Registrant Contact Email:.*\
|Registrant Contact Organisation:.*|Name Server:.*)')
    status = ''
    name_server = ''
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            status += match.split(':')[1].strip()
            status += ';'
        elif match.split(':')[0].strip() == 'Registrant Contact Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Contact Organisation':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ';'
            
    domain_whois['status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')      
    domain_whois['details'] = str(data)
    return domain_whois
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    