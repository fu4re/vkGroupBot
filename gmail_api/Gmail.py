import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# from email import encoders



class Mail:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def gmailCreateMsg(self, subject, reciever, msg, attach=None):
        message = MIMEMultipart()
        attachment = MIMEBase('application', "octet-stream")

        message['From'] = self.login
        message['To'] = reciever
        message['Subject'] = subject

        # attachment.set_payload(attach)
        # encoders.encode_base64(attachment)

        message.attach(MIMEText(msg, 'plain'))
        # message.attach(attachment)

        gmail_session = smtplib.SMTP('smtp.gmail.com', 587)
        gmail_session.starttls()
        gmail_session.login(self.login, self.password)
        gmail_session.sendmail(self.login, reciever, message.as_string())
        gmail_session.quit()

        print('Message to ' + f"{reciever}, text: {msg};" + ' send!')