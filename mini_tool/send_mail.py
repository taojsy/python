#!/usr/bin/env python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

me = "jun.tao@nokia-sbell.com"
you = "jun.tao@nokia-sbell.com"
# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('multipart')
msg['Subject'] = "mail sending test"
msg['From'] = me
msg['To'] = you
# Create the body of the message (a plain-text and an HTML version).
#text = "Hi!/nHow are you?/nHere is the link you wanted:/nhttp://www.python.org"
text = 'Hi!/nHow are you?/nHere is text part'
html = """
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       Here is html part<br>
       Here is the <a href="http://www.python.org" mce_href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""
# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')
# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)
# Send the message via local SMTP server.
s = smtplib.SMTP('mail.int.nokia-sbell.com')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()



