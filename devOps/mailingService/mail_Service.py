from datetime import datetime
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest import case
import constants

# TODO: DONE! create a function that will recive a maling list, success/fail, deploy/build and will build a mail accordingly. 

# create 3 mailing lists - DevOps only, Billing+DevOps, Weight+DevOps
def getContacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split(", ")[0])
            emails.append(a_contact.split(", ")[1])
    return names, emails

def readTemplate(filename):
    with open(filename,mode='r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)    

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(constants.mailAddress,constants.password)
    

def mailNotification(proc, team, status ): #proc = build/deploy, team = mailinglist, status = success/fail
    match team: # select mailing list
        case 'billing': # B&DO
            names, emails = getContacts('Billing_DevOps_MailingList.txt')
            
        case 'weight': # W&DO
            names, emails = getContacts('Weight_DevOps_MailingList.txt')
            
        case 'devops': 
            names, emails = getContacts('DevOps_MailingList.txt')
    
    match status: # select EMail Template
        case True: 
            message_template = readTemplate('msgSuccess.txt')
            st = 'Success'
        
        case False : 
            message_template = readTemplate('msgFail.txt')
            st = 'Failed'
    
    timeOfEvent=datetime.now() # simulated time of event 
    
    for name, email in zip(names, emails): #building the email msg object:
        msg = MIMEMultipart() # created the mail
        message = message_template.substitute(PERSON_NAME=name.title(), TIME_STAMP=timeOfEvent, PROCCESS=proc.upper()) #add the actual name to the template
        msg['From']=constants.mailAddress
        msg['To']=email
        msg['Subject']=f'Important Update - {proc.upper()} proccess ${st.upper()}'
        msg.attach(MIMEText(message,'plain'))
        s.send_message(msg) #sending the actual email
        del msg
    
    
    
        
            
    