#! /usr/bin/env python

"""
Copyright notice:
(c) Copyright 2024 RocketGate
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

# Setup a couple required and testing variables
the_time = int(time.time())
cust_id = f"{the_time}.PythonTest"
inv_id = f"{the_time}.RebillStatusTest"
merch_id = "1"
merch_password = "testpassword"

# Allocate the objects we need for the test.
request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

# Setup the Purchase request.
request.Set(GatewayRequest.MERCHANT_ID, merch_id)
request.Set(GatewayRequest.MERCHANT_PASSWORD, merch_password)

request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

request.Set(GatewayRequest.AMOUNT, 9.99)
request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")

request.Set(GatewayRequest.CARDNO, "4111111111111111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")

request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
request.Set(GatewayRequest.BILLING_STATE, "NV")
request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
request.Set(GatewayRequest.BILLING_COUNTRY, "US")

# Risk/Scrub Request Setting
request.Set(GatewayRequest.SCRUB, "IGNORE")
request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

# Setup test parameters in the service and request.
service.SetTestMode(1)

# Perform the Purchase transaction.
if service.PerformPurchase(request, response):
    print("1. Purchase succeeded")

    # CHECK Rebill Status
    # This would normally be two separate processes,
    # but for example's sake is in one process (thus we clear and set a new GatewayRequest object)
    # The key values required are MERCHANT_CUSTOMER_ID and MERCHANT_INVOICE_ID.
    request = GatewayRequest()
    request.Set(GatewayRequest.MERCHANT_ID, merch_id)
    request.Set(GatewayRequest.MERCHANT_PASSWORD, merch_password)

    request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
    request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

    status = service.PerformRebillUpdate(request, response)
    if status:
        rebill_end_date = response.Get(GatewayResponse.REBILL_END_DATE)

        if rebill_end_date is None:
            print("2. User is Active and Set to Rebill")
            print(" Rebill Date:", response.Get(GatewayResponse.REBILL_DATE))

        else:
            print("2. User is Active and Set to Cancel")
            print(" Cancel Date:", rebill_end_date)

        print(" Join Date:", response.Get(GatewayResponse.JOIN_DATE))
        print(" Join Amount:", response.Get(GatewayResponse.JOIN_AMOUNT))

        print(" Rebill Amount:", response.Get(GatewayResponse.REBILL_AMOUNT))
        print(" Rebill Frequency:", response.Get(GatewayResponse.REBILL_FREQUENCY))
        print(" Rebill Status:", response.Get(GatewayResponse.REBILL_STATUS))

        print(" Last Billing Date:", response.Get(GatewayResponse.LAST_BILLING_DATE))
        print(" Last Billing Amount:", response.Get(GatewayResponse.LAST_BILLING_AMOUNT))
        print(" Last Reason Code:", response.Get(GatewayResponse.LAST_REASON_CODE))

    else:
        print("2. User is Canceled")

else:
    print("1. Purchase failed")
    print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("Exception:", response.Get(GatewayResponse.EXCEPTION))
