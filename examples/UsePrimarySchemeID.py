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

# Allocate the objects we need for the test.
request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

# Setup the original transaction request.
request.Set(GatewayRequest.MERCHANT_ID, "1")
request.Set(GatewayRequest.MERCHANT_PASSWORD, "testpassword")

# For example/testing, we set the order id and customer as the unix timestamp as a convenient sequencing value
# appending a test name to the order id to facilitate some clarity when reviewing the tests
time_value = int(time.time())
inv_id = f"{time_value}.UsePrySchemeID"
request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, f"{time_value}.PythonTest")
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

request.Set(GatewayRequest.AMOUNT, "9.99")
request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.CARDNO, "4111111111111111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")
request.Set(GatewayRequest.IPADDRESS, "127.0.0.1")  # Replace with actual IP

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
service.SetTestMode(True)

# Step 1: Perform an Auth-Only transaction.
if service.PerformAuthOnly(request, response):
    print("Original transaction succeeded")
    print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("Scheme TransactionId:", response.Get(GatewayResponse.SCHEME_TRANSACTION_ID))
    print("Scheme SettlementDate:", response.Get(GatewayResponse.SCHEME_SETTLEMENT_DATE))

    # Compose a request to lookup the invoiceId
    request = GatewayRequest()
    request.Set(GatewayRequest.MERCHANT_ID, "1")
    request.Set(GatewayRequest.MERCHANT_PASSWORD, "testpassword")

    request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

    # Step 2: Perform Lookup to fetch scheme transactionId and settlementDate
    if service.PerformLookup(request, response):
        lookupTransactionId = response.Get(GatewayResponse.SCHEME_TRANSACTION_ID)
        lookupSettlementDate = response.Get(GatewayResponse.SCHEME_SETTLEMENT_DATE)

        print("\nLookup succeeded")
        print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
        print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
        print("Account:", response.Get(GatewayResponse.MERCHANT_ACCOUNT))
        print("Scheme TransactionId:", lookupTransactionId)
        print("Scheme SettlementDate:", lookupSettlementDate)

        # Create a new request to use the scheme transactionId and settlementDate of the original transaction to create an Xsell transaction
        request = GatewayRequest()

        request.Set(GatewayRequest.MERCHANT_ID, "1")
        request.Set(GatewayRequest.MERCHANT_PASSWORD, "testpassword")

        # For example/testing, we set the order id and customer as the unix timestamp as a convenient sequencing value
        # appending a test name to the order id to facilitate some clarity when reviewing the tests
        request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, f"{time_value}.PythonTest")

        time_value += 1
        request.Set(GatewayRequest.MERCHANT_INVOICE_ID, f"{time_value}.UsePrySchemeID")

        request.Set(GatewayRequest.AMOUNT, "3.00")
        request.Set(GatewayRequest.CURRENCY, "USD")
        request.Set(GatewayRequest.CARD_HASH, response.Get(GatewayResponse.CARD_HASH))

        request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
        request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
        request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")
        request.Set(GatewayRequest.IPADDRESS, "127.0.0.1")  # Replace with actual IP

        request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
        request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
        request.Set(GatewayRequest.BILLING_STATE, "NV")
        request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
        request.Set(GatewayRequest.BILLING_COUNTRY, "US")

        # Risk/Scrub Request Setting
        request.Set(GatewayRequest.SCRUB, "IGNORE")
        request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

        # Set necessary parameters required for RocketGate to port previous transaction's scheme transactionId and settlementDate
        request.Set(GatewayRequest.USE_PRIMARY_SCHEMEID, "TRUE")
        request.Set(GatewayRequest.BILLING_TYPE, "T")
        request.Set(GatewayRequest.REFERENCE_SCHEME_TRANSACTION_ID, lookupTransactionId)
        request.Set(GatewayRequest.REFERENCE_SCHEME_SETTLEMENT_DATE, lookupSettlementDate)

        response = GatewayResponse()

        # Step 3: Send a transaction to utilize the scheme transactionId and settlementDate
        if service.PerformAuthOnly(request, response):
            areSchemeTransactionIdSame = (
                "true" if request.Get(GatewayRequest.REFERENCE_SCHEME_TRANSACTION_ID) is None or response.Get(GatewayResponse.SCHEME_TRANSACTION_ID) == lookupTransactionId
                else "false"
            )

            areSchemeSettlementDateSame = (
                "true" if request.Get(GatewayRequest.REFERENCE_SCHEME_SETTLEMENT_DATE) is None or response.Get(GatewayResponse.SCHEME_SETTLEMENT_DATE) == lookupSettlementDate
                else "false"
            )

            print("Xsell transaction succeeded")
            print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
            print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
            print("Lookup & Xsell transaction response Scheme transactionIds are the same?", areSchemeTransactionIdSame)
            print("Lookup & Xsell transaction response Scheme settlementDates are the same?", areSchemeSettlementDateSame)
        else:
            print("Xsell transaction failed")
            print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
            print("Transaction time:", response.Get(GatewayResponse.TRANSACTION_TIME))
            print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
            print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
            print("Exception:", response.Get(GatewayResponse.EXCEPTION))
            print("Scrub:", response.Get(GatewayResponse.SCRUB_RESULTS))
    else:
        print("\nLookup failed")
        print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
        print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
        print("Exception:", response.Get(GatewayResponse.EXCEPTION))
else:
    print("Original transaction failed")
    print("GUID:", response.Get(GatewayResponse.TRANSACT_ID))
    print("Transaction time:", response.Get(GatewayResponse.TRANSACTION_TIME))
    print("Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("Exception:", response.Get(GatewayResponse.EXCEPTION))
    print("Scrub:", response.Get(GatewayResponse.SCRUB_RESULTS))
