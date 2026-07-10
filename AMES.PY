#AUTOMATED EMAIL SENDER 

import smtplib
from email.message import EmailMessage

import time

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
def serv(server):
    server.login('hdeep89977@gmail.com', 'syqk fsmb yhsg zmma')

serv(server)

msg= EmailMessage()
msg['From']= "hdeep89977@gmail.com"
msg['To']=input("Enter receiver email: ")
msg['subject']= "Hello from Python Email Sender"

msg.set_content("""
Hello,

This is a test email sent using my Python Automated Email Sender project.

Regards,
Harmandeep
""")
for i in range(10):
    server.sendmail(
        msg['From'],
        msg['To'],
        msg.as_string()
    )
    print(f"Email {i+1} sent")
    time.sleep(6)   # 6 seconds ka gap
server.quit()

