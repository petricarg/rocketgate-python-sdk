#! /usr/bin/env python

"""
Copyright notice:
(c) Copyright 2018 RocketGate
All rights reserved.

The copyright notice must not be removed without specific, prior
written permission from RocketGate.

This software is protected as an unpublished work under the U.S. copyright
laws. The above copyright notice is not intended to effect a publication of
this work. This software is the confidential and proprietary information of RocketGate.
Neither the binaries nor the source code may be redistributed without prior
written permission from RocketGate.

The software is provided "as-is" and without warranty of any kind, express, implied
or otherwise, including without limitation, any warranty of merchantability or fitness
for a particular purpose. In no event shall RocketGate be liable for any direct,
special, incidental, indirect, consequential or other damages of any kind, or any damages
whatsoever arising out of or in connection with the use or performance of this software,
including, without limitation, damages resulting from loss of use, data or profits, and
whether or not advised of the possibility of damage, regardless of the theory of liability.
"""

import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RocketGate import *

"""
Example Scenario:
$9.99 USD purchase.
Subsequently, the user wants to make another $8.99 purchase using the card on file (CardHash)
"""

current_time = int(time.time())
cust_id = f"{current_time}.PythonTest"
inv_id = f"{current_time}.PayInfoTest"

merchant_id = "1"
merchant_password = "testpassword"
merchant_id_1c = "1256059862"
merchant_password_1c = "LLSgMD8tSkVkZED3"

# Allocate the objects we need for the test
request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

# Setup the Purchase request
request.Set(GatewayRequest.MERCHANT_ID, merchant_id)
request.Set(GatewayRequest.MERCHANT_PASSWORD, merchant_password)

# Setting the order id and customer as the unix timestamp as a convenient sequencing value
# Prepended a test name to the order id to facilitate some clarity when reviewing the tests 
request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

# Example join on Site 1
request.Set(GatewayRequest.MERCHANT_SITE_ID, 1)

# $9.99/month subscription
request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.AMOUNT, 9.99)  # bill 9.99

request.Set(GatewayRequest.CARDNO, "4111111111111111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.EMAIL, "pythontester@fakedomain.com")

request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
request.Set(GatewayRequest.BILLING_STATE, "NV")
request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
request.Set(GatewayRequest.BILLING_COUNTRY, "US")

# Risk/Scrub Request Setting
request.Set(GatewayRequest.SCRUB, "IGNORE")
request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

# Setup test parameters in the service and request
service.SetTestMode(True)

# Perform the Purchase transaction
if service.PerformPurchase(request, response):
    print("Purchase succeeded")
    print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))

    # Get the PayInfo Token so we can run the next transaction without needing to store the credit card #
    payinfo_transact_id = response.Get(GatewayResponse.TRANSACT_ID)

    # Run additional purchase using card_hash
    # This would normally be two separate processes,
    # but for example's sake is in one process (thus we clear and set a new GatewayRequest object)
    # The key values required are MERCHANT_CUSTOMER_ID and MERCHANT_INVOICE_ID AND CARD_HASH.
    request = GatewayRequest()
    request.Set(GatewayRequest.MERCHANT_ID, merchant_id_1c)
    request.Set(GatewayRequest.MERCHANT_PASSWORD, merchant_password_1c)

    request.Set(GatewayRequest.REFERRING_MERCHANT_ID, merchant_id)
    request.Set(GatewayRequest.REFERRED_CUSTOMER_ID, cust_id)
    request.Set(GatewayRequest.PAYINFO_TRANSACT_ID, payinfo_transact_id)

    request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, f"{cust_id}1CTEST")
    request.Set(GatewayRequest.MERCHANT_INVOICE_ID, f"{inv_id}1CTEST")

    # Example 1-click on Site 2
    request.Set(GatewayRequest.MERCHANT_SITE_ID, 2)

    request.Set(GatewayRequest.AMOUNT, 14.99)
    request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")

    if service.PerformPurchase(request, response):
        print("1Click Purchase succeeded")
        print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
        print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
        print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    else:
        print("1Click Purchase failed")
        print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
else:
    print("Purchase failed")
    print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("Exception:", response.Get(GatewayResponse.EXCEPTION))
    print("Scrub:", response.Get(GatewayResponse.SCRUB_RESULTS))
