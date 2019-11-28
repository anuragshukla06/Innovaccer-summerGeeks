# importing twilio
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com / console 
account_sid = 'ACce78497a4095c6d2166193ba17149ab7'
auth_token = '99935c13fba0c8893067fc6ec67a0b7d'

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