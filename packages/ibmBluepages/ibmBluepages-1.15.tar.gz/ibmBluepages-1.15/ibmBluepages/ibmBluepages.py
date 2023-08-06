#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import json
import httplib2
from xml.dom.minidom import parse
import xml.dom.minidom

from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool, Tls
import ssl
#author: guojial@cn.ibm.com
#version: v1.15
#Date:   2019-07-25
#Last Modified by: guojial@cn.ibm.com
#Last Modified time: 2019-07-25

class ibmBluepages:
    
    #from Bluepages get person's information.
    def getPersonInfoByIntranetID(self, intranetID):
        
        http = httplib2.Http() 
        content = http.request("https://bluepages.ibm.com/BpHttpApisv3/slaphapi?ibmperson/mail="+intranetID+".list/byxml", "GET")
        #print(content)
        
        DOMTree = xml.dom.minidom.parseString(content[1])
        collection = DOMTree.documentElement
        #print(content[1])

        entry = collection.getElementsByTagName("entry")
        attrs = collection.getElementsByTagName("attr")
        #print(entry[0].getAttribute("dn"))

        attrData = {}
        for attr in attrs:
            #print (attr.getAttribute('name') + "  :  " + attr.getElementsByTagName('value')[0].childNodes[0].data)
            attrData[attr.getAttribute("name")] = attr.getElementsByTagName("value")[0].childNodes[0].data
        
        #print(attrData)
        attrData["dn"] = entry[0].getAttribute("dn")
        personInfo = json.dumps(attrData)
        #print(personInfo)
        return personInfo

    #authenticate the person existed in Bluepages
    def authenticate(self, username, password):

        SEARCH_BASE = "ou=bluepages,o=ibm.com"
        ldap_server_pool = "ldaps://bluepages.ibm.com:636"
        server = Server(ldap_server_pool, get_info=ALL)

        personInfo = self.getPersonInfoByIntranetID(username)
        personInfo = eval(personInfo)
        
        dn = personInfo["dn"]
        # check password by dn
        try:
            #print("dn==========>" + dn)
            conn = Connection(server, user = dn, password = password, check_names = True, lazy = False, raise_exceptions = False) 
            conn.open()
            conn.bind()
            #print(conn)
            #print(conn.result["description"])
            if conn.result["description"] == "success":
                #print("success")
                return True
            else: 
                #print("auth fail")
                return False 
        except Exception as e:
            #print("auth fail")
            return False
    
    def getPersonInfoByIntranetIDUseProfile(self, intranetID):
        
        http = httplib2.Http() 
        content = http.request("http://unified-profile.w3ibm.mybluemix.net/myw3/unified-profile/v1/docs/instances/masterByEmail?email="+intranetID+"", "GET")
        #print(content)
        if (content[0]['status'] == '200'):
            strCon = str(content[1], 'utf-8')
            #print (strCon)
            jsonCon = json.loads(strCon)
            #print (len(jsonCon))
            #print(len(jsonCon['content']['identity_info']))
            contentInfo = jsonCon['content']['identity_info']
            contentInfo["image"] = "https://unified-profile.w3ibm.mybluemix.net/myw3/unified-profile-photo/v1/image/"+intranetID+""
            return contentInfo
        else:
           return False
        