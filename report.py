import smtplib
import json
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('c:\\API\Mykola\copy_tables\credentials_report.json') as f:
    MAIL = json.load(f)

def send_report(data, recipient = None):
    text = make_body(data)
    me = MAIL['from']
    mail2 = recipient if recipient else MAIL['recipient']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'parse_links report {date.today(): %Y-%m-%d}'
    msg['From'] = me
    msg['To'] = mail2

    print(text)
    # msg.attach(MIMEText(text, 'html'))
    # server = smtplib.SMTP(f'{MAIL["host"]}:{MAIL["port"]}')
    # server.login(MAIL['user'], MAIL['password'])
    # server.sendmail(me, mail2.split(','), msg.as_string())
    # server.quit()

def make_body(data):
    body = str(data)
    return body

if __name__ == '__main__':
    result = [('ikscs.in.ua', 200, 2609), ('ikscs.in.ua', 301, 869), ('ikscs.in.ua', 404, 3), ('ingener.in.ua', 0, 1), ('ingener.in.ua', 200, 723), ('ingener.in.ua', 303, 1), ('ingener.in.ua', 404, 13)]
    send_report(result)