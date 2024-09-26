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

"""
Example $3.00 3x day trial rebills to $9.99 monthly.
 Subsequently, Generate CrossSale for $1 4x day trial rebills $7.99/month
 Requires Merchant Option set: PermitMultipleMemberships=true 
"""

# Setup required and testing variables
time_now = int(time.time())
cust_id = f"{time_now}.PythonTest"
inv_id = f"{time_now}.TestGenerateXsell"
merchant_id = "1"
merchant_password = "testpassword"

# Allocate the objects needed for the test
request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

# Setup the Purchase request
request.Set(GatewayRequest.MERCHANT_ID, merchant_id)
request.Set(GatewayRequest.MERCHANT_PASSWORD, merchant_password)

# Customer and invoice ID setup
request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

# $3.00 3x day trial rebills to $9.99 monthly
request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.AMOUNT, "3.00")
request.Set(GatewayRequest.REBILL_START, "3")
request.Set(GatewayRequest.REBILL_AMOUNT, "9.99")
request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")

# Card details
request.Set(GatewayRequest.CARDNO, "4111111111111111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

# Customer information
request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")
request.Set(GatewayRequest.USERNAME, "pythontest_user")
request.Set(GatewayRequest.CUSTOMER_PASSWORD, "pythontest_pass")

# Setup test mode parameters in service and request
service.SetTestMode(True)

# Perform the Purchase transaction
if service.PerformPurchase(request, response):
    print("Test Purchase succeeded")
    print("CUST:", cust_id)
    print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    print("Account:", response.Get(GatewayResponse.MERCHANT_ACCOUNT))

    # Update Sticky MID
    request = GatewayRequest()
    request.Set(GatewayRequest.MERCHANT_ID, merchant_id)
    request.Set(GatewayRequest.MERCHANT_PASSWORD, merchant_password)
    request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)

    # Different invoice id for xsell
    inv_id = f"{time_now + 1}.TestGenerateXsell"
    request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

    # Generate CrossSale
    request.Set(GatewayRequest.CURRENCY, "USD")
    request.Set(GatewayRequest.AMOUNT, "1.00")
    request.Set(GatewayRequest.REBILL_START, "4")
    request.Set(GatewayRequest.REBILL_AMOUNT, "7.99")
    request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")

    if service.GenerateXsell(request, response):
        print("GenerateXsell Succeeded")
    else:
        print("GenerateXsell Failed")
        print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
else:
    print("Test Purchase Failed!")
    print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("Exception:", response.Get(GatewayResponse.EXCEPTION))
