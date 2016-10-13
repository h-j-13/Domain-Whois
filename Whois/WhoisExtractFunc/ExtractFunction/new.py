import re

def ac_manage(data, domain_whois):

    if data.find('available for purchase') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status :.*|Expiry :.*|NS.*?:.*|Owner Name    :.*|Owner OrgName :.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('NS') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiry':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Owner Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Owner OrgName':
            domain_whois['org_name'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def dk_manage(data, domain_whois):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|Registered:.*|Expires:.*|Hostname:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expires':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Hostname':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def dm_manage(data, domain_whois):

    if data.find('not found') != -1:
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

    return domain_whois

def dz_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Contact administratif.*|Organisme administratif.*|Telephone contact administratif.*|Mail contact administratif.*|Date de creation.*|Registrar.*)')

    for match in pattern.findall(data):
        if match.split('#')[0].strip().find('Contact administratif')!=-1:
            domain_whois['reg_name'] = match.split('#',1)[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Organisme administratif') != -1:
            domain_whois['org_name'] = match.split('#',1)[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Telephone contact administratif') != -1:
            domain_whois['reg_phone'] = match.split('#',1)[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Mail contact administratif') != -1:
            domain_whois['reg_email'] = match.split('#',1)[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Date de creation') != -1:
            domain_whois['creation_date'] = match.split('#',1)[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split('#',1)[1].strip('. ').strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

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

def ru_manage(domain_whois, data):

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
        elif match.split(':')[0].strip() == 'org': #去除org tag下的'和" （否则插入MySQL时回报错）
            tmp = match.split(':')[1].strip()
            for char in tmp:
                #print char
                if char != "'":
                    if char != '''"''':
                        domain_whois['org_name'] += char
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def tn_manage(domain_whois, data):

    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern1 = re.compile(r'(This is JWhoisServer serving.*?----------------------------------------)',re.S)
    pattern = re.compile(r'(Status:.*|First Name:.*|Last Name:.*|Date Created:.*|Tel:.*|Expiry date:.*|e-mail:.*|Registrar:.*|Activation:.*|Name Server .*:.*|)')

    if pattern1.findall(data):
        tmp = str(pattern1.findall(data)[0])

    data2 = ''.join(tmp)
    # print type(data2)
    # print data2
    for tmp in pattern.findall(data2):
        match = ''.join(tmp)
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip(".").strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip(".").strip()
        elif match.split(':')[0].strip() == 'Tel':
            domain_whois['reg_phone'] = match.split(':')[1].strip(".").strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip(".").strip()
        elif match.split(':')[0].strip() == 'Activation':
            domain_whois['updated_date'] = match.split(':',1)[1].strip(".").strip()
        elif match.split(':')[0].strip() == 'Name Server (DB)':
            name_server += match.split(':')[1].strip(".").strip()
            name_server += ';'
        elif match.split(':')[0].strip() == 'Last Name':
            last_name = match.split(':')[1].strip(".").strip()
        elif match.split(':')[0].strip() == 'First Name':
            first_name = match.split(':')[1].strip(".").strip()
    domain_whois['reg_name'] = last_name + first_name

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

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
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')


    return domain_whois

def tw_manage(domain_whois, data):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(  Domain Status:.*|   Record expires on.*|   Record created on.*|\
|Registration Service Provider:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':', 1)[1].strip().split(' ')[0].strip().upper()
            domain_status += ';'
        elif match.split('on')[0].strip() == 'Record expires':
            domain_whois['expiration_date'] = match.split('on', 1)[1].strip()
        elif match.split('on')[0].strip() == 'Record created':
            domain_whois['creation_date'] = match.split('on', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registration Service Provider':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(   Domain servers in listed order:([\s\S]*?)Registration Service Provider)')
    for match4 in pattern2.findall(data):
        for line in str(match4[0]).split("\n"):
            if line:
                if line.find("Domain servers in listed order")==-1 and line.find("Registration Service Provider")==-1:
                    name_server += line.strip()
                    name_server += ';'

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
    return domain_whois

def tz_manage(domain_whois, data):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(nserver:.*|)')
    for match in pattern.findall(data):
        if match.split(":")[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'


    pattern2 = re.compile(r'(% Timestamp([\s\S]*?)e-mail.*)')
    for match2 in pattern2.findall(data):
        data2 = str(match2[0])
        pattern3 = re.compile(r'(registrar:.*|registered:.*|changed:.*|\
|expire:.*|org:.*|name:.*|phone:.*|e-mail:.*|)')
        for match in pattern3.findall(data2):
            if match.split(":")[0].strip() == 'registrar':
                domain_whois['sponsoring_registrar'] = match.split(":")[1].strip()
            elif match.split(":")[0].strip() == 'registered':
                domain_whois['creation_date'] = match.split(":", 1)[1].strip()
            elif match.split(":")[0].strip() == 'changed':
                domain_whois['updated_date'] = match.split(":", 1)[1].strip()
            elif match.split(":")[0].strip() == 'expire':
                domain_whois['expiration_date'] = match.split(":", 1)[1].strip()
            elif match.split(":")[0].strip() == 'org':
                domain_whois['org_name'] = match.split(":")[1].strip()
            elif match.split(":")[0].strip() == 'name':
                domain_whois['reg_name'] = match.split(":")[1].strip()
            elif match.split(":")[0].strip() == 'phone':
                domain_whois['reg_phone'] = match.split(":")[1].strip()
            elif match.split(":")[0].strip() == 'e-mail':
                domain_whois['reg_email'] = match.split(":")[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def fi_manage(domain_whois, data):

    if data.find('Domain not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(phone:.*|status:.*|created:.*|modified:.*|expires:.*|nserver:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            if match.split(':')[1].strip().find("[")!=-1:
                name_server += match.split(':')[1].strip().split("[")[0].strip()
            else:
                name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def gd_manage(domain_whois, data):

    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrar:.*|status:.*|created date:.*|updated date:.*|expiration date:.*|\
owner-organization:.*|owner-name:.*|owner-phone:.*|owner-email:.*|nameserver:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'updated date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expiration date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'owner-organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'owner-name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'owner-phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'owner-email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def bg_manage(domain_whois, data):

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

def nl_manage(domain_whois, data):
    if data.find('is free') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Status') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Domain nameservers([\s\S]*?)Record maintained)')
    for match4 in pattern2.findall(data):
        for line in str(match4[0]).split("\n"):
            if line:
                if line.find("Domain nameservers") == -1 and line.find(
                        "Record maintained") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def no_manage(domain_whois, data):
    if data.find('No match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Name Server Handle.*|Domain Holder Handle.*|Registrar Handle.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip().find("Name Server Handle") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].strip().find("Registrar Handle") != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Additional information([\s\S]*?)Email Address.*)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2))
        pattern = re.compile(r'(Name.*|Created.*|Last updated.*|\
    |Phone Number.*|Email Address.*|Type.*)')
        for match in pattern.findall(data2):
            if match.split(':')[0].strip().find("Type") != -1:
                type = match.split(':')[1].strip()
            elif match.split(':')[0].strip().find("Name") != -1:
                if str(type).find('organization') != -1:
                    domain_whois['org_name'] = match.split(':')[1].strip()
                else :
                    domain_whois['reg_name'] = match.split(':')[1].strip()
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

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def ua_manage(domain_whois, data):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern4 = re.compile(r'(domain([\s\S]*?)% Registrar)')
    for match4 in pattern4.findall(data):
        data3 = "".join(tuple(match4))
        pattern = re.compile(r'(registrant:.*|nserver:.*|status:.*|created:.*|modified:.*|expires:.*)')
        for match in pattern.findall(data3):
            if match.split(':')[0].strip() == 'registrant':
                domain_whois['reg_name'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'nserver':
                name_server += match.split(':')[1].strip()
                name_server += ";"
            elif match.split(':')[0].strip() == 'status':
                domain_status += match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'created':
                domain_whois['creation_date'] = match.split(':', 1)[1].strip()
            elif match.split(':')[0].strip() == 'modified':
                domain_whois['updated_date'] = match.split(':', 1)[1].strip()
            elif match.split(':')[0].strip() == 'expires':
                domain_whois['expiration_date'] = match.split(':', 1)[1].strip()


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

    return domain_whois

def ug_manage(domain_whois, data):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registered:.*|Expiry:.*|Status:.*|Admin Contact:.*|Nameserver:.*|Updated:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiry':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Admin Contact':
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(Admin Contact([\s\S]*?)Tech Contact)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Phone:.*|)')
        data2 = "".join(tuple(match2)[0])

        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def vg_manage(domain_whois, data):
    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|created date:.*|updated date:.*|expiration date:.*|owner-name:.*|\
    |owner-organization:.*|owner-organization:.*|owner-phone:.*|owner-email:.*|nameserver:.*|registrar:.*|)')
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
            elif match.split(':')[0].strip() == 'owner-organization':
                domain_whois['org_name'] = match.split(':')[1].strip()
            elif match.split(':')[0].strip() == 'created date':
                domain_whois['creation_date'] = match.split(':', 1)[1].strip()
            elif match.split(':')[0].strip() == 'updated date':
                domain_whois['updated_date'] = match.split(':', 1)[1].strip()
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

    return domain_whois

def uy_manage(domain_whois, data):

    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrado por:.*|Ultima Actualizacion:.*|Fecha de Creacion:.*|Estatus del dominio:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Estatus del dominio':
            domain_status += match.split(':', 1)[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Ultima Actualizacion':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Fecha de Creacion':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrado por':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Nombres de Dominio([\s\S]*?)NIC-Uruguay)')
    for match4 in pattern2.findall(data):
        for line in str(match4[0]).split("\n"):
            if line:
                if line.find("Dominio") == -1 and line.find(
                        "NIC-Uruguay") == -1:
                    name_server += line.strip('- ').strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def vu_manage(domain_whois, data):

    if data.find('not valid') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(First Name:.*|Last Name:.*|Date Created:.*|Expiry date:.*|DNS servers.*:.*|)')

    for match in pattern.findall(data):
        if match.find('status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('First Name:') != -1:
            domain_whois['reg_name'] += match.split(':')[1].strip()
        elif match.find('Last Name') != -1:
            domain_whois['reg_name'] += ' '+match.split(':')[1].strip()
        elif match.find('DNS servers') != -1:
            name_server += match.split(':', 1)[1].strip()
            name_server += ';'
        elif match.find('Date Created') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('Expiry date:') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def yt_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    owner = ''

    pattern3 = re.compile(r'(status:.*|holder-c:.*|nserver.*|registrar:.*|Expiry Date:.*|created:.*|last-update:.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'holder-c':
            owner += match.split(':')[1].strip()
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiry Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'last-update':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()


    pattern2 = re.compile(r'(nic-hdl([\s\S]*)source)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)).split('source')
        for data3 in data2:
            if data3.find(owner)!=-1:
                pattern = re.compile(r'(phone:.*|e-mail:.*|)')
                for match3 in pattern.findall(data3):
                    if match3.split(':')[0].strip() == 'phone':
                        domain_whois['reg_phone'] = match3.split(':')[1].strip()
                    elif match3.split(':')[0].strip() == 'e-mail':
                        domain_whois['reg_email'] = match3.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def sa_manage(domain_whois, data):
    if data.find('No Match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created on:.*|Last Updated on:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Created on':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated on':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Name Servers([\s\S]*?)Created on)')
    for match4 in pattern2.findall(data):
        for line in str(match4[0]).split("\n"):
            if line:
                if line.find("Name Servers") == -1 and line.find(
                        "Created on") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def bo_manage(data, domain_whois):
    if data.find('solo acepta') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Fecha de registro:.*|Fecha de vencimiento:.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Fecha de registro':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Fecha de vencimiento':
            domain_whois['expiration_date']  = match.split(':')[1].strip()

    pattern2 = re.compile(r'(TITULAR([\s\S]*?)CONTACTO ADMINISTRATIVO)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2))
        pattern = re.compile(r'(Organizacion:.*|Nombre:.*|Email:.*|Telefono.*)')
        for match3 in pattern.findall(data2):
            if match3.split(':')[0].strip() == 'Organizacion':
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Nombre':
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Telefono':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def kr_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Registrant.*:.*|AC E-Mail.*:.*|AC Phone Number.*:.*|Registered Date.*:.*|\
|Last Updated Date.*:.*|Expiration Date.*:.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Registrant':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'AC E-Mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'AC Phone Number':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registered Date':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated Date':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Primary Name Server([\s\S]*?)상기 정보는 UTF-8)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        pattern = re.compile(r'(Host Name.*:.*|)')
        for match3 in pattern.findall(data2):
            if match3.split(':')[0].strip() == 'Host Name':
                name_server += match3.split(':')[1].strip()
                name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def am_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Status:.*|Registrar:.*|Registered:.*|Last modified:.*|Expires:.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(DNS servers([\s\S]*?)Registered)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('DNS servers') == -1 and line.find('Registered') == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def be_manage(data, domain_whois):
    if data.find('AVAILABLE') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Registrant:.*\n.*|Status:.*|Registered:.*|Name:.*|)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.find('Registrant') != -1:
            domain_whois['sponsoring_registrar'] = match.split('\n', 1)[1].strip()

    pattern2 = re.compile(r'(Nameservers([\s\S]*?)Keys)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find("Nameservers") == -1 and line.find("Keys") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def bn_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Registrar:.*|Creation Date:.*|Modified Date:.*|Expiration Date:.*|Status:.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Modified Date':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Name Servers:([\s\S]*?)\n)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('Name Servers') == -1 and line.find('Registered') == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')


def cf_manage(data, domain_whois):
    if data.find('Invalid query or domain') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Phone:.*|E-mail:.*|)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Phone':
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'E-mail':
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Domain Nameservers([\s\S]*?)Your selected domain)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('Domain Nameservers') == -1 and line.find('Your selected domain') == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def de_manage(data, domain_whois):
    if data.find('free') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    pattern = re.compile(r'(Status:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    return domain_whois

def edu_manage(data, domain_whois):
    if data.find('No Match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Domain record activated:.*|Domain record last updated:.*|Domain expires:.*|)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Domain record activated':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain record last updated':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain expires':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Name Servers([\s\S]*?)Domain record activated)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('Name Servers') == -1 and line.find('Domain record activated') == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def eu_manage(data, domain_whois):
    if data.find('AVAILABLE') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern2 = re.compile(r'(Registrant([\s\S]*?)Technical)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Name:.*|Phone:.*|Email:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('Name') != -1:
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('Phone') != -1:
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('Email') != -1:
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    pattern2 = re.compile(r'(Registrar([\s\S]*?)Name servers)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Name:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('Name') != -1:
                domain_whois['sponsoring_registrar'] = match3.split(':')[1].strip()

    pattern2 = re.compile(r'(Name servers([\s\S]*?)Please visit)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('Name servers') == -1 and line.find('Please visit') == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def as_manage(data, domain_whois):
    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Registrant:\n.*|Registrar:\n.*|Registration status:\n.*|Registered on.*|Registry fee due on.*)')
    for match in pattern3.findall(data):
        if match.find("Registered on") != -1:
            domain_whois['creation_date'] = match.split('on',1)[1].strip()
        elif match.find('Registry fee due') != -1:
            domain_whois['expiration_date'] = match.split('on',1)[1].strip()
        elif match.split('\n',1)[0].find('Registrant') != -1:
            domain_whois['reg_name'] = match.split('\n',1)[1].strip()
        elif match.split('\n',1)[0].find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split('\n',1)[1].strip()
        elif match.split('\n',1)[0].find('Registration status') != -1:
            domain_status += match.split('\n',1)[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Name servers([\s\S]*?)WHOIS lookup made)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find("Name servers") == -1 and line.find("WHOIS lookup made") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def pl_manage(data, domain_whois):
    if data.find('No information available') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''
    domain_status = ''
    pattern = re.compile(r'(created:.*|last modified:.*|renewal date:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'last modified':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'renewal date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(nameservers([\s\S]*?)created)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('created') == -1:
                    if line.find('nameservers') != -1:
                        name_server += line.strip('nameservers:').strip()
                        name_server += ';'
                    else:
                        name_server += line.strip()
                        name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def tk_manage(data, domain_whois):
    # 两种格式？
    if data.find('Invalid query') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Domain registered:.*|Record will expire on:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain registered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Record will expire on':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Owner contact([\s\S]*?)Admin contact)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Organization:.*|Name:.*|E-mail:.*|Phone:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Organization':
                domain_whois['org_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'E-mail':
                domain_whois['reg_email'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match3.split(':', 1)[1].strip()
    pattern2 = re.compile(r'(Organisation([\s\S]*?)Domain Nameservers)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Organization:.*|Name:.*|E-mail:.*|Phone:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Organization':
                domain_whois['org_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'E-mail':
                domain_whois['reg_email'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match3.split(':', 1)[1].strip()

    pattern3 = re.compile(r'(Domain Nameservers([\s\S]*?)Domain registered)')
    for match3 in pattern3.findall(data):
        data3 = "".join(tuple(match3)[0])
        for line in data3.split('\n'):
            if line:
                if line.find("Domain Nameservers") == -1 and line.find("Domain registered") == -1:
                    name_server += line.strip()
                    name_server += ';'
    pattern3 = re.compile(r'(Domain Nameservers([\s\S]*?)Your selected domain name)')
    for match3 in pattern3.findall(data):
        data3 = "".join(tuple(match3)[0])
        for line in data3.split('\n'):
            if line:
                if line.find("Domain Nameservers") == -1 and line.find("Your selected domain name") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def uk_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Registrant:.*\n.*|Registrar:.*\n.*|Registration status:\n.*|Registered on.*|Registry fee due on.*)')
    for match in pattern3.findall(data):
        if match.find("Registered on") != -1:
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.find('Registry fee due') != -1:
            domain_whois['expiration_date'] = match.split('on',1)[1].strip()
        elif match.split('\n',1)[0].find('Registrant') != -1:
            domain_whois['reg_name'] = match.split('\n',1)[1].strip()
        elif match.split('\n',1)[0].find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split('\n',1)[1].strip()
        elif match.split('\n',1)[0].find('Registration status') != -1:
            domain_status += match.split('\n',1)[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Name servers([\s\S]*?)WHOIS lookup made)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find("Name servers") == -1 and line.find("WHOIS lookup made") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def uz_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Creation Date:.*|Expiration Date:.*|Status:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Domain servers in listed order([\s\S]*?)Administrative Contact)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('Domain servers in listed order') == -1 and \
                    line.find('Administrative Contact') == -1 and \
                     line.find('not.defined') == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def cf_manage(data, domain_whois):
    if data.find('is free') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Domain nameservers([\s\S]*?)Record maintained)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('Domain nameservers') == -1 and \
                    line.find('Record maintained') == -1 :
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def jp_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrant.*|Name Server.*|登録年月日.*|有効期限.*|\
|状態.*|Name.*|Email.*|電話番号.*|)')
    for match in pattern.findall(data):
        if match.find("状態") != -1:
            domain_status += match.split(']')[1].strip()
            domain_status += ';'
        elif match.find("Registrant") != -1:
            domain_whois['reg_name'] = match.split(']')[1].strip()
        elif match.find("登録年月日") != -1:
            domain_whois['creation_date'] = match.split(']')[1].strip()
        elif match.find("有効期限") != -1:
            domain_whois['expiration_date'] = match.split(']')[1].strip()
        elif match.find("Email") != -1:
            domain_whois['reg_email'] = match.split(']')[1].strip()
        elif match.find("電話番号") != -1:
            domain_whois['reg_phone'] = match.split(']')[1].strip()
        elif match.find("Name") != -1 and match.find("Name Server") == -1:
            domain_whois['org_name'] = match.split(']')[1].strip()
        elif match.find("Name Server") != -1:
            name_server += match.split(']')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def nu_manage(data, domain_whois):

    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(state:.*|holder:.*|created:.*|modified:.*|expires:.*|nserver:.*|registrar:.*| )')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'state':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'holder':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def nz_manage(data, domain_whois):

    if data.find('220 Available') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(query_status:.*|domain_dateregistered:.*|domain_datebilleduntil:.*|domain_datelastmodified:.*|\
registrar_name:.*|registrant_contact_name:.*|registrant_contact_phone:.*|registrant_contact_email:.*|ns_name.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registrar_name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'query_status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'registrant_contact_name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'domain_dateregistered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datebilleduntil':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datelastmodified':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_name':
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_phone':
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_email':
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.find("ns_name") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
