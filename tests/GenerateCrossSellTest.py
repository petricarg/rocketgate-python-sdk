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
from RocketGate import GatewayRequest, GatewayResponse
import time


class GenerateCrossSellTest(BaseTestCase):
    def get_test_name(self) -> str:
        return "GenerateCrossSellTest"

    def test(self):
        # $3.00 Test
        self.request.Set(GatewayRequest.CURRENCY, "USD")
        self.request.Set(GatewayRequest.AMOUNT, "3.00")               # bill 3.00 now
        self.request.Set(GatewayRequest.REBILL_START, "3")          # Rebill in 3x days
        self.request.Set(GatewayRequest.REBILL_AMOUNT, "9.99")          # Rebill at 9.99
        self.request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")  # ongoing renewals monthly

        self.request.Set(GatewayRequest.USERNAME, "pythontest_user")
        self.request.Set(GatewayRequest.CUSTOMER_PASSWORD, "pythontest_pass")

        # Risk/Scrub Request Setting

        # Perform the Purchase transaction
        self.assertTrue(
            self.service.PerformPurchase(self.request, self.response),
            "Perform Purchase"
        )

        # Update Sticky MID
        #
        # This would normally be two separate processes,
        # but for example's sake is in one process (thus we clear and set a new GatewayRequest object)
        # The key values required are MERCHANT_CUSTOMER_ID and MERCHANT_INVOICE_ID
        #
        request = GatewayRequest()
        request.Set(GatewayRequest.MERCHANT_ID, self.merchant_id)
        request.Set(GatewayRequest.MERCHANT_PASSWORD, self.merchant_password)

        request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, self.customer_id)

        # Different invoice id for xsell.
        request.Set(GatewayRequest.MERCHANT_INVOICE_ID, f"{int(time.time())}.TestGenerateXsell")

        # $1.00 Test
        request.Set(GatewayRequest.CURRENCY, "USD")
        request.Set(GatewayRequest.AMOUNT, "1.00")                # bill $1.00
        request.Set(GatewayRequest.REBILL_START, "4")            # Rebill in 4x days
        request.Set(GatewayRequest.REBILL_AMOUNT, "7.99")        # Rebill at 7.99
        request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")  # ongoing renewals monthly

        self.assertTrue(
            self.service.GenerateXsell(request, self.response),
            "Generate Xsell"
        )


if __name__ == '__main__':
    unittest.main()
