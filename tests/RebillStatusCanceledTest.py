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
from RocketGate import GatewayRequest, GatewayResponse, GatewayCodes


class RebillStatusCanceledTest(BaseTestCase):
    def get_test_name(self) -> str:
        return "RebillStatusCanceledTest"

    def test(self):
        # $9.99/month subscription
        self.request.Set(GatewayRequest.CURRENCY, "USD")
        self.request.Set(GatewayRequest.AMOUNT, "9.99")  # bill 9.99 now
        self.request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")  # ongoing renewals monthly

        self.request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
        self.request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
        self.request.Set(GatewayRequest.BILLING_STATE, "NV")
        self.request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
        self.request.Set(GatewayRequest.BILLING_COUNTRY, "US")

        self.request.Set(GatewayRequest.SCRUB, "IGNORE")
        self.request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
        self.request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

        # Perform the Purchase transaction
        self.assertTrue(self.service.PerformPurchase(self.request, self.response), "Perform Purchase")

        # Cancel Rebill
        # This would normally be two separate processes,
        # but for example's sake is in one process (thus we clear and set a new GatewayRequest object)
        # The key values required are MERCHANT_CUSTOMER_ID and MERCHANT_INVOICE_ID.
        request = GatewayRequest()
        request.Set(GatewayRequest.MERCHANT_ID, self.merchant_id)
        request.Set(GatewayRequest.MERCHANT_PASSWORD, self.merchant_password)
        request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, self.customer_id)
        request.Set(GatewayRequest.MERCHANT_INVOICE_ID, self.invoice_id)

        self.assertTrue(self.service.PerformRebillCancel(request, self.response), "Cancel Rebill")

        # CHECK Rebill Status
        request = GatewayRequest()
        request.Set(GatewayRequest.MERCHANT_ID, self.merchant_id)
        request.Set(GatewayRequest.MERCHANT_PASSWORD, self.merchant_password)
        request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, self.customer_id)
        request.Set(GatewayRequest.MERCHANT_INVOICE_ID, self.invoice_id)

        if self.service.PerformRebillUpdate(request, self.response):
            self.assertIsNotNone(self.response.Get(GatewayResponse.REBILL_END_DATE), "User is active and set to cancel")
        else:
            self.assertEqual(GatewayCodes.REASON_NO_ACTIVE_MEMBERSHIP,
                             self.response.Get(GatewayResponse.REASON_CODE),
                             "Canceled subscription")


if __name__ == '__main__':
    unittest.main()
