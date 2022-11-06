import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config



# read in our list of keywords
# with open("keywords.txt", "r") as fd:
#    file_contents = fd.read()
#    keywords = file_contents.splitlines()
def send_alert(alert_email):

    email_body = "The following are keyword hits that were just found:\r\n\r\n"

    # walk through the searx results
    if 'searx' in alert_email:

        for keyword in alert_email['searx']:

            email_body += "<h1>\r\nKeyword: %s\r\n\r\n</h1>" % keyword

            for keyword_hit in alert_email['searx'][keyword]:
                if keyword_hit[12:19] == 'youtube':
                    email_body += """<p>This is an alert test,<br>
                               <br>
                               <iframe width="105" height="75" src='""" + keyword_hit + """'>
</iframe> 
                               you are great.
                            </p>
                            """
                else:
                    email_body += """<p>This is an alert test,<br>
           <br>
           <a href='""" + keyword_hit + """'>Real Link test</a> 
           you are great.
        </p>
        """

    # walk through pastebin results
    html = """\
    <html>
      <body>
        """ + email_body + """
      </body>
    </html>
    """

    # build the email message

    msg = MIMEText(html, "html")
    #msg = MIMEMultipart(html)
    msg['Subject'] = " Keyword Alert"
    msg['From'] = config.alert_email_account
    msg['To'] = config.alert_email_account
    msg["Bcc"] = 'nopyepyep@gmail.com'


    server = smtplib.SMTP("mail.lovebenin.com", 26)

    server.ehlo()
    server.starttls()
    server.login(config.alert_email_account, config.alert_email_password)
    server.sendmail(config.alert_email_account, config.alert_email_account, msg.as_string())
    server.quit()

    print("[!] Alert email sent!")

    return