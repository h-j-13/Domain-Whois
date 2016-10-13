# /usr/bin/python
# encoding:utf8
# hj
# 2016.2.29

#NOTE
#Whois信息获取表结构

# | domain           | 域名名称
# | flag             | flag
# | ip               | 域名ip
# | top_whois_server | 顶级whois服务器
# | sec_whois_server | 二级whois服务器
# | reg_name         | 注册人姓名
# | reg_email        | 注册人联系邮箱
# | reg_phone        | 注册人联系电话
# | org_name         | 公司名称
# | creation_date    | 注册时间
# | expiration_date  | 到期时间
# | updated_date     | 更新时间
# | domain_details   | 域名whois详细信息
# | insert_time      | 插入时间
# | tld              | 后缀

        # "domain": "",                         # 域名
        # "flag": 0,                            # 状态标记
        # "status": "",                         # 域名状态
        # "sponsoring_registrar": "",           # 注册商
        # "top_whois_server": "",               # 顶级域名服务器
        # "sec_whois_server": "",               # 二级域名服务器
        # "reg_name": "",                       # 注册姓名
        # "reg_phone": "",                      # 注册电话
        # "reg_email": "",                      # 注册email
        # "org_name": "",                       # 注册公司名称
        # "creation_date": "",                  # 创建时间
        # "expiration_date": "",                # 到期时间
        # "updated_date": "",                   # 更新时间
        # "insert_time": "",                    # 信息插入时间
        # "details": "",                        # 细节
        # "name_server": "",                    # 域名服务器
        # "hash_value": 0,                      # 哈希值

import re

#>>>>>>tld    .ykp 没找到

def ykp_manage(domain_whois, data):
    pass

#==================================================================================================================

#>>>>>>tld    .ws
#addr   whois.website.ws
#Eg     topne.ws

# raw_data=
#   Domain Name: TOPNE.WS
#   Registry Domain ID: D865CD2BADEE835CE040010AAB015FFF
#   Registrar WHOIS Server: whois.registrygate.com
#   Registrar URL: http://registrygate.com/de/whois
#   Updated Date: 2015-12-26
#   Creation Date: 2008-12-26
#   Registrar Registration Expiration Date: 2016-12-26
#   Registrar: RegistryGate GmbH
#   Registrar IANA ID: 1328
#   Registrar Abuse Contact Email: registry@registrygate.com
#   Registrar Abuse Contact Phone: 498955061270
#   Domain Status: ok
#   Name Server: ns.ordergate.biz
#   Name Server: ns2.ordergate.biz
#   Name Server: ns3.ordergate.biz
#   DNSSEC: unsigned
#   URL of the ICANN WHOIS Data Problem Reporting System: http://wdprs.internic.net/
# >>> Last update of WHOIS database: 2016-03-01 <<<

def ws_manage(domain_whois, data):

    if data.find('No match') != -1:
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

# test_result:
# ---------------domain_whois-----------------
# domain:                       topne.ws
# status:                       30
# flag:                         112
# sponsoring_registrar:
# top_whois_server:             whois.registrygate.com
# sec_whois_server:
# reg_name:
# reg_phone:                    498955061270
# reg_email:                    registry@registrygate.com
# org_name:
# updated_date:                 2015-12-26
# creation_date:                2008-12-26
# expiration_date:              2016-12-26
# name_server:                  ns.ordergate.biz;ns2.ordergate.biz;ns3.ordergate.biz
# hash_value:                   2584376219419845143
# --------------------------------------------



#==================================================================================================================


#>>>>>>tld    .fr
#addr   whois.nic.yt
#Eg     transpole.fr

# raw_data=
# %%
# %% This is the AFNIC Whois server.
# %%
# %% complete date format : DD/MM/YYYY
# %% short date format    : DD/MM
# %% version              : FRNIC-2.5
# %%
# %% Rights restricted by copyright.
# %% See http://www.afnic.fr/afnic/web/mentions-legales-whois_en
# %%
# %% Use '-h' option to obtain more information about this service.
# %%
# %% [202.102.144.11 REQUEST] >> transpole.fr
# %%
# %% RL Net [##########] - RL IP [#########.]
# %%
#
# domain:      transpole.fr
# status:      ACTIVE
# hold:        NO
# holder-c:    KL2267-FRNIC
# admin-c:     KL2267-FRNIC
# tech-c:      NAC7-FRNIC
# zone-c:      NFC1-FRNIC
# nsl-id:      NSL1431-FRNIC
# registrar:   AXINET COMMUNICATION
# Expiry Date: 28/05/2016
# created:     15/12/1997
# last-update: 28/05/2015
# source:      FRNIC
#
# ns-list:     NSL1431-FRNIC
# nserver:     ns1.axinet.fr [62.73.4.5]
# nserver:     ns2.axinet.fr [62.73.4.6]
# source:      FRNIC
#
# registrar:   AXINET COMMUNICATION
# type:        Isp Option 1
# address:     34 Avenue de l'Europe
# address:     Immeuble Le Trident - Bâtiment A
# address:     GRENOBLE
# country:     FR
# phone:       +33 4 56 38 15 15
# fax-no:      +33 4 56 38 15 16
# e-mail:      info@axinet.com
# website:     http://www.axinet.fr
# anonymous:   NO
# registered:  01/04/1999
# source:      FRNIC
#
# nic-hdl:     KL2267-FRNIC
# type:        ORGANIZATION
# contact:     KEOLIS LILLE
# address:     KEOLIS LILLE
# address:     276, avenue de la Marne
# address:     59700 Marcq en Baroeul
# country:     FR
# phone:       +33 3 20 81 43 96
# e-mail:      francois.chassignet@keolis-lille.fr
# registrar:   AXINET COMMUNICATION
# changed:     30/12/2015 nic@nic.fr
# anonymous:   NO
# obsoleted:   NO
# eligstatus:  ok
# eligsource:  REGISTRAR
# eligdate:    18/03/2015 14:26:04
# reachmedia:  phone
# reachstatus: ok
# reachsource: REGISTRAR
# reachdate:   18/03/2015 14:26:04
# source:      FRNIC
#
# nic-hdl:     NAC7-FRNIC
# type:        ROLE
# contact:     NOC Axinet Communication
# address:     AXINET COMMUNICATION
# address:     34, avenue de l'Europe
# address:     immeuble le Trident
# address:     38100 Grenoble
# country:     FR
# phone:       +33 4 56 38 15 15
# e-mail:      supportfr@axinet.com
# trouble:     www.axinet.com
# admin-c:     MB4675-FRNIC
# tech-c:      LC185-FRNIC
# notify:      supportfr@axinet.com
# registrar:   AXINET COMMUNICATION
# changed:     10/10/2008 supportfr@axinet.com
# anonymous:   NO
# obsoleted:   NO
# source:      FRNIC


def fr_manage(domain_whois, data):

    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|registrar:.*|Expiry Date:.*|created:.*|\
last-update:.*|phone:.*|e-mail:.*|nserver:.*)')


    for match in pattern.findall(data):
        if match.find('status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('nserver:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('last-update:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('created:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('Expiry Date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()

        elif match.find('registrar:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()

        elif match.find('e-mail:') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()

        elif match.find('phone:') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

# test_resut=
# domain:                       transpole.fr
# status:                       30
# flag:                         112
# sponsoring_registrar:
# top_whois_server:             whois.nic.yt
# sec_whois_server:
# reg_name:                     AXINET COMMUNICATION
# reg_phone:                    +33 4 56 38 15 15
# reg_email:                    supportfr@axinet.com
# org_name:
# updated_date:                 28/05/2015
# creation_date:                15/12/1997
# expiration_date:              28/05/2016
# name_server:                  ns1.axinet.fr [62.73.4.5];ns2.axinet.fr [62.73.4.6]
# hash_value:                   -6368378822603386753



#==================================================================================================================


#>>>>>>tld    .wf
#addr   whois.nic.wf
#Eg     nox.wf

# raw_data=
# %%
# %% This is the AFNIC Whois server.
# %%
# %% complete date format : DD/MM/YYYY
# %% short date format    : DD/MM
# %% version              : FRNIC-2.5
# %%
# %% Rights restricted by copyright.
# %% See http://www.afnic.fr/afnic/web/mentions-legales-whois_en
# %%
# %% Use '-h' option to obtain more information about this service.
# %%
# %% [202.102.144.11 REQUEST] >> nox.wf
# %%
# %% RL Net [##########] - RL IP [#########.]
# %%
#
# domain:      nox.wf
# status:      ACTIVE
# hold:        NO
# holder-c:    ANO00-FRNIC
# admin-c:     OVH5-FRNIC
# tech-c:      OVH5-FRNIC
# zone-c:      NFC1-FRNIC
# nsl-id:      NSL87589-FRNIC
# registrar:   OVH
# Expiry Date: 20/07/2016
# created:     20/07/2013
# last-update: 09/07/2015
# source:      FRNIC
#
# ns-list:     NSL87589-FRNIC
# nserver:     ks390846.kimsufi.com
# nserver:     ns.kimsufi.com
# source:      FRNIC
#
# registrar:   OVH
# type:        Isp Option 1
# address:     2 Rue Kellermann
# address:     ROUBAIX
# country:     FR
# phone:       +33 8 99 70 17 61
# fax-no:      +33 3 20 20 09 58
# e-mail:      support@ovh.net
# website:     http://www.ovh.com
# anonymous:   NO
# registered:  21/10/1999
# source:      FRNIC
#
# nic-hdl:     OVH5-FRNIC
# type:        ROLE
# contact:     OVH NET
# address:     OVH
# address:     140, quai du Sartel
# address:     59100 Roubaix
# country:     FR
# phone:       +33 8 99 70 17 61
# e-mail:      tech@ovh.net
# trouble:     Information: http://www.ovh.fr
# trouble:     Questions:  mailto:tech@ovh.net
# trouble:     Spam: mailto:abuse@ovh.net
# admin-c:     OK217-FRNIC
# tech-c:      OK217-FRNIC
# notify:      tech@ovh.net
# registrar:   OVH
# changed:     11/10/2006 tech@ovh.net
# anonymous:   NO
# obsoleted:   NO
# source:      FRNIC
#
# nic-hdl:     ANO00-FRNIC
# type:        PERSON
# contact:     Ano Nymous
# remarks:     -------------- WARNING --------------
# remarks:     While the registrar knows him/her,
# remarks:     this person chose to restrict access
# remarks:     to his/her personal data. So PLEASE,
# remarks:     don't send emails to Ano Nymous. This
# remarks:     address is bogus and there is no hope
# remarks:     of a reply.
# remarks:     -------------- WARNING --------------
# registrar:   OVH
# changed:     20/07/2013 anonymous@anonymous
# anonymous:   YES
# obsoleted:   NO
# eligstatus:  ok
# eligdate:    20/07/2013 13:11:36
# source:      FRNIC


def fr_manage(domain_whois, data):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|registrar:.*|Expiry Date:.*|created:.*|\
last-update:.*|phone:.*|e-mail:.*|nserver:.*)')


    for match in pattern.findall(data):
        if match.find('status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('nserver:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('last-update:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('created:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('Expiry Date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()

        elif match.find('registrar:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()

        elif match.find('e-mail:') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()

        elif match.find('phone:') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois
# result=
# domain:                       nox.wf
# status:                       30
# flag:                         112
# sponsoring_registrar:
# top_whois_server:             whois.nic.wf
# sec_whois_server:
# reg_name:                     OVH
# reg_phone:                    +33 8 99 70 17 61
# reg_email:                    tech@ovh.net
# org_name:
# updated_date:                 09/07/2015
# creation_date:                20/07/2013
# expiration_date:              20/07/2016
# name_server:                  ks390846.kimsufi.com;ns.kimsufi.com
# hash_value:                   2879732878107958847


#==================================================================================================================

#>>>>>>tld    .vu
#addr   vunic.vu
#Eg     de.vu

# raw_data=
# #
# # -- /usr/local/bin/mywhois --
# #
# First Name:     Domain
# Last Name:      Administration
# Adress:          Marius Strasser  P.O. Box 51
# City:            Nea Michaniona
# Country:         Greece
# Date Created:   Thu Jun 2012 10:04:14
# Expiry date:    Thu Jun 2018 22:04:14
# DNS servers1:    ns1.idnscan.net : 88.198.56.226
# DNS servers2:    ns6.idnscan.net : 80.190.246.106

def vu_manage(domain_whois, data):

    if data.find('is not valid') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Date Created:.*|Expiry date:.*|DNS servers1:.*|DNS servers2:.*)')


    for match in pattern.findall(data):
        if match.find('status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('DNS servers1:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.find('DNS servers2:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.find('DNS servers3:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('Date Created:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('Expiry date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

# result=
# domain:                       de.vu
# status:                       30
# flag:                         101
# sponsoring_registrar:
# top_whois_server:             vunic.vu
# sec_whois_server:
# reg_name:
# reg_phone:
# reg_email:
# org_name:
# updated_date:
# creation_date:                Thu Jun 2012 10
# expiration_date:              Thu Jun 2018 22
# name_server:                  ns6.idnscan.net;ns1.idnscan.net
# hash_value:                   -3195753719091573556


#==================================================================================================================


#>>>>>>tld    .vg
#addr   whois.nic.vg
#Eg     cc.vg

# raw_data=
# ...
# domain name: CC.VG
# registrar: OVH
# url: www.ovh.com
# status: clienttransferprohibited
# status: clientdeleteprohibited
# created date: 2014-07-03 09:20:08
# updated date: 2016-01-27 09:18:47
# expiration date: 2017-07-03 09:20:08
#
# owner-contact: P-JPT33
# owner-name: Jose Antonio Priego Torres
# owner-street: Andujar 10 3A
# owner-city: Huetor Vega
# owner-state: Granada
# owner-zip: 18198
# owner-country: ES
# owner-phone: +34.644357374
# owner-email: prekillo@gmail.com
#
# admin-contact: P-JPT33
# admin-name: Jose Antonio Priego Torres
# admin-street: Andujar 10 3A
# admin-city: Huetor Vega
# admin-state: Granada
# admin-zip: 18198
# admin-country: ES
# admin-phone: +34.644357374
# admin-email: prekillo@gmail.com
#
# tech-contact: P-JPT33
# tech-name: Jose Antonio Priego Torres
# tech-street: Andujar 10 3A
# tech-city: Huetor Vega
# tech-state: Granada
# tech-zip: 18198
# tech-country: ES
# tech-phone: +34.644357374
# tech-email: prekillo@gmail.com
#
# billing-contact: P-JPT33
# billing-name: Jose Antonio Priego Torres
# billing-street: Andujar 10 3A
# billing-city: Huetor Vega
# billing-state: Granada
# billing-zip: 18198
# billing-country: ES
# billing-phone: +34.644357374
# billing-email: prekillo@gmail.com
#
# nameserver: ns1.nazuka.net
# nameserver: ns2.nazuka.net
# nameserver: ns3.nazuka.net
# nameserver: ns4.nazuka.net

def vg_manage(domain_whois, data):
    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrar:.*|status:.*|created date:.*|updated date:.*|\
expiration date:.*|owner-name:.*|phone:.*|email:.*|nameserver:.*)')


    for match in pattern.findall(data):
        if match.find('status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('nameserver:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('updated date:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

        elif match.find('created date:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('expiration date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()

        elif match.find('owner-name:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()

        elif match.find('email:') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()

        elif match.find('phone:') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

# result=
# domain:                       cc.vg
# status:                       30
# flag:                         112
# sponsoring_registrar:         OVH
# top_whois_server:             whois.nic.vg
# sec_whois_server:
# reg_name:                     Jose Antonio Priego Torres
# reg_phone:                    +34.644357374
# reg_email:                    prekillo@gmail.com
# org_name:
# updated_date:                 2016-01-27 09
# creation_date:                2014-07-03 09
# expiration_date:              2017-07-03 09
# name_server:                  ns1.nazuka.net;ns2.nazuka.net;ns3.nazuka.net;ns4.nazuka.net
# hash_value:                   -9065637074899635889

#==================================================================================================================

#>>>>>>tld    .ve
#addr   whois.nic.ve
#Eg     gob.ve

raw_data=
# Servidor Whois del Centro de Información de Red de Venezuela (NIC.VE)
#
# Este servidor contiene información autoritativa exclusivamente de dominios .VE
# Cualquier consulta sobre este servicio, puede hacerla al correo electrónico whois@nic.ve
#
# Titular:
# Universidad de los Andes		dtes@ula.ve
#    Universidad de Los Andes
#    Av. 3 Independencia, entre calles 23 y 24, Edificio del Rectorado
#    Mérida, Mérida  VE
#    0274 2401124, 2402311, 2402350, 2401111 (FAX)
#
#    Nombre de Dominio: ula.ve
#
#    Contacto Administrativo:
#       Leonardo González Villasmil		dtes@ula.ve
#       Universidad de Los Andes
#       Av. 3 Independencia, entre calles 23 y 24, Edificio del Rectorado
#       Mérida, Mérida  VE
#       0274 2401124 (FAX)
#
#    Contacto Técnico:
#       Juan Luis Chaves		dtes@ula.ve
#       Universidad de Los Andes
#       Av. 3 Independencia, entre calles 23 y 24, Edificio del Rectorado
#       Mérida, Mérida  VE
#       0274 2403944 (FAX)
#
#    Contacto de Cobranza:
#       Karina Pabón		dtes@ula.ve
#       Universidad de Los Andes
#       Av. 3 Independencia, entre calles 23 y 24, Edificio del Rectorado
#       Mérida, Mérida  VE
#       0274 2401124 (FAX)
#
#    Ultima Actualización: 2015-08-10 15:24:46
#    Fecha de Creación: 2005-11-15 14:40:48
#
#    Estatus del dominio: ACTIVO
#
#    Servidor(es) de Nombres de Dominio:
#
#    - avalon.ula.ve
#    - azmodan.ula.ve
#
# NIC-Venezuela - CONATEL

def ve_manage(domain_whois, data):
    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Titular:.*|Estatus del dominio.*|Fecha de Creación.*|Ultima Actualización:.*|\
|Mérida, Mérida  VE.*||Servidor(es) de Nombres de Dominio:.*)')


    for match in pattern.findall(data):
        if match.find('Estatus del dominio:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('Servidor(es) de Nombres de Dominio:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('Ultima Actualización:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('Fecha de Creación') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('Titular:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()

        elif match.find('Administrative Contac') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()

        elif match.find('Mérida, Mérida  VE') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

#==================================================================================================================

#>>>>>>tld    .vc
#addr   whois2.afilias-grs.net
#Eg     zz.vc

# raw_data=

# Access to CCTLD WHOIS information is provided to assist persons in
# determining the contents of a domain name registration record in the
# Afilias registry database. The data in this record is provided by
# Afilias Limited for informational purposes only, and Afilias does not
# guarantee its accuracy.  This service is intended only for query-based
# access. You agree that you will use this data only for lawful purposes
# and that, under no circumstances will you use this data to: (a) allow,
# enable, or otherwise support the transmission by e-mail, telephone, or
# facsimile of mass unsolicited, commercial advertising or solicitations
# to entities other than the data recipient's own existing customers; or
# (b) enable high volume, automated, electronic processes that send
# queries or data to the systems of Registry Operator, a Registrar, or
# Afilias except as reasonably necessary to register domain names or
# modify existing registrations. All rights reserved. Afilias reserves
# the right to modify these terms at any time. By submitting this query,
# you agree to abide by this policy.
#
# Domain ID:D1625734-LRCC
# Domain Name:ZZ.VC
# Created On:19-Apr-2010 00:49:51 UTC
# Last Updated On:08-Apr-2015 17:39:18 UTC
# Expiration Date:19-Apr-2018 00:49:51 UTC
# Sponsoring Registrar:Tucows Inc. (R63-LRCC)
# Status:OK
# Registrant ID:tuKOp8p74O6i7A4L
# Registrant Name:Hostinger Hostmaster
# Registrant Organization:Hostinger International Ltd.
# Registrant Street1:61 Lordou Vyronos
# Registrant Street2:
# Registrant Street3:
# Registrant City:Larnaca
# Registrant State/Province:Larnaca
# Registrant Postal Code:6023
# Registrant Country:CY
# Registrant Phone:+357.24030130
# Registrant Phone Ext.:
# Registrant FAX:
# Registrant FAX Ext.:
# Registrant Email:clients@hostinger.com
# Admin ID:tuRQUbp3AR10sRHb
# Admin Name:Hostinger Hostmaster
# Admin Organization:Hostinger International Ltd.
# Admin Street1:61 Lordou Vyronos
# Admin Street2:
# Admin Street3:
# Admin City:Larnaca
# Admin State/Province:Larnaca
# Admin Postal Code:6023
# Admin Country:CY
# Admin Phone:+357.24030130
# Admin Phone Ext.:
# Admin FAX:
# Admin FAX Ext.:
# Admin Email:clients@hostinger.com
# Billing ID:tu0w5H0GJegTrd9v
# Billing Name:Hostinger Hostmaster
# Billing Organization:Hostinger International Ltd.
# Billing Street1:61 Lordou Vyronos
# Billing Street2:
# Billing Street3:
# Billing City:Larnaca
# Billing State/Province:Larnaca
# Billing Postal Code:6023
# Billing Country:CY
# Billing Phone:+357.24030130
# Billing Phone Ext.:
# Billing FAX:
# Billing FAX Ext.:
# Billing Email:clients@hostinger.com
# Tech ID:tuB5Roi1zZcGbwC0
# Tech Name:Hostinger Hostmaster
# Tech Organization:Hostinger International Ltd.
# Tech Street1:61 Lordou Vyronos
# Tech Street2:
# Tech Street3:
# Tech City:Larnaca
# Tech State/Province:Larnaca
# Tech Postal Code:6023
# Tech Country:CY
# Tech Phone:+357.24030130
# Tech Phone Ext.:
# Tech FAX:
# Tech FAX Ext.:
# Tech Email:abuse@main-hosting.com
# Name Server:NS1.HOSTINGER.COM
# Name Server:NS2.HOSTINGER.COM
# Name Server:NS3.HOSTINGER.COM
# Name Server:
# Name Server:
# Name Server:
# Name Server:
# Name Server:
# Name Server:
# Name Server:
# Name Server:
# Name Server:
# Name Server:

def vc_manage(domain_whois, data):
    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created On:.*|Last Updated On:.*|Expiration Date:.*|Sponsoring Registrar:.*|\
|Status:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone:.*|Registrant Email:.*|Name Server:.*)')


    for match in pattern.findall(data):
        if match.find('Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('Last Updated On:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('Created On:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('Expiration Date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()

        elif match.find('Sponsoring Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

        elif match.find('Registrant Name:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()

        elif match.find('Registrant Organization:') != -1:
            domain_whois['org_name'] = match.split(':', 1)[1].strip()

        elif match.find('Registrant Email:') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()

        elif match.find('Registrant Phone:') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

# result=
# domain:                       zz.vc
# status:                       30
# flag:                         122
# sponsoring_registrar:         Tucows Inc. (R63-LRCC)
# top_whois_server:             whois2.afilias-grs.net
# sec_whois_server:
# reg_name:                     Hostinger Hostmaster
# reg_phone:                    +357.24030130
# reg_email:                    clients@hostinger.com
# org_name:                     Hostinger International Ltd.
# updated_date:                 08-Apr-2015 17
# creation_date:                19-Apr-2010 00
# expiration_date:              19-Apr-2018 00
# name_server:                  NS1.HOSTINGER.COM;NS2.HOSTINGER.COM;NS3.HOSTINGER.COM
# hash_value:                   -610202059776859055

#==================================================================================================================

#>>>>>>tld    .uz
#addr   whois.cctld.uz
#Eg     westmotor.uz

# raw_data=

# % UzWhois Server Version 1.0
#
# % Domain names in the .uz domain can now be registered
# % with many different competing registrars. Go to http://www.cctld.uz/
# % for detailed information.
#
#    Domain Name: WESTMOTOR.UZ
#    Registrar: BCC
#    Whois Server: www.whois.uz
#    Referral URL: http://www.cctld.uz/
#    Name Server: dns1.webspace.uz. 46.8.35.129
#    Name Server: dns2.webspace.uz. 46.8.35.130
#    Name Server: dns3.webspace.uz. 94.20.20.155
#    Name Server: not.defined. not.defined.
#    Status: ACTIVE
#    Updated Date: 19-aug-2013
#    Creation Date: 14-Dec-2012
#    Expiration Date: 14-dec-2018
#
#
# % >>> Last update of whois database: Sun, 06 Mar 2016 13:58:44 +0500 <<<
#
# % NOTICE: The expiration date displayed in this record is the date the
# % registrar's sponsorship of the domain name registration in the registry is
# % currently set to expire. This date does not necessarily reflect the expiration
# % date of the domain name registrant's agreement with the sponsoring
# % registrar.  Users may consult the sponsoring registrar's Whois database to
# % view the registrar's reported date of expiration for this registration.
#
# % TERMS OF USE: You are not authorized to access or query our Whois
# % database through the use of electronic processes that are high-volume and
# % automated except as reasonably necessary to register domain names or
# % modify existing registrations; the Data in Center UZINFOCOM ccTLD.uz
# % Services ( Center UZINFOCOM ) Whois database is provided by Center UZINFOCOM for
# % information purposes only, and to assist persons in obtaining information
# % about or related to a domain name registration record. Center UZINFOCOM does not
# % guarantee its accuracy. By submitting a Whois query, you agree to abide
# % by the following terms of use: You agree that you may use this Data only
# % for lawful purposes and that under no circumstances will you use this Data
# % to: (1) allow, enable, or otherwise support the transmission of mass
# % unsolicited, commercial advertising or solicitations via e-mail, telephone,
# % or facsimile; or (2) enable high volume, automated, electronic processes
# % that apply to Center UZINFOCOM (or its computer systems). The compilation,
# % repackaging, dissemination or other use of this Data is expressly
# % prohibited without the prior written consent of Center UZINFOCOM. You agree not to
# % use electronic processes that are automated and high-volume to access or
# % query the Whois database except as reasonably necessary to register
# % domain names or modify existing registrations. Center UZINFOCOM reserves the right
# % to restrict your access to the Whois database in its sole discretion to ensure
# % operational stability. Center UZINFOCOM may restrict or terminate your access to the
# % Whois database for failure to abide by these terms of use. Center UZINFOCOM
# % reserves the right to modify these terms at any time.
#
# % The Registry database contains ONLY .UZ domains and
# % Registrars.
#
# % Registration Service Provided By: BCC
#
# Domain Name: WESTMOTOR.UZ
#
# Registrant:
#     not.defined.
#     	(abdullaev.murad [at] gmail.com)
#
#
#     , 100015
#     uz
#     Tel. (+998 90) 167-88-167-88-84
#     Fax.
#
# Creation Date: 14-Dec-2012
# Expiration Date: 14-dec-2018
#
# Domain servers in listed order:
#     dns1.webspace.uz.
#     dns2.webspace.uz.
#     dns3.webspace.uz.
#     not.defined.
#
#
# Administrative Contact:
#     not.defined.
#     not.defined.	(abdullaev.murad [at] gmail.com)
#     not.defined.
#     not.defined.
#     not.defined., 100015
#     uz
#     Tel. (+998 90) 167-88-167-88-84
#     Fax. not.defined.
#
# Technical Contact:
#     not.defined.
#     not.defined.	(abdullaev.murad [at] gmail.com)
#     not.defined.
#     not.defined.
#     not.defined., 100015
#     uz
#     Tel. (+998 90) 167-88-167-88-84
#     Fax. not.defined.
#
# Billing Contact:
#     not.defined.
#     not.defined.	(abdullaev.murad [at] gmail.com)
#     not.defined.
#     not.defined.
#     not.defined., 100015
#     uz
#     Tel. (+998 90) 167-88-167-88-84
#     Fax. not.defined.
#
# Status: ACTIVE
#
# % The data in this whois database is provided to you for informationpurposes only, that is, to assist you in obtaining
# % information about or related to a domain name registration record. We make this informationavailable "as is", and do
# % not guarantee its accuracy. By submitting awhois query, you agree that you will use this data only for lawfulpurposes
# % and that, under no circumstances will you use this data to:(1) enable high volume, automated, electronic processes
# % that stress orload this whois database system providing you this information; or(2) allow,  enable, or otherwise
# % support the transmission of massunsolicited,  commercial advertising or solicitations via direct mail,electronic mail,
# % or by telephone. The compilation, repackaging,dissemination or other use of this data is expressly prohibited withoutprior
# % written consent from us. The registrar of record is Critical Internet, Inc.. We reserve the right to modifythese terms at
# % any time. By submitting this query, you agree to abideby these terms.
#
#
# %  The Whois Server (ver. 1.0) of ccTLD.UZ
# %  (c) 2005, Center UZINFOCOM

def uz_manage(domain_whois, data):
    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrar:.*|Name Server:.*|Status:.*|Updated Date:.*|\
|Creation Date:.*|Expiration Date:.*| Tel.*|)')


    for match in pattern.findall(data):
        if match.find('Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('Updated Date:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('Creation Date:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('Expiration Date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()

        elif match.find('Registrar:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()

        elif match.find('Tel') != -1:
            domain_whois['reg_phone'] = match.split('.', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

# result=
# domain:                       westmotor.uz
# status:                       30
# flag:                         112
# sponsoring_registrar:
# top_whois_server:             whois.cctld.uz
# sec_whois_server:
# reg_name:                     BCC
# reg_phone:                    (+998 90) 167-88-167-88-84
# reg_email:
# org_name:
# updated_date:                 19-aug-2013
# creation_date:                14-Dec-2012
# expiration_date:              14-dec-2018
# name_server:                  dns1.webspace.uz. 46.8.35.129;dns2.webspace.uz. 46.8.35.130;dns3.webspace.uz. 94.20.20.155;not.defined. not.defined.
# hash_value:                   -581056328429563121

#==================================================================================================================

#>>>>>>tld    .uy
#addr   whois.nic.org.uy
#Eg     gub.uy

def uy_manage(domain_whois, data):
    pass

    #返回的信息是法语 暂时未写


#==================================================================================================================

#>>>>>>tld    .us
#addr   whois.nic.us
#Eg     nd.us

# raw_data=
# Domain Name:                                 ND.US
# Domain ID:                                   D658443-US
# Sponsoring Registrar:                        US LOCALITY
# Registrar URL (registration services):       www.whois.us
# Domain Status:                               serverDeleteProhibited
# Domain Status:                               serverHold
# Domain Status:                               serverTransferProhibited
# Domain Status:                               serverUpdateProhibited
# Domain Status:                               inactive
# Variant:                                     ND.US
# Registrant ID:                               NEUSTAR-US
# Registrant Name:                             NEUSTAR
# Registrant Organization:                     NEUSTAR
# Registrant Address1:                         Loudoun Tech Center
# Registrant Address2:                         45980 Center Oak Plaza
# Registrant City:                             Sterling
# Registrant State/Province:                   VA
# Registrant Postal Code:                      20166
# Registrant Country:                          United States
# Registrant Country Code:                     US
# Registrant Phone Number:                     +1.5714345728
# Registrant Facsimile Number:                 +1.5714345758
# Registrant Email:                            support.us@neustar.us
# Registrant Application Purpose:              P5
# Registrant Nexus Category:                   C21
# Administrative Contact ID:                   NEUSTAR-US
# Administrative Contact Name:                 NEUSTAR
# Administrative Contact Organization:         NEUSTAR
# Administrative Contact Address1:             Loudoun Tech Center
# Administrative Contact Address2:             45980 Center Oak Plaza
# Administrative Contact City:                 Sterling
# Administrative Contact State/Province:       VA
# Administrative Contact Postal Code:          20166
# Administrative Contact Country:              United States
# Administrative Contact Country Code:         US
# Administrative Contact Phone Number:         +1.5714345728
# Administrative Contact Facsimile Number:     +1.5714345758
# Administrative Contact Email:                support.us@neustar.us
# Administrative Application Purpose:          P5
# Administrative Nexus Category:               C21
# Billing Contact ID:                          NEUSTAR-US
# Billing Contact Name:                        NEUSTAR
# Billing Contact Organization:                NEUSTAR
# Billing Contact Address1:                    Loudoun Tech Center
# Billing Contact Address2:                    45980 Center Oak Plaza
# Billing Contact City:                        Sterling
# Billing Contact State/Province:              VA
# Billing Contact Postal Code:                 20166
# Billing Contact Country:                     United States
# Billing Contact Country Code:                US
# Billing Contact Phone Number:                +1.5714345728
# Billing Contact Facsimile Number:            +1.5714345758
# Billing Contact Email:                       support.us@neustar.us
# Billing Application Purpose:                 P5
# Billing Nexus Category:                      C21
# Technical Contact ID:                        NEUSTAR-US
# Technical Contact Name:                      NEUSTAR
# Technical Contact Organization:              NEUSTAR
# Technical Contact Address1:                  Loudoun Tech Center
# Technical Contact Address2:                  45980 Center Oak Plaza
# Technical Contact City:                      Sterling
# Technical Contact State/Province:            VA
# Technical Contact Postal Code:               20166
# Technical Contact Country:                   United States
# Technical Contact Country Code:              US
# Technical Contact Phone Number:              +1.5714345728
# Technical Contact Facsimile Number:          +1.5714345758
# Technical Contact Email:                     support.us@neustar.us
# Technical Application Purpose:               P5
# Technical Nexus Category:                    C21
# Created by Registrar:                        REGISTRY REGISTRAR
# Last Updated by Registrar:                   NEULEVELCSR
# Last Transferred Date:                       Thu Feb 20 23:46:05 GMT 2003
# Domain Registration Date:                    Thu Apr 18 16:37:47 GMT 2002
# Domain Expiration Date:                      Tue Apr 17 23:59:59 GMT 2018
# Domain Last Updated Date:                    Wed Dec 31 13:26:29 GMT 2014
# DNSSEC:                                      false

def us_manage(domain_whois, data):
    if data.find('Not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Phone Number:.*|\
|Registrant Email:.*|Created by Registrar:.*| Registration Date:.*|Expiration Date:.*|Last Updated Date:.*|Email:.*|Email:.*|Email:.*)')


    for match in pattern.findall(data):
        if match.find('Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('Updated Date:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('Creation Date:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('Expiration Date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()

        elif match.find('Registrar:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()

        elif match.find('Tel') != -1:
            domain_whois['reg_phone'] = match.split('.', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

#==================================================================================================================

#>>>>>>tld    .ug
#addr   whois.co.ug
#Eg     go.ug

#查询总是超时


#==================================================================================================================

#>>>>>>tld    .ua
#addr   whois.ua
#Eg     te.ua

# raw_data=
# % request from 221.2.164.39
# % This is the Ukrainian Whois query server #I.
# % The Whois is subject to Terms of use
# % See https://hostmaster.ua/services/
# %
#
# % % .UA whois
# % Domain Record:
# % =============
# domain:     te.ua
# admin-c:    UADM22-UANIC
# tech-c:     UT45-UANIC
# dom-public: YES
# nserver:    ns.te.ua
# nserver:    ns2.uar.net
# nserver:    nix.ns.ua
# nserver:    ns2.km.ua
# nserver:    ns.dn.ua
# remark:     Ternopil region
# created:    0-UANIC 19970216000000
# changed:    UT45-UANIC 20150518
# source:     UANIC
#
# % Glue Record:
# % ===========
# nserver:    ns.te.ua
# ip-addr:    193.108.170.1
# ipv6-addr:  2001:67c:29e0::15
#
# % Administrative Contact:
# % ======================
# nic-handle:     UADM22-UANIC
# organization:   АДМІНІСТРАЦІЯ TERNOPIL.UA
# address:        Not Available
# e-mail:         ROMAN@BIT.TE.UA
# org-id:         N/A
# mnt-by:         NONE
# changed:        UADM22-UANIC 20040304140005
# source:         UANIC
#
# % Technical Contact:
# % =================
# nic-handle:     UT45-UANIC
# organization:   ТОВ "Юнітрейд Про"
# address:        Миколайчука, 3
# address:        58000 ЧЕРНІВЦІ
# address:        UA
# phone:          +380 (37) 2585637
# e-mail:         vit@sacura.net
# org-id:         N/A
# mnt-by:         NONE
# changed:        UT45-UANIC 20121121114323
# source:         UANIC
#
# % % .UA whois
#
#
#
#
# % Query time:     0 msec

def ua_manage(domain_whois, data):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(nserver:.*|created:.*|changed:.*|e-mail:.*|organization:.*)')


    for match in pattern.findall(data):

        if match.find('nserver:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

        elif match.find('changed:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()

        elif match.find('created:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()

        elif match.find('e-mail:') != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()

        elif match.find('organization:') != -1:
            domain_whois['org_name'] = match.split(':', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois
#
# result=
# domain:                       te.ua
# status:                       30
# flag:                         111
# sponsoring_registrar:
# top_whois_server:             whois.ua
# sec_whois_server:
# reg_name:
# reg_phone:
# reg_email:                    vit@sacura.net
# org_name:                     ТОВ "Юнітрейд Про"
# updated_date:                 UT45-UANIC 20121121114323
# creation_date:                0-UANIC 19970216000000
# expiration_date:
# name_server:                  ns.te.ua;ns2.uar.net;nix.ns.ua;ns2.km.ua;ns.dn.ua;ns.te.ua
# hash_value:                   1857382894111946535

#==================================================================================================================

#>>>>>>tld    .tz
#addr   whois.tznic.or.tz
#Eg     go.tz

# raw_data=
# domain:       go.tz
# registrant:   ADMIN-TZNIC
# admin-c:      ADMIN-TZNIC
# nsset:        NS-GO.TZ
# keyset:       KS-GO.TZ
# registrar:    REG-TZNIC
# registered:   22.07.2009 11:44:11
# changed:      12.10.2012 19:00:43
# expire:       22.07.2019
#
# contact:      ADMIN-TZNIC
# org:          Tanzania Network Information Centre
# name:         Manager
# address:      LAPF Millennium Towers
# address:      New Bagamoyo Road
# address:      Dar es Salaam
# address:      P.O. BOX 34543
# address:      TZ
# phone:        +255.222772659
# fax-no:       +255.222772660
# e-mail:       manager@tznic.or.tz
# registrar:    REG-TZNIC
# created:      22.07.2009 11:42:00
#
# nsset:        NS-GO.TZ
# nserver:      ns2.tznic.or.tz
# nserver:      nic.co.tz
# nserver:      rip.psg.com
# nserver:      d.ext.nic.cz
# nserver:      sns-pb.isc.org
# nserver:      ns.anycast.co.tz
# nserver:      fork.sth.dnsnode.net
# tech-c:       MNT-TZNIC
# registrar:    REG-TZNIC
# created:      22.07.2009 11:43:24
# changed:      10.07.2015 16:53:44
#
# contact:      MNT-TZNIC
# org:          Tanzania Network Information Centre
# name:         Technical Officer
# address:      LAPF Millenium Towers
# address:      New Bagamoyo Road
# address:      Dar es Salaam
# address:      P.O.Box 34543
# address:      TZ
# phone:        +255.222772659
# fax-no:       +255.222772660
# e-mail:       support@tznic.or.tz
# registrar:    REG-TZNIC
# created:      21.07.2009 15:28:07
# changed:      04.02.2015 16:46:11
#
# keyset:       KS-GO.TZ
# dnskey:       257 3 10 AwEAAeNXG65FqNdH9IY23oKSPApuUBlxo8gVLcvw08aV/9Kg4/glTKNPeQNnFDIzo2yBTrm2HhS/6+TWBvAWu3KVw/5AItQwTEsOWZEWTaP2B5uX1qS3VuKVqKgf+jT6GZnpLOxkAIcj5osD0w1DKjHmUnWjzejtU6yY1h4slJ7TNSST
# tech-c:       MNT-TZNIC
# registrar:    REG-TZNIC
# created:      12.10.2012 19:00:23
# changed:      05.03.2015 12:53:56

def tz_manage(domain_whois, data):
    if data.find('No entries found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrant:.*|registrar:.*|registered:.*|changed:.*|\
|expire:.*|org:.*| name:.*|phone:.*|e-mail:.*|nserver:.*|created:.*)')


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
            domain_whois['reg_phone'] = match.split('.', 1)[1].strip()

        elif match.find('e-mail') != -1:
            domain_whois['reg_email'] = match.split('.', 1)[1].strip()

        elif match.find('org') != -1:
            domain_whois['org_name'] = match.split('.', 1)[1].strip()


    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois

# result=domain:                       go.tz
# status:                       30
# flag:                         122
# sponsoring_registrar:         ADMIN-TZNIC
# top_whois_server:             whois.tznic.or.tz
# sec_whois_server:
# reg_name:                     Technical Officer
# reg_phone:                    +255.222772659
# reg_email:                    support@tznic.or.tz
# org_name:                     Tanzania Network Information Centre
# updated_date:                 05.03.2015 12
# creation_date:                12.10.2012 19
# expiration_date:              22.07.2019
# name_server:                  ns2.tznic.or.tz;nic.co.tz;rip.psg.com;d.ext.nic.cz;sns-pb.isc.org;ns.anycast.co.tz;fork.sth.dnsnode.net
# hash_value:                   -6678294567317075623

if __name__ == '__main__':

