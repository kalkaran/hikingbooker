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


#not sure if there is a csfr token but I am adding it to check.

def get_csfr_token(text):
    m = re.search('name="csfr_token" value="([^"]+)"', text)
    return m.group(1)




def get_config():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    '''
    [simplesettings]
email = mail@example.com
docpassword = password
account_sid = AC...
auth_token = 39abdad23123
number = 0101010101
receiver = 01010101
    
    
    
    '''


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



def login(session, url, password):
    r = session.get(url)
    r.raise_for_status()
    csfr_token = get_csfr_token(r.text)

    configdata = get_config()

    data = dict({
        'inUsername' : configdata[email],
        'inPassword' : configdata[inPassword],
        'inSessionSecurity' : 'on',
        'sublogin2' : 'LogIn',
        'csfr_token' : csfr_token,
    })




def sendtext(text):
    data = get_config()

    account_sid = data['account_sid']
    auth_token = data['auth_token']
    number = data['number']
    receiver = data['receiver']

    client = Client(account_sid, auth_token)

    message = client.messages \
    .create(
    body=text,
    from_=number,
    to=receiver
    )

    print(message.sid)

sendtext("helloski puffin time")

