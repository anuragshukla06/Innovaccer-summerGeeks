# importing twilio
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com / console

# This is just a test file.
account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)

''' Change the value of 'from' with the number  
received from Twilio and the value of 'to' 
with the number in which you want to send message.'''
message = client.messages.create(
    from_='+12055579239',
    body='body',
    to='+919399151865'
)

print(message.sid) 