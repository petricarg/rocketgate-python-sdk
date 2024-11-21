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

import sys
import os

from RocketGate import *

"""
Reactivate cancelled subscription example.
"""

# Reactivate canceled subscription example
# MERCHANT_CUSTOMER_ID and MERCHANT_INVOICE_ID associated with the subscription
cust_id = "Client.1657710404894"
inv_id = "Invoice.1657710404894"
merchant_id = "1"
merchant_password = "testpassword"

# Allocate the objects needed for the test
request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

# Set required request parameters to identify the subscription
request.Set(GatewayRequest.MERCHANT_ID, merchant_id)
request.Set(GatewayRequest.MERCHANT_PASSWORD, merchant_password)
request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

# Set REBILL_REACTIVATE parameter TRUE to reactivate subscription
request.Set(GatewayRequest.REBILL_REACTIVATE, "TRUE")

""" 
Optionally, we can set:
    - date to cancel subscription
    request.Set(GatewayRequest.REBILL_END_DATE, "2025-12-31")

    - start date for subscription
    - subscription can start in 3 days
    request.Set(GatewayRequest.REBILL_START, "3")
    
    - or subscription can start at the specified date
    request.Set(GatewayRequest.REBILL_START, "2023-01-17 00:00:00")
"""

# Setup test parameters in the service and request
service.SetTestMode(True)

# Perform PerformRebillUpdate() operation
if service.PerformRebillUpdate(request, response):
    print("Subscription successfully reactivated")
else:
    print("Subscription reactivate failed")
    print("  Response Code:", response.Get(GatewayResponse.RESPONSE_CODE))
    print("  Reason Code:", response.Get(GatewayResponse.REASON_CODE))
    print("  Exception:", response.Get(GatewayResponse.EXCEPTION))
