from datetime import datetime
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import constants



_timeOfEvent=datetime.now()

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
s.login(mailAddress,password)

names, emails = getContacts('contacts.txt')
# if fail - use Fail, if success - use Success
message_template = readTemplate('msgDeploySuccess.txt')

for name, email in zip(names, emails): #building the email msg object:
    msg = MIMEMultipart() # created the mail
    message = message_template.substitute(PERSON_NAME=name.title(), TIME_OF_ERROR=_timeOfEvent) #add the actual name to the template
    msg['From']=_mailAddress
    msg['To']=email
    msg['Subject']='Test Mail for DevWeek'
    msg.attach(MIMEText(message,'plain'))
    s.send_message(msg) #sending the actual email
    
    del msg