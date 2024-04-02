import smtplib
from email.message import EmailMessage
 
def sendmail(to,subject,body):
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('manukondaaneela1520@gmail.com','vqvj uzhh wbvt idhk')
    msg= EmailMessage()
    msg['From']='manukondaaneela1520@gmail.com'
    msg['To'] =to
    msg['subject']=subject
    msg.set_content(body)
    server.send_message(msg)
    server.quit()

