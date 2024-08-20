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


class PurchaseRebillTest(BaseTestCase):
    def get_test_name(self) -> str:
        return "PurchaseRebillTest"

    def test(self):
        # $1.99 3-day trial which renews to $9.99/month
        self.request.Set(GatewayRequest.CURRENCY, "USD")
        self.request.Set(GatewayRequest.AMOUNT, "1.99")  # bill 1.99 trial now
        self.request.Set(GatewayRequest.REBILL_START, "3")  # renew in 3 days
        self.request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")  # ongoing renewals monthly
        self.request.Set(GatewayRequest.REBILL_AMOUNT, "9.99")

        self.request.Set(GatewayRequest.IPADDRESS, '72.229.28.185')

        self.request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
        self.request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
        self.request.Set(GatewayRequest.BILLING_STATE, "NV")
        self.request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
        self.request.Set(GatewayRequest.BILLING_COUNTRY, "US")

        # Risk/Scrub Request Setting
        self.request.Set(GatewayRequest.SCRUB, "IGNORE")
        self.request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
        self.request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

        # Perform the Purchase transaction
        self.assertTrue(
            self.service.PerformPurchase(self.request, self.response),
            "Perform Purchase"
        )


if __name__ == '__main__':
    unittest.main()
