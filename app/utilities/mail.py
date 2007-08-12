import smtplib
import string, sys

# thanks effbot
def mail(to, subject, message):
    HOST = "localhost"
    FROM = "admin@seddit"
    TO = to
    SUBJECT = subject
    BODY = message

    body = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        BODY), "\r\n")

    print body

    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, [TO], body)
    server.quit()
    
if __name__ == "__main__":
    mail('drew@substandard.net', 'hey there', 'this is a test')