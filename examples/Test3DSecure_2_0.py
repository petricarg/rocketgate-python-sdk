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

from RocketGate import *

# Object instantiation
request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

# Setup the Auth-Only request
request.Set(GatewayRequest.MERCHANT_ID, "1")
request.Set(GatewayRequest.MERCHANT_PASSWORD, "testpassword")

# For example/testing, we set the order id and customer as the unix timestamp as a convenient sequencing value
# appending a test name to the order id to facilitate some clarity when reviewing the tests
current_time = str(int(time.time()))
cust_id = current_time + '.PythonTest'
inv_id = current_time + '.3DSTest'

request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.AMOUNT, "9.99")    # bill 9.99 now

request.Set(GatewayRequest.CARDNO, "4000000000001091")  # This card will trigger a 3DS 2.0 stepUp in the TestProcessor
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

# Request 3DS
request.Set(GatewayRequest.USE_3D_SECURE, "TRUE")
request.Set(GatewayRequest.BROWSER_USER_AGENT, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36")
request.Set(GatewayRequest.BROWSER_ACCEPT_HEADER, "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")

# Setup test parameters in the service and request
service.SetTestMode(True)

# Step 1: Perform the BIN intelligence transaction
service.PerformPurchase(request, response)

response_code = response.Get(GatewayResponse.RESPONSE_CODE)
reason_code = response.Get(GatewayResponse.REASON_CODE)

if (response_code != GatewayCodes.RESPONSE_RISK_FAIL
        and reason_code != GatewayCodes.REASON_3DSECURE_INITIATION):
    print("Response Code:", response_code)
    print("Reason Code:", reason_code)
    exit("error: expected response 2 and reason 225")

print("3DS 2.0 Device Fingerprinting Succeeded!")
print("  Response Code:", response_code)
print("  Reason Code:", reason_code)
print("  Device Fingerprinting URL:", response.Get(GatewayResponse._3DSECURE_DEVICE_COLLECTION_URL))
print("  Device Fingerprinting JWT:", response.Get(GatewayResponse._3DSECURE_DEVICE_COLLECTION_JWT))
print("  Exception:", response.Get(GatewayResponse.EXCEPTION))

# Recycle the first request and add two new fields
request.Set(GatewayRequest._3DSECURE_DF_REFERENCE_ID, "fake")
request.Set(GatewayRequest._3DSECURE_REDIRECT_URL, "fake")

# Step 2: Perform the Lookup transaction
if service.PerformPurchase(request, response):
    print("Purchase succeeded")
    print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    print("Account:", response.Get(GatewayResponse.MERCHANT_ACCOUNT))
    print("Exception:", response.Get(GatewayResponse.EXCEPTION))
elif response.Get(GatewayResponse.REASON_CODE) == GatewayCodes.REASON_3DSECURE_AUTHENTICATION_REQUIRED:
    print("3DS Lookup succeeded")
    print("  GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    print("  3DS Version:", response.Get(GatewayResponse._3DSECURE_VERSION))
    print("  Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("  PAREQ:", response.Get(GatewayResponse.PAREQ))
    print("  ACS URL:", response.Get(GatewayResponse.ACS_URL))
    print("  STEP-UP URL:", response.Get(GatewayResponse._3DSECURE_STEP_UP_URL))
    print("  STEP-UP JWT:", response.Get(GatewayResponse._3DSECURE_STEP_UP_JWT))

    # Setup the 3rd request
    request = GatewayRequest()

    request.Set(GatewayRequest.MERCHANT_ID, "1")
    request.Set(GatewayRequest.MERCHANT_PASSWORD, "testpassword")

    request.Set(GatewayRequest.CVV2, "999")

    request.Set(GatewayRequest.REFERENCE_GUID, response.Get(GatewayResponse.TRANSACT_ID))

    # In a real transaction this would include the PARES returned from the Authentication
    # On dev we send through the SimulatedPARES + TRANSACT_ID
    pares = "SimulatedPARES" + response.Get(GatewayResponse.TRANSACT_ID)
    request.Set(GatewayRequest.PARES, pares)

    # Risk/Scrub Request Setting
    request.Set(GatewayRequest.SCRUB, "IGNORE")
    request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
    request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

    # Step 3: Perform the Purchase transaction
    if service.PerformPurchase(request, response):
        print("Purchase succeeded")
        print("  Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
        print("  Reason Code:", response.Get(GatewayResponse.REASON_CODE))
        print("  GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    else:
        print("Purchase failed")
        print("  GUID:", response.Get(GatewayResponse.TRANSACT_ID))
        print("  Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
        print("  Reason Code:", response.Get(GatewayResponse.REASON_CODE))
        print("  Exception:", response.Get(GatewayResponse.EXCEPTION))
else:
    print("Purchase failed")
    print("  GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    print("  Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("  Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("  Exception:", response.Get(GatewayResponse.EXCEPTION))
