#!/usr/bin/env python

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

import unittest
from RocketGate import GatewayRequest
from RocketGate import GatewayResponse
from RocketGate import GatewayService


class ACHTest(unittest.TestCase):
    def get_test_name(self) -> str:
        return "ACHTest"

    def test(self):
        super().setUp()
        self.service = GatewayService()
        self.service.SetTestMode(True)
        self.response = GatewayResponse()
        self.request = GatewayRequest()

        # Merchant data
        self.merchant_id = 1
        self.merchant_password = 'testpassword'
        self.request.Set(GatewayRequest.MERCHANT_ID, self.merchant_id)
        self.request.Set(GatewayRequest.MERCHANT_PASSWORD, self.merchant_password)

        # Provide information about the customer.
        self.request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
        self.request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
        self.request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
        self.request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
        self.request.Set(GatewayRequest.BILLING_STATE, "NV")
        self.request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
        self.request.Set(GatewayRequest.BILLING_COUNTRY, "US")
        self.request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")
        self.request.Set(GatewayRequest.IPADDRESS, "10.10.10.10")

        # Provide information about the purchase.
        self.request.Set(GatewayRequest.AMOUNT, "9.99")

        # Provide information about the bank account.
        # Notes: Accounts default to 'checking account'. If the
        # account is a savings account, set the SAVINGS_ACCOUNT
        # parameter to TRUE.
        # SBW requires the last four digits of the customer's
        # Social Security Number. This is sent in the SS_NUMBER
        # parameter.
        self.request.Set(GatewayRequest.ROUTING_NO, "999999999")
        self.request.Set(GatewayRequest.ACCOUNT_NO, "112233")
        self.request.Set(GatewayRequest.SAVINGS_ACCOUNT, "TRUE")
        self.request.Set(GatewayRequest.SS_NUMBER, "1111")

        # Risk/Scrub Request Setting
        self.request.Set(GatewayRequest.SCRUB, "IGNORE")

        # Perform the Purchase transaction.
        self.assertTrue(
            self.service.PerformPurchase(self.request, self.response),
            "Perform Purchase"
        )


if __name__ == '__main__':
    unittest.main()
