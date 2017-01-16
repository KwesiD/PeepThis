# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
import keys
import user_info

# Find these values at https://twilio.com/user/account
# account_sid = "ACXXXXXXXXXXXXXXXXX"
# auth_token = "YYYYYYYYYYYYYYYYYY"
def send_sms(message):
	client = TwilioRestClient(keys.text_sid,keys.text_token)

	message = client.messages.create(to=user_info.phone, from_=keys.text_phone,
	                                     body=message)