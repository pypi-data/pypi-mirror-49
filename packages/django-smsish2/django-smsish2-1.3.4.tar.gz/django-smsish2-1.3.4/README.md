# django-smsish
Forked from [RyanBalfanz](https://github.com/RyanBalfanz/django-smsish)

Installation
------------

Add `smsish` to your `INSTALLED_APPS` and set `SMS_BACKEND`.

	INSTALLED_APPS += (
		'smsish',
	)

	SMS_BACKEND_CONSOLE = 'smsish.sms.backends.console.SMSBackend'
	SMS_BACKEND_DUMMY = 'smsish.sms.backends.dummy.SMSBackend'
	SMS_BACKEND_TWILIO = 'smsish.sms.backends.twilio.SMSBackend'
	SMS_BACKEND = SMS_BACKEND_DUMMY

To use the Twilio backend set some additional settings as well.

	TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", None)
	TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", None)
	TWILIO_MAGIC_FROM_NUMBER = "+15005550006"  # This number passes all validation.
	TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", TWILIO_MAGIC_FROM_NUMBER)

Note: You must also `pip install twilio` to use the Twilio backend.


# Test

```
tox
```
