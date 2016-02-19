import os, sys, smtplib
from email.mime.text import MIMEText

#username = 'somebody@gmail.com'
#password = 'rsapbxdgreajkser'


def send(msg_file, frm, to, subject):
    #print('Enter gmail password for %s.' % username)
    #password = raw_input()
    with open(msg_file, 'rb') as f:
        msg = MIMEText(f.read())
    msg['Subject'] = subject
    msg['From'] = frm
    msg['Reply-To'] = frm
    #s = smtplib.SMTP('smtp.gmail.com:587')
    s = smtplib.SMTP('mail.acme.com')
    #s.ehlo()
    #s.starttls()
    #s.login(username, password)
    s.sendmail(frm, [x.strip() for x in to.split(',')], msg.as_string())
    s.quit()

if __name__ == '__main__':
    try:
        send(*sys.argv[1:])
    except:
        import traceback
        traceback.print_exc()
        print('\n\nSample invocation:\npython sendmail.py msg1.txt "\\"Steve Taylor\\" <steven.taylor@acme.com>" "\\"Gullible Jack\\" <gjack@acme.com>, \\"Gullible Jane\\" <gjane@acme.com>" "worried about new java CVE; may affect our codebases"\n')
