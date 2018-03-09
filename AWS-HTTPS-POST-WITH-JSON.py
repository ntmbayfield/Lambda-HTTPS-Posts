import base64
import json
import os
import urllib
from urllib import request, parse

# update the xxxxx text with the domain name of your mailgun service (typically: mail.yourdomaingoeshere.com)
TARGET_URL = "https://api.mailgun.net/v3/XXXXXXXXXXXXXXXXX/messages"
USER_ID = os.environ.get("ACCOUNT_ID")
USER_PASS = os.environ.get("ACCOUNT_PASS")


def lambda_handler(event, context):
    to_email = event['To']
    from_email = event['From']
    email_subject = "Alert: " + str(event['Subject']) 
    email_html = event['HTML'] 
    
    if not USER_ID:
        return "Unable to access USER ID."
    elif not USER_PASS:
        return "Unable to access USER PASS."
    elif not to_email:
        return "The function needs a 'To' email"
    elif not from_email:
        return "The function needs a 'From' email"
    elif not email_subject:
        return "The function needs a 'Email Subject' message to send."

    # insert Account ID into the REST API URL
    populated_url = TARGET_URL.format(USER_ID)
    post_params = {"to": to_email, "from": from_email, "subject": email_subject, "html": email_html}

    # encode the parameters for Python's urllib
    data = parse.urlencode(post_params).encode()
    req = request.Request(populated_url)

    # add authentication header to request based on Account SID + Auth Token
    authentication = "{}:{}".format(USER_ID, USER_PASS)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))

    try:
        # perform HTTP POST request
        with request.urlopen(req, data) as f:
            print("Service returned {}".format(str(f.read().decode('utf-8'))))
    except Exception as e:
        # something went wrong!
        return e

    return "Message sent successfully!"
