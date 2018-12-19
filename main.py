#!/usr/bin/env python3

import requests
import re
import sys
import configparser


## Twilio ##
from twilio.rest import Client

'''
pip installs
pip install requests
pip install ConfigParser
pip install twilio
'''

# Aim of the program is to login to the DOC site
# Select the correct settings
#Choose : Great walk, start date, nights = 1, number of people = 2
#Make a search
#save the availabilities
#Select the next x weeks
#save the next x availabilities
#if there is an availability then signal in some way
#probably see if I can hook up twilio to send a text message to me


def get_config():
    '''returns the parameters for logging in and using notification services'''
    '''
    example config file
    [simplesettings]
    email = mail@example.com
    docpassword = password
    account_sid = AC...
    auth_token = 39abdad23123
    number = 0101010101
    receiver = 01010101
    '''
    config = configparser.ConfigParser()
    config.read("./config.ini")

    #for doc website
    configemail = config.get('simplesettings', 'email')
    configdocpassword = config.get('simplesettings', 'docpassword')

    #for twilio
    configaccount_sid = config.get('simplesettings', 'account_sid')
    configauth_token = config.get('simplesettings', 'auth_token')
    confignumber = config.get('simplesettings', 'number')
    configreceiver = config.get('simplesettings', 'receiver')

    data = dict({
        'loginemail': configemail,
        'docpassword': configdocpassword,
        'account_sid': configaccount_sid,
        'auth_token': configauth_token,
        'number': confignumber,
        'receiver': configreceiver,
        })
    return data


def sendtext(text):
    '''sends text message containing arguement based on parameters set in config file'''
    configdata = get_config()

    account_sid = configdata['account_sid']
    auth_token = configdata['auth_token']
    number = configdata['number']
    receiver = configdata['receiver']

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=text,
        from_=number,
        to=receiver
    )

    print(message.sid)



#not sure if there is a csfr token but I am adding it to check.

def get_csfr_token(text):
    m = re.search('name="csfr_token" value="([^"]+)"', text)
    return m.group(1)

def login(session, url, password):
    r = session.get(url)
    r.raise_for_status()
    configdata = get_config()

    '''
    ctl01$Hidscreenresolutionmain	
    ctl01$hdnCulture	
    ctl01$Rptheadermenu$ctl00$HidURL	/Default.aspx
    ctl01$Rptheadermenu$ctl01$HidURL	/Facilities/SearchViewGW.aspx
    ctl01$hdnClearCustomerKiosk	
    ctl01$mainContent$txtEmail	test@test.com
    ctl01$mainContent$txtPassword	fart
    
    '''

    data = dict({
        'ctl01$Rptheadermenu$ctl00$HidURL':	'/Default.aspx',
        'ctl01$Rptheadermenu$ctl01$HidURL':	'/Facilities/SearchViewGW.aspx',
        'ctl01$mainContent$txtEmail' : configdata['loginemail'],
        'ctl01$mainContent$txtPassword' : configdata['docpassword'],
    })




def testbed(url):
    configdata = get_config()
    data = dict({
        'ctl01$Rptheadermenu$ctl00$HidURL':	'/Default.aspx',
        'ctl01$Rptheadermenu$ctl01$HidURL':	'/Facilities/SearchViewGW.aspx',
        'ctl01$mainContent$txtEmail': configdata['loginemail'],
        'ctl01$mainContent$txtPassword': configdata['docpassword'],
    })

    r = requests.post(url, data=data)
    return r.text


url = "https://bookings.doc.govt.nz/Saturn/Customers/Login.aspx"
with open("test.html","w+") as f:
    f.write(testbed(url))


