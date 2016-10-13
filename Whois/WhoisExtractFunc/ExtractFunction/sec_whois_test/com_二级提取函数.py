whois.godaddy.com  :  com1_manage
def com1_manage(data, domain_whois):
    if data.find('No match for') != -1 or\
       data.find('not found') != -1 or\
       data.find('NOT FOUND') != -1 or\
       data.find('Not found') != -1 or\
       data.find('NO DOMAIN') != -1 or\
       data.find('''can't be found''') != -1 or\
       data.find('NO MATCH FOR') != -1:
        domain_whois['status'] = 'NOTEXIST'
	return domain_whois
    if not data:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Updated Date:.*|Update Date:.*|Last updated Date:.*|Creation Date:.*|Registrar:.*|Domain Status:.*|Registrant Name:.*|Expiration Date:.*|Registry Expiry Date:.*|\
                            |Creation  Date:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Registrant Email :.*|Name Server:.*|Name server:.*|Registrar Registration Expiration Date:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Update Date' or \
             match.split(':')[0].strip() == 'Updated Date' or \
             match.split(':')[0].strip() == 'Last updated Date' :
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date' or \
             match.split(':')[0].strip() == 'Creation  Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Registration Expiration Date' or \
             match.split(':')[0].strip() == 'Expiration Date' or \
             match.split(':')[0].strip() == 'Registry Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server' or \
             match.split(':')[0].strip() == 'Name server':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.fastdomain.com  :  com1_manage
whois.wildwestdomains.com  : com1_manage
whois.bluerazor.com  :  com1_manage
whois.gomontenegrodomains.com  :  com1_manage
whois.do-reg.jp  :  jp_manage
def jp_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(.Status.*|.Nameserver.*|.Creation Date.*|.Expiration Date.*|.Last Update.*|Registrar.*\n.*)')
    for match in pattern.findall(data):
        if match.split(']')[0].strip().find('Status')!=-1:
            domain_status += match.split(']')[1].strip()
            domain_status += ';'
        elif match.split(']')[0].strip().find('Nameserver')!=-1:
            name_server += match.split(']')[1].strip()
            name_server += ';'
        elif match.split(']')[0].strip().find('Creation Date') != -1:
            domain_whois['creation_date'] = match.split(']')[1].strip()
        elif match.split(']')[0].strip().find('Expiration Date') != -1:
            domain_whois['expiration_date'] = match.split(']')[1].strip()
        elif match.split(']')[0].strip().find('Last Update') != -1:
            domain_whois['updated_date'] = match.split(']')[1].strip()
        elif match.split(']')[0].strip().find('Registrar') != -1:
            print match.split('\n')[1].strip()#只取[Registrar]后第一行信息
            domain_whois['sponsoring_registrar'] = match.split(']')[1].strip()

    pattern2 = re.compile(r'(Registrant([\s\S]*?)Admin Contact)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'        Name:.*')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match3.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.enetica.com.au  :  enetica_manage
def enetica_manage(data, domain_whois):
    if data.find('No match found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(  Name Server:.*|  Registrar of Record:.*|  Record last updated on.*|  Record created on.*|  Record expires on.*)')
    for match in pattern.findall(data):
        if match.split('on')[0].strip().find('Record created') != -1:
            domain_whois['creation_date'] = match.split('on', 1)[1].strip()
        elif match.split('on')[0].strip().find('Record expires') != -1:
            domain_whois['expiration_date'] = match.split('on', 1)[1].strip()
        elif match.split('on')[0].strip().find('Record last updated') != -1:
            domain_whois['updated_date'] = match.split('on', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar of Record':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':', 1)[1].strip()
            name_server += ';'

    pattern4 = re.compile(r'(Registrant Details:([\s\S]*?)Administrative Contact:)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(.*\+\d*\.\d*)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
                domain_whois['reg_phone'] = match5.strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.aitdomains.com  :  com1_manage
whois.misk.com  :  linuxaria.com #Your ip must have a reverse dns record ...
whois.ibi.net  :  ibi_manage
def ibi_manage(data, domain_whois):
    if data.find('01-Jan-1970 EDT') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(	Registrar :.*|	Record created on.*|	Record expires on.*|  Record created on.*|	Record last updated on.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Record created') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Record expires on') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Record last updated on') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()


    pattern2 = re.compile(r'(Domain Name Servers in listed order:([\s\S]*?)# KOREAN)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Domain Name Servers in listed order') == -1 and line.find('# KOREAN') == -1:
                name_server += line.strip()
                name_server += ';'

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
ewhois.sundns.com  :  com1_manage
whois.bookmyname.com  :  com1_manage
whois.goaustraliadomains.com  :  com1_manage
whois.ireg.net  :  com1_manage
whois.networking4all.com  :  networking4all_manage

def networking4all_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status.*|Updated date.*|Created date.*|Expiration date.*|Registration service provided by:.*\n.*\n.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Status') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip().find('Updated date') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Created date') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Expiration date') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('Registration service') != -1:
            domain_whois['sponsoring_registrar'] = match.split('\n')[2].strip()

    pattern2 = re.compile(r'(Domain nameservers:([\s\S]*?)Status)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Domain nameservers')==-1 and line.find('Status')==-1:
                name_server += line.strip()
                name_server += ';'
    pattern4 = re.compile(r'(Registrant([\s\S]*?)Administrative contact)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(    Name.*|    E-mail.*|    Phone.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip().find('Name') != -1:
                domain_whois['reg_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip().find('Phone') != -1:
                domain_whois['reg_phone'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip().find('E-mail') != -1:
                domain_whois['reg_email'] = match5.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.dotroll.com  :  dotroll_manage
def dotroll_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrar:.*|.*Status:.*|Record created:.*|Last updated:.*|Domain Expires:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('Status')!=-1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Record created':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Last updated':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain Expires':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Registrant([\s\S]*?)Administrative Contact)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'Company:.*|Name:.*|Phone:.*|Email:.*|')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Company':
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    pattern4 = re.compile(r'(Name servers:([\s\S]*?); Register your domain)')
    for match4 in pattern4.findall(data):
        for line in match4[0].split('\n'):
            if line and line.split(':')[0].find('Name servers:')==-1 and line.find('Register your domain')==-1:
                name_server += line.strip('Name servers:').strip()
                name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.ownidentity.com  :  ownidentity_manage
def ownidentity_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registration Date:.*|Expiration Date:.*|Name Server:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].strip() == 'Registration Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(registrant([\s\S]*?)admin_c)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Organization:.*|Phone Prefix:.*|Phone Number:.*|Email:.*|)')
        data2 = "".join(tuple(match2)[0])
        #合成电话号码
        phone_1 = ''
        phone_2 = ''
        phone = ''
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Phone Prefix':
                phone_1 += match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Organization':
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Phone Number':
                phone_2 += match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match3.split(':')[1].strip()
        phone += phone_1 + ' ' + phone_2
        if phone:
            domain_whois['reg_phone'] = phone

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.51web.hk  :  com1_manage
whois.serveisweb.com  :  serveisweb_manage
def serveisweb_manage(data, domain_whois):
    if data.find('Domain is not managed') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(query_status:.*|domain_dateregistered:.*|domain_datebilleduntil:.*|  registrant_contact_organization:.*|  registrant_contact_name:.*|\
                            |  registrant_contact_phone:.*|  registrant_contact_email:.*|Registrars.Registration Service Provided By:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'query_status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'domain_dateregistered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datebilleduntil':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrars.Registration Service Provided By':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_organization':
            domain_whois['org_name'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Domain servers in listed order([\s\S]*?)The data in this whois database)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.split(':')[0].find('Domain servers in listed order') == -1 and line.find('The data in this whois database') == -1:
                name_server += line.strip('Domain servers in listed order').strip()
                name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.ownregistrar.com  :  ownregistrar_manage
def ownregistrar_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'( Registrar :.*| Expiration Date:.*| Creation Date:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip()== 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip()== 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()


    pattern2 = re.compile(r'( Name Servers:([\s\S]*?)DNSSEC)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.split(':')[0].find('Name Servers') == -1 and line.find('DNSSEC') == -1:
                name_server += line.strip('Name Servers').strip()
                name_server += ';'

    pattern4 = re.compile(r'( Registrant Contact Details: ([\s\S]*?) Administrative Contact Details:)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'( Tel No.*| Email Address:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip().find('Tel No') != -1:
                domain_whois['reg_phone'] = match5.split('.',1)[1].strip()
            elif match5.split(':')[0].strip() == 'Email Address':
                domain_whois['reg_email'] = match5.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.ksdom.kr  :  com1_manage
whois.nayana.com  :  com1_manage
whois.gocanadadomains.com  :  com1_manage
whois.gofrancedomains.com  :  com1_manage
whois.gochinadomains.com  :  com1_manage
whois.allglobalnames.com  :  allglobalnames_manage
def allglobalnames_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(Registrar:.*|Owner Name:.*|Owner Phone:.*|Owner email:.*|\
                        |registration_date:.*|expiration_date:.*|nameserver.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Owner Name':
            domain_whois['reg_name'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Owner Phone':
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Owner email':
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registration_date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expiration_date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('nameserver') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
comnet-whois.humeia.com  :  com1_manage
whois.arcticnames.com  :  arcticnames_manage
def arcticnames_manage(data, domain_whois):
    if data.find('omain Not Found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(Registrar of Record:.*|Create Date:.*|Expiry Date:.*|Update Date:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Update Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Create Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar of Record':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Domain Name Servers([\s\S]*?)Registration Service Provider)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Domain Name Servers') == -1 and line.find('Registration Service Provider') == -1:
                name_server += line.strip()
                name_server += ';'

    pattern4 = re.compile(r'(Registrant:([\s\S]*?)Administrative Contact)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(	Voice:.*|	EMail:.*)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'EMail':
                domain_whois['reg_email'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Voice':
                domain_whois['reg_phone'] = match5.split('.',1)[1].strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.8hy.cn  :  com1_manage
whois.iana.org  :  iana_manage
def iana_manage(data, domain_whois):
    if data.find('domain:       COM') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    pattern = re.compile(r'(organisation:.*|created:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'organisation':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()

    return domain_whois 

whois.domains.domreg.lt  :  domreg_manage
def domreg_manage(data, domain_whois):
    if data.find('No records for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created:.*|Expiration:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Created':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()


    pattern2 = re.compile(r'(Nameservers([\s\S]*?)Registrant)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Nameservers') == -1 and line.find('Registrant') == -1:
                name_server += line.strip()
                name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.nordreg.com  : com1_manage
whois.chinanet.cc  :  chinanet_manage
def chinanet_manage(data, domain_whois):
    if data.find('no match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''
    
    pattern = re.compile(r'(Registrar:.*|Creation Date:.*|Expiration Date:.*|Name Server:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            for item in match.split(':')[1].strip().split(','):
                name_server += item
                name_server += ';'

    pattern2 = re.compile(r'(Registrant Contact:([\s\S]*?)Administrative Contact:)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(telephone:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('telephone') != -1:
                domain_whois['reg_phone'] = match3.split(':')[1].strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.rockenstein.de  :  com1_manage 
whois.afriregister.com  :  com1_manage 
whois.oiinternet.com.br  :  oiinternet_manage
def oiinternet_manage(data, domain_whois):
    if data.find('Nnot found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(registrar           :.*|registered_date     :.*|registerexpire_date :.*|changed             :.*|nameserver          :.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('registered_date') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('registerexpire_date') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('changed') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('nameserver') != -1:
            name_server += match.split(':', 1)[1].strip()
            name_server += ';'

    pattern4 = re.compile(r'(Registrant Contact Information([\s\S]*?)Billing Contact Information)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(name      :.*|phone     :.*|email     :.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip().find('name') != -1:
                domain_whois['reg_name'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip().find('phone') != -1:
                domain_whois['reg_phone'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip().find('email') != -1:
                domain_whois['reg_email'] = match5.split(':', 1)[1].strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.beartrapdomains.com  :  com1_manage 
whois.internetdomainnameregistrar.org  :internetdomainnameregistrar_manage
def internetdomainnameregistrar_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(changed:.*|registered:.*|expires:.*|nameserver:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'changed':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            for item in match.split(':')[1].strip().split(','):
                name_server += item
                name_server += ';'

    pattern2 = re.compile(r'(holder([\s\S]*?)admin_c)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(name:.*|phone:.*|email:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('phone') != -1:
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('name') != -1:
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('email') != -1:
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.domainprocessor.com  :  domainprocessor_manage
def domainprocessor_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'( Creation Date:.*| Expiration Date:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Creation Date') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Expiration Date') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'( Domain servers:([\s\S]*?)The Data in)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Domain servers') == -1 and line.find('The Data in') == -1:
                name_server += line.strip()
                name_server += ';'

    pattern4 = re.compile(r'(Registrant:([\s\S]*?) Domain name:)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(.*?@.*)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            for item in match5.split(' '):
                if item.find('@')!=-1:
                    domain_whois['reg_email'] = item

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.sunmounta.in  :  com1_manage 

whois.kudo.com  :  tadacip20.com  #[Errno -2] Name or service not known
whois.alices-registry.com  :  com1_manage 
whois.dagnabit.biz  :  com1_manage 
whois.domainnameroute.com  :  com1_manage 
whois.2imagen.net  :  #返回 #Please stop abusing this service.
whois.namebright.com  :  com1_manage 
whois.turbosite.com.br  :  turbosite_manage
def turbosite_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(Record expires on.*|Record created on.*|Database last updated on.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()

    pattern4 = re.compile(r'(Domain servers in listed order:([\s\S]*?)Registration Service Provider:)')
    for match4 in pattern4.findall(data):
        for line in match4[0].split('\n'):
            if line and line.find('Domain servers in listed order') == -1 and line.find('Registration Service Provider') == -1:
                name_server += line.strip()
                name_server += ';'

    pattern2 = re.compile(r'(Registration Service Provider:([\s\S]*?)Web:)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'Name:.*|')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Name':
                domain_whois['sponsoring_registrar'] = match3.split(':')[1].strip()

    pattern2 = re.compile(r'(Registrant:([\s\S]*?)Administrative Contact:)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'Registrant Email:.*|')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Registrant Email':
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.netdorm.com  :  com1_manage 
whois.sdsns.com  : sdsns_manage
sdsns_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(	Registrant Name :.*|	Registrant Phone :.*|	Registrant E-mail:.*|	Updated Date	:.*|\
                        |	Creation Date	:.*|	Expiration Date	:.*|	Name Server.*|	Registrar :.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Name Server') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois
whois.ilait.com  :  com1_manage
whois.namepanther.com  :  com1_manage
whois.badger.com  : com1_manage
whois.binero.se  :  binero_manage
def binero_manage(data, domain_whois):
    if data.find('does not exist') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(Created.*|Modified.*|Expires.*|Registrar.*|nameserver:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Created')!=-1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Modified') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Expires') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('nameserver') != -1:
            name_server += match.split(':', 1)[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(Owner-c:([\s\S]*)\n)Admin-c')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'Name.*|Organization.*|Phone.*|E-mail.*|')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('Name') != -1:
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('Organization') != -1:
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('Phone') != -1:
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('E-mail') != -1:
                domain_whois['reg_email'] = match3.split(':')[1].strip()


    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
whois.dotearth.com  :  com1_manage
whois.k8.com.br  :  #没找到域名
whois.asiaregister.com  :  com1_manage
whois.domainsinthebag.com  :  com1_manage
whois.maprilis.com.vn  :  maprilis_manage
def maprilis_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(Registrar:.*|Record expires on.*|Record created on.*|)')
    for match in pattern.findall(data):
        if match.split('on')[0].strip().find('Record created')!=-1:
            domain_whois['creation_date'] = match.split('on', 1)[1].strip()
        elif match.split('on')[0].strip().find('Record expires') != -1:
            domain_whois['expiration_date'] = match.split('on', 1)[1].strip()
        elif match.split(':')[0].strip().find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Registrant: ([\s\S]*)\n)Domain Name')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'Email:.*|Phone:.*|')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()

    pattern2 = re.compile(r'(Domain servers([\s\S]*?)DNSSEC)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Domain servers')==-1 and line.find('DNSSEC')==-1:
                name_server += line.strip()
                name_server += ';'

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
nswhois.domainregistry.com  :  com1_manage
whois.worldbizdomains.com  :  #总是time out
whois.portlandnames.com  :  com1_manage
whois.flancrestdomains.com  :  com1_manage
whois.interlakenames.com  :  com1_manage
whois.domainguardians.com  :  domainguardians_manage 
def domainguardians_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(Updated Date:.*|Creation Date:.*|Expiration Date:.*|nameserver:.*|Registrar:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    pattern2 = re.compile(r'(holder([\s\S]*?)admin_c)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'name:.*|phone:.*|email:.*|')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'email':
                domain_whois['reg_email'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'phone':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'name':
                domain_whois['reg_name'] = match3.split(':')[1].strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

whois.dynadot8.com  :  com1_manage
whois.naugus.com  :  #[Errno 111] Connection refused
whois.boterosolutions.net  :  com1_manage





