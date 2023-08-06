## Cowin API

Python package to interact with [COWIN Public API](https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2)

### Features

- [x] Supports both Synchronous and Asynchronous modes.
- [x] 95% test coverage with mocking API responses.
- [x] Get list of states
- [x] Get list of districts for a state
- [x] Get vaccine centers with sessions by pincode and date
- [x] Generate and Verify OTP
- [x] Download Certificates

Example:

For API response payload samples visit the [API portal](https://apisetu.gov.in/public/marketplace/api/cowin/cow).

```python
# blocking synchronous client
from cowin import Cowin

client = Cowin()

states = client.get_states()
districts = client.get_districts(state_id=4)

# below function accepts optional datetime.date object
# by default current date is used
vaccine_sessions = client.get_available_sessions_by_pincode(pincode=605001)

# get OTP to mobile number
response = client.get_otp(mobile='9876543210')
txn_id = response['txnId']

# verify OTP and receive token
response = client.confirm_otp(txn_id=txn_id, otp=123456)
token = response['token']

# download certificate by beneficiary reference number
# Note: ServerError exception will be raised when response content is not pdf
cert_content = client.get_certificate(token, beneficiary_id='xxxxxxxxxxxx')

# save certificate content to disk
with open('certificate.pdf', 'wb') as cert_file:
    cert_file.write(cert_content)
```

```python
# non-blocking async client
from cowin import AsyncCowin

async_client = AsyncCowin()

states = await async_client.get_stateS()
districts = await async_client.get_districts(state_id=4)

vaccine_sessions = await async_client.get_available_sessions_by_pincode(pincode='605001')

# get OTP to mobile number
response = await async_client.get_otp(mobile='9876543210')
txn_id = response['txnId']

# verify OTP and receive token
response = await async_client.confirm_otp(txn_id=txn_id, otp='123456')
token = response['token']

# download certificate by beneficiary reference number
# Note: ServerError exception will be raised when response content is not pdf
cert_content = await async_client.get_certificate(token, beneficiary_id='xxxxxxxxxxxx')

# save certificate content to disk
with open('certificate.pdf', 'wb') as cert_file:
    cert_file.write(cert_content)
```

### Contributions

Issues and pull requests are welcome. Feel free to improve the package.

# License:

LGPL v3.0
