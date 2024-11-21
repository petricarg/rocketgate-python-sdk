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

from RocketGate import *

"""
Example Scenario:
 $9.99 USD purchase.
 Subsequently, the user wants to make another $8.99 purchase using the card on file (PayInfo Token)
"""

# Generate the required variables for the test
time = int(time.time())
cust_id = f"{time}.PythonTest"
inv_id = f"{time}.PayInfoTest"
merchant_id = "1"
merchant_password = "testpassword"

# Initialize the objects required for the test
request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

# Set up the Purchase request
request.Set(GatewayRequest.MERCHANT_ID, merchant_id)
request.Set(GatewayRequest.MERCHANT_PASSWORD, merchant_password)
request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)
request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.AMOUNT, "9.99")

# Card details
request.Set(GatewayRequest.CARDNO, "4111111111111111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

# Customer details
request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.EMAIL, "pythontester@fakedomain.com")

# Billing address
request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
request.Set(GatewayRequest.BILLING_STATE, "NV")
request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
request.Set(GatewayRequest.BILLING_COUNTRY, "US")

# Risk/Scrub settings
request.Set(GatewayRequest.SCRUB, "IGNORE")
request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

# Test mode setup
service.SetTestMode(True)

# Perform the Purchase transaction
if service.PerformPurchase(request, response):
    print("Initial Purchase succeeded")
    print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))

    # Get the PayInfo Token for the next transaction
    payinfo_transact_id = response.Get(GatewayResponse.TRANSACT_ID)

    # Run an additional purchase using the PayInfo Token
    secondary_request = GatewayRequest()
    secondary_request.Set(GatewayRequest.MERCHANT_ID, merchant_id)
    secondary_request.Set(GatewayRequest.MERCHANT_PASSWORD, merchant_password)
    secondary_request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
    secondary_request.Set(GatewayRequest.PAYINFO_TRANSACT_ID, payinfo_transact_id)
    secondary_request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)
    secondary_request.Set(GatewayRequest.AMOUNT, "8.99")
    
    if service.PerformPurchase(secondary_request, response):
        print("PayInfo Purchase succeeded")
        print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    else:
        print("PayInfo Purchase failed")
else:
    print("Initial Purchase failed")
    print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("Exception:", response.Get(GatewayResponse.EXCEPTION))
    print("Scrub:", response.Get(GatewayResponse.SCRUB_RESULTS))
