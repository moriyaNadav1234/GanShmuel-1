from ast import If
from datetime import datetime
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest import case
# from constants import mailAddress, password

mailAddress='dorzvulundeveleapbluedevops@gmail.com'
password='13578642'

# create 3 mailing lists - DevOps only, Billing+DevOps, Weight+DevOps
def _getContacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split(", ")[0])
            emails.append(a_contact.split(", ")[1])
    return names, emails

def _readTemplate(filename):
    with open(filename,mode='r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)    

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(mailAddress,password)
    

def mailNotification(proc, team, status): #proc = build/deploy, team = mailinglist, status = success/fail
    if team == 'billing': # B&DO
        names, emails = _getContacts('./mailingService/Billing_DevOps_MailingList.txt')
            
    if team == 'weight': # W&DO
        names, emails = _getContacts('./mailingService/Weight_DevOps_MailingList.txt')

            
    if team ==  'devops': 
        names, emails = _getContacts('./mailingService/DevOps_MailingList.txt')
    

         # select EMail Template
        if status:  
            message_template = _readTemplate('./mailingService/msgSuccess.txt')
            st = 'Success'
        else:
            message_template = _readTemplate('./mailingService/msgFail.txt')
            st = 'Failed'

    
    timeOfEvent=datetime.now() # simulated time of event 
    if proc == "updateRepo":
        proc = "update server's repo"
        
    for name, email in zip(names, emails): #building the email msg object:
        msg = MIMEMultipart() # created the mail
        message = message_template.substitute(PERSON_NAME=name.title(), TIME_STAMP=timeOfEvent, PROCCESS=proc.upper()) #add the actual name to the template
        msg['From']=mailAddress
        msg['To']=email
        msg['Subject']=f'Important Update - {proc.upper()} proccess ${st.upper()}'
        msg.attach(MIMEText(message,'plain'))
        s.send_message(msg) #sending the actual email
        del msg

def sendErrorToLog(filename, status, proc):
    
    filename = "./logs/"+filename
    with open(filename,mode='a', encoding='utf-8') as log_file:
        loginput=f'{datetime.now()}: {proc} has {status.upper()}\n'
        log_file.write(loginput)
            
    