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
from BaseTestCase import BaseTestCase
from RocketGate import GatewayRequest


class UploadTest(BaseTestCase):
    def get_test_name(self) -> str:
        return "UploadTest"

    def test(self):
        # Setting the order id and customer as the unix timestamp as a convenient sequencing value
        # Prepended a test name to the order id to facilitate some clarity when reviewing the tests

        self.request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, "Customer-1")

        self.request.Set(GatewayRequest.CARDNO, "4111111111111111")
        self.request.Set(GatewayRequest.EXPIRE_MONTH, "12")
        self.request.Set(GatewayRequest.EXPIRE_YEAR, "2030")

        self.request.Set(GatewayRequest.CUSTOMER_PASSWORD, "ThePassword")

        self.request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
        self.request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
        self.request.Set(GatewayRequest.BILLING_STATE, "NV")
        self.request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
        self.request.Set(GatewayRequest.BILLING_COUNTRY, "US")

        # Setup test parameters in the service
        self.service.SetTestMode(True)

        # Perform the Purchase transaction
        self.assertTrue(self.service.PerformCardUpload(self.request, self.response), "Perform Card Upload")


if __name__ == '__main__':
    unittest.main()
