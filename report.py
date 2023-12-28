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
    msg.attach(MIMEText(text, 'html'))
    server = smtplib.SMTP(f'{MAIL["host"]}:{MAIL["port"]}')
    server.login(MAIL['user'], MAIL['password'])
    server.sendmail(me, mail2.split(','), msg.as_string())
    server.quit()

def make_body(data):
    flag_400, flag_500 = False, False
    for domain, status_code, count in data:
        if not status_code:
            continue
        if status_code >= 500:
            flag_500 = True
        elif (status_code >= 400) and (status_code < 500):
            flag_400 = True
    if flag_400:
        if flag_500:
            text = 'ERRORS 400, 500'
        else:
            text = 'ERROR 400'
    else:
        if flag_500:
            text = 'ERROR 500'
        else:
            text = 'all OK'
    
    style = 'style="background-color:Red;"' if 'ERROR' in text else ''
    body = f'<h1 {style}>{text}</h1>\n'
    body += '<table cellpadding="5" border="1" style="border-collapse: collapse;">'
    body += '<tr>'
    body += '<th>domain</th>'
    body += '<th>status_code</th>'
    body += '<th>count</th>'
    body += '</tr>'
    for row in data:
        body += '<tr>'
        for col in row:
            body += f'<td align="right">{col}</td>'
        body += '</tr>'    
    body += '</table>'
    return body

if __name__ == '__main__':
    result = [('ikscs.in.ua', 200, 2609), ('ikscs.in.ua', 301, 869), ('ikscs.in.ua', 404, 3), ('ingener.in.ua', 0, 1), ('ingener.in.ua', 200, 723), ('ingener.in.ua', 303, 1), ('ingener.in.ua', 404, 13)]
    send_report(result, 'all OK')