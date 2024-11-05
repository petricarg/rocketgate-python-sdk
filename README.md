![rocketgate-python-sdk](http://rocketgate.com/images/logo_rocketgate.png)

RocketGate Gateway Python SDK
===========

The Python 3.x Software Development Kit and Test Scripts

Documentation is available in RocketGate's helpdesk at https://help.rocketgate.com/support/solutions/28000015702

Docs related to this repository are located at:

1. GatewayService: https://help.rocketgate.com/support/solutions/articles/28000018238-gatewayservice
2. GatewayRequest: https://help.rocketgate.com/support/solutions/articles/28000018237-gatewayrequest
3. GatewayResponse: https://help.rocketgate.com/support/solutions/articles/28000018236-gatewayresponse
4. GatewayResponse Error / Decline Codes: https://help.rocketgate.com/support/solutions/articles/28000018169-gatewayresponse-error-decline-codes


## Running integration tests
From the root of the project, using your installed Python Interpreter, run the following command:
```shell
python3 -m unittest discover ./tests -p '*.py'
```

## Install RocketGate SDK
```shell
pip install RocketGate
```

## Example

Save next `python` code in `AuthOnly.py` file and
run with `python3 AuthOnly.py`

```python
from RocketGate import *

request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

request.Set(GatewayRequest.MERCHANT_ID, "1")
request.Set(GatewayRequest.MERCHANT_PASSWORD, "testpassword")

request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, "My.PythonTest")
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, "My.Invoice")

request.Set(GatewayRequest.AMOUNT, 9.99)
request.Set(GatewayRequest.CURRENCY, "USD")

request.Set(GatewayRequest.CARDNO, "4111111111111111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
request.Set(GatewayRequest.BILLING_STATE, "NV")
request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
request.Set(GatewayRequest.BILLING_COUNTRY, "US")

request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.EMAIL, "python_user@fakedomain.com")
request.Set(GatewayRequest.IPADDRESS, "68.224.133.117")

request.Set(GatewayRequest.AVS_CHECK, "IGNORE")
request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
request.Set(GatewayRequest.SCRUB, "IGNORE")

service.SetTestMode(1)

# Perform the Auth-Only transaction.
if service.PerformAuthOnly(request, response):
    print("Auth Only succeeded")
    print("GUID: ", response.Get(GatewayResponse.TRANSACT_ID))
    print("Response Code: ", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code: ", response.Get(GatewayResponse.REASON_CODE))
    print("AuthNo: ", response.Get(GatewayResponse.AUTH_NO))
    print("AVS: ", response.Get(GatewayResponse.AVS_RESPONSE))
    print("CVV2: ", response.Get(GatewayResponse.CVV2_CODE))
    print("Card Hash: ", response.Get(GatewayResponse.CARD_HASH))
    print("Card Region: ", response.Get(GatewayResponse.CARD_REGION))
    print("Card Description: ", response.Get(GatewayResponse.CARD_DESCRIPTION))
    print("Account: ", response.Get(GatewayResponse.MERCHANT_ACCOUNT))
    print("Scrub: ", response.Get(GatewayResponse.SCRUB_RESULTS))

else:
    print("Auth Only failed")
    print("GUID: ", response.Get(GatewayResponse.TRANSACT_ID))
    print("Response Code: ", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code: ", response.Get(GatewayResponse.REASON_CODE))
    print("Exception: ", response.Get(GatewayResponse.EXCEPTION))
    print("Scrub: ", response.Get(GatewayResponse.SCRUB_RESULTS))

```

Expect to see output like:

```bash
Auth Only succeeded
GUID:  1000192FD2DED89
Response Code:  0
Reason Code:  0
AuthNo:  985828
AVS:  Y
CVV2:  None
Card Hash:  8Yz0jmvTGdDaZV9g58L+9mJ+0jw2fodvgktC/jS8GSs=
Card Region:  1,2
Card Description:  CLASSIC
Account:  14
Scrub:  NEGDB=0,PROFILE=0,ACTIVITY=1
```