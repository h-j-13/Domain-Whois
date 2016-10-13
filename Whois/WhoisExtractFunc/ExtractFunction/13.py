import re
def ws_manage(domain_whois, data):

    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrar WHOIS Server:.*|Updated Date:.*|Creation Date:.*|Registrar Registration Expiration Date:.*|\
Registrar:.*|Registrar Abuse Contact Email:.*|Registrar Abuse Contact Phone:.*|Domain Status:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.find('Domain Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.find('Registrar WHOIS Server: ') != -1:
            domain_whois['top_whois_server'] = match.split(':')[1].strip()
        elif match.find('Updated Date:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.find('Creation Date:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.find('Expiration Date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.find('Registrar:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()
        elif match.find('Registrar Abuse Contact Email:') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.find('Registrar Abuse Contact Phone:') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ua_manage(domain_whois, data):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrant:.*|nserver:.*|status:.*|created:.*|modified:.*|expires:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registrant':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':', 1).strip()
        elif match.split(':')[0].strip() == 'modified':
            domain_whois['updated_date'] = match.split(':', 1).strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':', 1).strip()

    pattern2 = re.compile(r'(Registrar([\s\S]*?)Registrant)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(organization:.*)')
        #元组转换成字符串
        data2 =  "".join(tuple(match2))
        #print data2
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'organization':
                domain_whois['sponsoring_registrar'] = match3.split(':')[1].strip()

    pattern4 = re.compile(r'(Registrant([\s\S]*?)Administrative Contacts)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(person:.*|organization:.*|e-mail:.*|phone:.*)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'person':
                domain_whois['reg_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'organization':
                domain_whois['org_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'e-mail':
                domain_whois['reg_email'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'phone':
                domain_whois['reg_phone'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def tz_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrant:.*|registrar:.*|registered:.*|changed:.*|\
|expire:.*|org:.*|name:.*|phone:.*|e-mail:.*|nserver:.*|created:.*)')

    for match in pattern.findall(data):
        if match.find('Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('nserver:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.find('registrant:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.find('changed:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.find('created:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.find('expire:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.find('name:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()
        elif match.find('phone') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
        elif match.find('e-mail') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.find('org:') != -1:
            domain_whois['org_name'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

def tw_manage(data, domain_whois):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(  Domain Status:.*|   Record expires on.*|   Record created on.*|\
|Domain servers in listed order:.*\n.*\n.*\n.*|Registration Service Provider:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':', 1)[1].strip().split(' ')[0].strip().upper()
            domain_status += ';'
        elif match.split('on')[0].strip() == 'Record expires':
            domain_whois['expiration_date'] = match.split('on')[1].strip()[:-12]
        elif match.split('on')[0].strip() == 'Record created':
            domain_whois['creation_date'] = match.split('on')[1].strip()[:-12]
        elif match.split(':')[0].strip() == 'Registration Service Provider':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain servers in listed order':
            for item in match.split('\n'):
                if item.strip()!='Domain servers in listed order:':
                    if item.strip():
                        name_server += item.strip()
                        name_server += ';'
                    else:
                        break

    pattern4 = re.compile(r'(   Registrant([\s\S]*?)   Administrative Contact)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(      \+.*|.*@.*)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if match5.strip()[0]=='+':
                domain_whois['reg_phone'] = match5.strip()
            if match5.find('@')!=-1:
                for item in match5.split(" "):
                    if item.find("@")!=-1:
                        domain_whois['reg_email'] = item.strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois

def ee_manage(data, domain_whois):

    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(nserver:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern4 = re.compile(r'(Domain([\s\S]*?)Administrative)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(name:.*|status:.*|registered:.*|changed:.*|expire:.*|email:.*|changed:.*|)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'name':
                if match5.split(':')[1].strip() != domain_whois['domain']:
                    domain_whois['reg_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'status':
                domain_status += match5.split(':')[1].strip()
                domain_status += ';'
            elif match5.split(':')[0].strip() == 'registered':
                domain_whois['creation_date'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip() == 'changed':
                domain_whois['updated_date'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip() == 'expire':
                domain_whois['expiration_date'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'email':
                if match5.split(':')[0].strip().find("Not Disclosed")!=-1:
                    domain_whois['reg_email'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois

def th_manage(data, domain_whois):

    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrar:.*|Name Server:.*|Status:.* |Updated date:.*|Created date:.*|Exp date:.*|Domain Holder:.*)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Updated date':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Created date':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Exp date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Holder':
            domain_whois['reg_name'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

def ru_manage(data, domain_whois):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(person:.*|nserver:.*|e-mail:.*|state:.*|registrar:.*|created:.*|paid-till:.*|org:.*|registrar:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'state':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'person':
            if match.split(':')[1].strip() != 'Private Person':
                domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'paid-till':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'org':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def nz_manage(data, domain_whois):

    if data.find('query_status: 220 Available') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(domain_dateregistered:.*|domain_datebilleduntil:.*|domain_datelastmodified:.*|registrant_contact_name:.*|ns_name.*:.*\
|domain_delegaterequested:.*|registrar_name:.*|registrar_phone:.*|registrar_email:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'domain_delegaterequested':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'domain_dateregistered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datebilleduntil':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datelastmodified':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_name':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar_phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar_email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar_name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip()[:-3] == 'ns_name':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def sk_manage(domain_whois, data):

    if data.find('Not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Admin-name.*|Admin-email.*|Last-update.*|Valid-date.*|dns_name.*|)')

    for match in pattern.findall(data):

        if match.split(' ')[0].strip() == 'Admin-name':
            temp=''
            for item in match.split(' '):
                if item:
                    temp+=item
                    temp+=" "
            #print temp.strip('Admin-name ')
            domain_whois['reg_name'] = temp.strip('Admin-name ')
        elif match.split(' ')[0].strip() == 'Admin-email':
            temp=''
            for item in match.split(' '):
                if item:
                    temp+=item
                    temp+=" "
            domain_whois['reg_email'] = temp.strip('Admin-email ')
        elif match.split(' ')[0].strip() == 'Last-update':
            temp=''
            for item in match.split(' '):
                if item:
                    temp+=item
                    temp+=" "
            domain_whois['updated_date'] = temp.strip('Last-update ')
        elif match.split(' ')[0].strip() == 'Valid-date':
            temp=''
            for item in match.split(' '):
                if item:
                    temp+=item
                    temp+=" "
            domain_whois['expiration_date'] = temp.strip('Valid-date ')
        elif match.split(' ')[0].strip() == 'dns_name':
            temp=''
            for item in match.split(' '):
                if item:
                    temp+=item
                    temp+=";"
            name_server += temp[9:]

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def sg_manage(data, domain_whois):

    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    temp=''

    pattern = re.compile(r'(    Domain Name:.*|Registrar:.*|    Creation Date:.*|    Modified Date:.*|    Expiration Date:.*|    Domain Status:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Domain Name':
            temp += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Modified Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    pattern4 = re.compile(r'(Registrant([\s\S]*?)Administrative)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(        Name:.*|)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()

    #print temp
    pattern2 = re.compile(r'(.*\..*\..*)')#匹配出所有符合格式的地址，并去掉域名
    for match2 in pattern2.findall(data):
        if match2.find(temp)==-1:
            name_server += match2.strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois

def scot_manage(domain_whois, data):

    if data.find('no matching objects found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Creation Date:.*|Update Date:.*|Registry Expiry Date:.*|Sponsoring Registrar:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*|)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Update Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ro_manage(domain_whois, data):

     if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registered On:.*|Registrar:.*|Domain Status:.*|Nameserver:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registered On':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Nameserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def rs_manage(domain_whois, data):

    if data.find('Domain is not registered') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain status:.*|Registration date:.*|Modification date:.*|Expiration date:.*|Registrar:.*|Registrant:.*|DNS:.*|)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Domain status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registration date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Modification date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'DNS':
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def qa_manage(domain_whois, data):

    if data.find('No Data Found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Last Modified:.*|Registrar Name:.*|Status:.* |Registrant Contact Email:.*|Name Server IP:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server IP':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Last Modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def pf_manage(data, domain_whois):
    if data.find('Domain unknown') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status :.*|Created.*|Last renewed.*|Expire.*|\
|Name server.*|Registrar Company Name :.*|Registrant Name :.*|)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip().find("Created")!=-1:
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Last renewed") != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Expire") != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrar Company Name") != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrant Name") != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Name server") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def om_manage(data, domain_whois):
    if data.find('No Data Found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Last Modified:.*|Registrar Name.*|Status.*|Registrant Contact Name.*|\
|Registrant Contact Email.*|Name Server:.*|)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip().find("Last Modified") != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find("Registrant Contact Email") != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrar Name") != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrant Contact Name") != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Name Server") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def co_za_manage(data, domain_whois):

    if data.find('Available') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrant:\n.*|        Email:.*|        Tel:.*|Registrar:\n.*|Registration Date:.*|Renewal Date:.*|Name Servers:\n.*\n.*\n.*|Domain Status:\n.*|)')

    for match in pattern.findall(data):
        if match.find('Domain Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('Registrant:') != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.find('        Email:') != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.find('        Tel:') != -1:
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.find('Registration Date:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('Renewal Date:') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.find('Name Servers:') != -1:
            temp_ns=match.split("\n")
            for ns in temp_ns[1:]:
                name_server += ns.strip()
                name_server += ';'
            name_server.strip("Name Servers:;").strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def si_manage(domain_whois, data):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrar:.*|nameserver:.*|registrant:.*|status:.*|created:.*|expire:.*|nameserver:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'registrant':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'status':
            domain_status+=match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expire':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def bg_manage(data, domain_whois):

    if data.find('not exist') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    temp=''

    pattern = re.compile(r'(requested on:.*|activated on:.*|expires at:.*|registration status:.*|    Expiration Date:.*|    Domain Status:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registration status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Domain Name':
            temp += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'activated on':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'requested on':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expires at':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern4 = re.compile(r'(ADMINISTRATIVE CONTACT([\s\S]*?)TECHNICAL CONTACT)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(  tel:.*|.*@.*)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'tel':
                domain_whois['reg_phone'] = match5.split(':')[1].strip()
            elif match5.strip().find('@')!=-1:
                domain_whois['reg_email'] = match5.strip()

    pattern2 = re.compile(r'(NAME SERVER([\s\S]*?)DNSSEC)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(.*\..*\..*)')
        data2 = "".join(tuple(match2[0]))#这里会匹配出两个，使DNS变成两倍的，所以用[0]
        for match3 in pattern3.findall(data2):
            name_server += match3.strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois

def no_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern2 = re.compile(r'(Additional information([\s\S]*?)Additional information)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2))

        pattern = re.compile(r'(NORID Handle.*|Name.*|Created.*|Last updated.*|\
    |Phone Number.*|Email Address.*|Registrar Handle.*|)')
        for match in pattern.findall(data2):
            if match.split(':')[0].strip().find("NORID Handle") != -1:
                domain_whois['reg_name'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip().find("Name") != -1:
                domain_whois['org_name'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip().find("Email Address") != -1:
                domain_whois['reg_email'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip().find("Registrar Handle") != -1:
                domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip().find("Phone Number") != -1:
                domain_whois['reg_phone'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip().find("Created") != -1:
                domain_whois['creation_date'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip().find("Last updated") != -1:
                domain_whois['updated_date'] = match.split(':')[1].strip()

    pattern3 = re.compile(r'(Name Server Handle.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip().find("Name Server Handle") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def yt_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern2 = re.compile(r'(domain([\s\S]*?)nic-hdl)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2))

        pattern = re.compile(r'(status:.*|holder-c:.*|registrar:.*|Expiry Date:.*|created:.*|\
    |last-update:.*|nserver:.*|phone:.*|e-mail:.*|)')
        for match in pattern.findall(data2):
            if match.split(':')[0].strip() == 'status':
                domain_status += match.split(':')[1].strip()
                domain_status += ';'
            elif match.split(':')[0].strip() == 'holder-c':
                domain_whois['reg_name'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'registrar':
                domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'Expiry Date':
                domain_whois['expiration_date'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'created':
                domain_whois['creation_date'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'last-update':
                domain_whois['updated_date'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'phone':
                domain_whois['reg_phone'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'e-mail':
                domain_whois['reg_email'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'nserver':
                if name_server.find(match.split(':')[1].strip()) == -1:
                    name_server += match.split(':')[1].strip()
                    name_server += ';'

    pattern3 = re.compile(r'(Name Server Handle.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip().find("Name Server Handle") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def vg_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|created date:.*|updated date:.*|expiration date:.*|owner-name:.*|\
    |owner-phone:.*|owner-email:.*|nameserver:.*|registrar:.*|)')
    for match in pattern.findall(data):
            if match.split(':')[0].strip() == 'status':
                domain_status += match.split(':')[1].strip()
                domain_status += ';'
            elif match.split(':')[0].strip() == 'owner-name':
                domain_whois['reg_name'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'registrar':
                domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'expiration date':
                domain_whois['expiration_date'] = match.split(':',1)[1].strip()
            elif match.split(':')[0].strip() == 'created date':
                domain_whois['creation_date'] = match.split(':',1)[1].strip()
            elif match.split(':')[0].strip() == 'updated date':
                domain_whois['updated_date'] = match.split(':',1)[1].strip()
            elif match.split(':')[0].strip() == 'owner-phone':
                domain_whois['reg_phone'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'owner-email':
                domain_whois['reg_email'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'nameserver':
                if name_server.find(match.split(':')[1].strip()) == -1:
                    name_server += match.split(':')[1].strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def travel_manage(domain_whois, data):

   if data.find('Not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone Number:.*|Registrant Email:.*|Name Server:.*|Domain Registration Date:.*|Domain Expiration Date:.*|Domain Last Updated Date:.*| )')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone Number':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Domain Registration Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Last Updated Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def tm_manage(domain_whois, data):

    if data.find('available for purchase') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status :.*|Expiry :.*|NS.*?:.*|Owner:.* )')

    for match in pattern.findall(data):

        for i in range(10):
            ns="NS "+str(i)
            if match.split(':')[0].strip() == ns:
                name_server+=match.split(':')[1].strip()
                name_server+=";"
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiry':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Owner':
            domain_whois['reg_name'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def tf_manage(domain_whois, data):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|holder-c:.*|registrar:.* |Expiry Date:.*|created:.*|last-update:.*|nserver:.*|phone:.*|e-mail:.*|nserver:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'holder-c':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Expiry Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()          
        elif match.split(':')[0].strip() == 'last-update':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def st_manage(domain_whois, data):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(created-date:.*|updated-date:.*|expiration-date:.*|registrant-organization:.*|registrant-name:.*|registrant-phone:.*|registrant-email:.*|nameserver:.*|)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'registrant-phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant-email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant-name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created-date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'updated-date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expiration-date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant-organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def sm_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern2 = re.compile(r'(Domain Name([\s\S]*?)Technical Contact)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2))

        pattern = re.compile(r'(Phone:.*|Email:.*|Registration date:.*|Status:.*|Domain Name:.*|)')
        for match in pattern.findall(data2):
            if match.split(':')[0].strip() == 'Status':
                domain_status += match.split(':')[1].strip()
                domain_status += ';'
            elif match.split(':')[0].strip() == 'Registration date':
                domain_whois['creation_date'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match.split(':')[1].strip()

    pattern4 = re.compile(r'(DNS Servers([\s\S]*)\n)')
    for match4 in pattern4.findall(data):
        print match4
        pattern5 = re.compile(r'(.*\..*\..*)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            name_server += match5.strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def sh_manage(domain_whois, data):

    if data.find('available for purchase') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status :.*|Expiry :.*|Owner  :.*|NS.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiry':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Owner':
            domain_whois['reg_name'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('NS')!=-1:
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def science_manage(domain_whois, data):

    if data.find('No Domain exists for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Creation Date:.*|Update Date:.*|Registry Expiry Date:.*|Sponsoring Registrar:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Update Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def re_manage(domain_whois, data):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|holder-c:.*|registrar:.* |Expiry Date:.*|created:.*|last-update:.*|nserver:.*|phone:.*|e-mail:.*|nserver:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'holder-c':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Expiry Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'last-update':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def pr_manage(data, domain_whois):
    if data.find('not registered') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created On:.*|Expires On:.*|DNS:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expires On':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'DNS':
            name_server += match.split(':')[1].strip()
	    name_server+=";"

    pattern4 = re.compile(r'(Contact:      Registrant([\s\S]*)Contact:      Administrative)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Organization:.*|Name:.*|Phone:.*|E-mail:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Organization':
                domain_whois['org_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'E-mail':
                domain_whois['reg_email'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def nrw_manage(data, domain_whois):

    if data.find('no matching objects found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Update Date:.*|Creation Date:.*|Registry Expiry Date:.*|Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*\
|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Update Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def name_manage(data, domain_whois):

    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()+";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def moe_manage(data, domain_whois):

    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Updated Date:.*|Creation Date:.*|Registry Expiry Date:.*|Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*\
|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = matc.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def me_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain Create Date:.*|Domain Last Updated Date:.*|Domain Expiration Date:.*|Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*\
|Registrant Organization:.*|Registrant Phone:.*|Registrant E-mail:.*|Nameservers:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Domain Create Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Last Updated Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Nameservers':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ly_manage(data, domain_whois):

    if data.find('Not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    temp=''

    pattern = re.compile(r'(   Phone:.*|.*@.*|Created:.*|Updated:.*|Expired:.*|Domain Status:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Updated':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expired':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.strip().find('@') != -1:
            domain_whois['reg_email'] = match.strip()

    pattern4 = re.compile(r'(Domain servers in listed order([\s\S]*?)Domain Status)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(.*\..*\..*)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if name_server.find(match5.strip()) == -1:
                name_server += match5.strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whoiss

def lv_manage(data, domain_whois):

    if data.find('Status: free') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Nserver:.*|Updated:.*|Status:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Updated':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern4 = re.compile(r'([Holder]([\s\S]*?)[Tech])')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Email:.*|Phone:.*|)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois

def kz_manage(data, domain_whois):

    if data.find('Nothing found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(server.*|Domain created:.*|Last modified :.*|Domain status :.*|Registar created:.*|Registar created:.*\
                         |Name.*|Organization Name.*|Phone Number.*|Email Address.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('server')!=-1:
            if match.split(':')[0].strip().count('.')>2:#用于去掉一行无用的信息
                name_server += match.split(':')[1].strip()
                name_server += ';'
        elif match.split(':')[0].strip() == 'Domain created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registar created':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('Name')!=-1:
            if match.split(':')[0].strip().count('.') > 2:
                domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('Organization Name')!=-1:
            print match
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('Phone Number')!=-1:
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('Email Address') != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois

def ir_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(
        r'(status:.*|holder-c:.*|org:.* |expire-date:.*|created:.*|last-updated:.*|nserver:.*|phone:.*|e-mail:.*|nserver:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'holder-c':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'org':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'expire-date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'last-updated':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def io_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status :.*|Expiry :.*|NS.*|Owner  :.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Expiry':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('NS') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'Owner':
            domain_whois['reg_name'] = match.split(':')[1].strip()
            break #只取得第一行的信息，即姓名。

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def im_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Expiry Date:.*|Name Server:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    pattern2 = re.compile(r'(Domain Managers([\s\S]*)Domain Owners)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Name:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Name':
                domain_whois['sponsoring_registrar'] = match3.split(':')[1].strip()

    pattern4 = re.compile(r'(Domain Owners([\s\S]*)Administrative Contact)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Name:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def hu_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(record created:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'record created':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def dz_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(
        r'(Contact administratif.*|Organisme administratif.*|Telephone contact administratif.*|Mail contact administratif.*|Date de creation.*|)')

    for match in pattern.findall(data):
        if match.split('#')[0].strip().find('Contact administratif')!=-1:
            domain_whois['reg_name'] = match.split('#')[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Organisme administratif') != -1:
            domain_whois['org_name'] = match.split('#')[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Telephone contact administratif') != -1:
            domain_whois['reg_phone'] = match.split('#')[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Mail contact administratif') != -1:
            domain_whois['reg_email'] = match.split('#')[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Date de creation') != -1:
            domain_whois['creation_date'] = match.split('#')[1].strip('. ').strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def dm_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|created date:.*|updated date:.*|expiration date:.*|owner-name:.*|nameserver:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'created date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'updated date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expiration date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'owner-name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def cz_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrar:.*|registered:.*|changed:.*|expire:.*|nserver:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'expire':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'changed':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(expire([\s\S]*?)nsset)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(name:.*|e-mail:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'name':
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'e-mail':
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def cr_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(
        r'(registrar:.*|status:.*|registered:.* |changed:.*|expire:.*|org:.*|name:.*|phone:.*|e-mail:.*|nserver:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'org':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registered':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'expire':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'changed':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def club_manage(data, domain_whois):

    if data.find('No Domain exists') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*|Creation Date:.*|Registry Expiry Date:.*|Updated Date:.*| )')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ceo_manage(data, domain_whois):

    if data.find('not exist') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*|Creation Date:.*|Registry Expiry Date:.*|Updated Date:.*| )')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def at_manage(data, domain_whois):
    if data.find('nothing found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern2 = re.compile(r'(domain([\s\S]*?)street address)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(registrant:.*|nserver:.*|changed:.*|organization:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'registrant':
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'changed':
                domain_whois['updated_date'] = match3.split(':',1)[1].strip()
            elif match3.split(':')[0].strip() == 'organization':
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'nserver':
                name_server += match3.split(':')[1].strip()
                name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)
	return domain_whois

def asia_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant E-mail:.*|Nameservers:.*|Domain Create Date:.*|Domain Expiration Date:.*|Updated Date:.*| )')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Nameservers':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Domain Create Date':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Expiration Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ag_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*|Created On:.*|Expiration Date:.*|Last Updated On:.*| )')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def nc_manage(data, domain_whois):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created on 		.*|Expires on 		:.*|Last updated on 	:.*|Domain server.*|Registrant name 	:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Domain server')!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].strip() == 'Created on':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expires on':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant name':
            domain_whois['reg_name'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois

def museum_manage(data, domain_whois):
    if data.find('no matching objects found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created On:.*|Last Updated On:.*|Expiration Date:.*|Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*\
|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['updated_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def mx_manage(data, domain_whois):
    if data.find('Object_Not_Found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created On:.*|Expiration Date:.*|Last Updated On:.*|Registrar:.*|   DNS:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'DNS':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(Registrant:([\s\S]*?)Administrative Contact:)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(   Name:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match3.split(':')[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

def mo_manage(data, domain_whois):

    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrar:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def mk_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrar:.*|registered:.*|changed:.*|expire:.*|nserver:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'expire':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'changed':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(expire([\s\S]*?)nsset)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(name:.*|e-mail:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'name':
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'e-mail':
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    pattern4 = re.compile(r'(Domain Owners([\s\S]*)Administrative Contact)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Name:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def il_manage(data, domain_whois):
    if data.find('No data was found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(
        r'(reg-name:.*|phone:.*|e-mail:.* |nserver:.*|status:.*|validity:.*|registrar name:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'reg-name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'registrar name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'validity':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def in_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*|Created On:.*|Expiration Date:.*|Last Updated On:.*| )')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def se_manage(domain_whois, data):is

     if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(holder:.*|created:.*|modified:.*|expires:.*|nserver:.*|status:.*|registrar:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'holder':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def nu_manage(data, domain_whois):

    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|holder:.*|created:.*|modified:.*|expires:.*\
|nserver:.*|registrar:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'holder':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def int_manage(data, domain_whois):
    if data.find('this server does not have') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(nserver:.*|created:.*|changed:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'changed':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(contact:      administrative([\s\S]*?)contact:      technical)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(name:.*|organisation:.*|phone:.*|e-mail:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'name':
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'organisation':
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'phone':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'e-mail':
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def hk_manage(data, domain_whois):
    if data.find('not been registered') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain Status:.*|Registrar Name:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'expire':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Name Servers Information:([\s\S]*?)Status Information:)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(.*\..*\..*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            name_server += match3.strip()
            name_server += ';'

    pattern4 = re.compile(r'(Registrant Contact Information:([\s\S]*)Administrative Contact Information:)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Company English Name.*|Expiry Date:.*|Domain Name Commencement Date:.*|Phone:.*|Email:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip().find('Company English Name')!=-1:
                domain_whois['org_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Expiry Date':
                domain_whois['expiration_date'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip() == 'Domain Name Commencement Date':
                domain_whois['creation_date'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip() == 'Phone':
                print match5
                domain_whois['reg_phone'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def tf_manage(data, domain_whois):
    if data.find('Domain not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(created:.*|phone:.*|e-mail:.* |nserver:.*|status:.*|modified:.*|expires:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    pattern = re.compile(r'(descr:.*|)')#取第一个descr：的值作为name
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'descr':
            domain_whois['reg_name'] = match.split(':')[1].strip()
            break

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def post_manage(domain_whois, data):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Created On:.*|Last Updated On:.*|Expiration Date:.*|Sponsoring Registrar:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*|)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['updated_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server+=match.split(':')[1].strip()
            name_server+=';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois 

def mobi_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created On:.*|Last Updated On:.*|Expiration Date:.*|Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*\
|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['expiration_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['updated_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois


def gov_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    pattern = re.compile(r'(   Status:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

    domain_whois['domain_status'] = domain_status.strip(';')

    return domain_whois
#=====================================================

def lt_manage(data, domain_whois):
    if data.find('Status:			available') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Registered:.*|Registrar:.* |Contact email:.*|Contact organization:.*|Nameserver:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Contact name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Contact email':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Contact organization':
            domain_whois['org_name'] = match.split(':')[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')


    return domain_whois

def ie_manage(data, domain_whois):
    if data.find('Not Registered') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    temp = ''
    temp2 = ''

    pattern = re.compile(r'(admin-c:.*|registration:.*|renewal:.*|nserver:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registration':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'renewal':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'admin-c':
            temp += match.split(':',)[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(person([\s\S]*?)source)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(person:.*|nic-hdl:.*|)')
        data2 = "".join(tuple(match2)[0])

        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'nic-hdl':
                temp2 += match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'person':
                if temp2 == temp:
                    domain_whois['reg_name'] = match3.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def lu_manage(data, domain_whois):
    if data.find('No such domain') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(domaintype:.*|nserver:.*|registered:.*|org-name:.*|adm-name:.*|adm-email:.*|registrar-name:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'domaintype':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'registered':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'registrar-name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'adm-name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'adm-email':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'org-name':
            domain_whois['org_name'] = match.split(':')[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def hr_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(person:.*|org:.*|expires:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'person':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'org':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def dk_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|Registered:.*|Expires:.*|Hostname:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Hostname':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ca_manage(data, domain_whois):
    if data.find('Notice, available') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain Status:.*|Creation date:.*|Expiry date:.*|Updated date:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Creation date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiry date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Name servers:([\s\S]*?)% WHOIS look-up)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split("\n"):
            if line.find(':')==-1:
               if line.strip().split(' ')[0]:
                   name_server += line.strip().split(' ')[0]
                   name_server += ';'

    pattern4 = re.compile(r'(Administrative contact([\s\S]*)Technical contact)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(    Name:.*|    Phone:.*|    Email:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match5.split(':', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def by_manage(data, domain_whois):
    if data.find('not exists') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrar:.*|Updated Date:.*|Creation Date:.*|Expiration Date:.*|Domain Name Administrator:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Name Administrator':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ax_manage(data, domain_whois):
    if data.find('No records matching') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Name:.*|Organization:.*|Email address:.*|Telephone:.*|Created:.*|Name Serve.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Email address':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Created':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Telephone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Name Serve")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def au_manage(data, domain_whois):
    if data.find('No Data Found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Registrant Contact Name:.*|Registrar Name:.*|Registrant Contact Email:.*|Name Server:.*|Last Modified:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrant Contact Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Last Modified':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip().find("Name Server")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def tn_manage(domain_whois, data):

    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern1 = re.compile(r'(This is JWhoisServer serving.*?----------------------------------------)',re.S)
    pattern = re.compile(r'(First Name:.*|Last Name:.*|Date Created:.*|Tel:.*|Expiry date:.*|e-mail:.*|Registrar:.*|Activation:.*|Name Server (DB):.*|)')

    if pattern1.findall(data):

        data2=pattern1.findall(data)[0]
        #print ">>>>>>"+data2
        for match in pattern.findall(data2):
            if match.find('status:') != -1:
                domain_status += match.split(':')[1].strip()
                domain_status += ';'
            elif match.find('First Name:') != -1:
                domain_whois['reg_name']+=match.split(':')[1].strip().strip(".")
            elif match.find('Last Name:') != -1:
                if domain_whois['reg_name']:
                    domain_whois['reg_name']+=' '+match.split(':')[1].strip().strip(".")
                else:
                    domain_whois['reg_name']+=match.split(':')[1].strip().strip(".")
            elif match.find('Activation:') != -1:
                domain_whois['updated_date'] = match.split(':')[1].strip().strip(".")
            elif match.find('Tel:') != -1:
                domain_whois['reg_phone']=match.split(':')[1].strip().strip(".")
            elif match.find('e-mail:') != -1:
                domain_whois['reg_email']=match.split(':')[1].strip().strip(".")
            elif match.find('Name Server (DB):') != -1:
                name_server+=match.split(':')[1].strip().strip(".")
                name_server += ';'
            elif match.find('Registrar:') != -1:
                domain_whois['sponsoring_registrar']=match.split(':')[1].strip().strip(".")

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def ae_manage(data, domain_whois):
    if data.find('No Data Found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Registrant Contact Name:.*|Registrant Contact Name:.*|Registrar Name:.*|Registrant Contact Email:.*|Name Server:.*|Registrant Contact Organisation.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrant Contact Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Contact Organisation':
            domain_whois['org_name'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip().find("Name Server")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def vu_manage(domain_whois, data):

    if data.find('not valid') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(First Name:.*|Last Name:.*|Date Created:.*|Expiry date:.*|DNS servers1:.*|DNS servers2:.*)')

    for match in pattern.findall(data):
        if match.find('status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('First Name:') != -1:
            domain_whois['reg_name']+=match.split(':')[1].strip()
        elif match.find('Last Name:') != -1:
            domain_whois['reg_name']+=' '+match.split(':')[1].strip()
        elif match.find('DNS servers1:') != -1:
            name_server += match.split(':')[2].strip()
            name_server += ';'
        elif match.find('DNS servers2:') != -1:
            name_server += match.split(':')[2].strip()
            name_server += ';'
        elif match.find('DNS servers3:') != -1:
            name_server += match.split(':')[2].strip()
            name_server += ';'
        elif match.find('Date Created:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.find('Expiry date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def tv_manage(domain_whois, data):

   if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Updated Date:.*|Creation Date:.*|Registry Expiry Date:.*|Sponsoring Registrar:.*|Domain Status:.*|Name Server:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server+=";"
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()[:-3]
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def pe_manage(data, domain_whois):
    if data.find('No Object Found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*|Registrant Name:.*|Admin Email:.*|Name Server:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Admin Email':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find("Name Server")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def cc_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(   Updated Date:.*|   Creation Date:.*|   Registry Expiry Date:.*|   Sponsoring Registrar:.*|   Domain Status:.*|   Name Server:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find("Name Server")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

def cn_manage(data, domain_whois):
    if data.find('No matching record') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrant:.*|Registrant Contact Email:.*|Sponsoring Registrar:.*|Registration Time:.*|Expiration Time:.*|Domain Status:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registration Time':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant':
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Time':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find("Name Server")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois
