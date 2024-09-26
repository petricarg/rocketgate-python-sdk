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
import time
from BaseTestCase import BaseTestCase
from RocketGate import GatewayRequest, GatewayResponse, GatewayCodes


class ThreeDSecureTest(BaseTestCase):
    def get_test_name(self) -> str:
        return "3DSecureTest"

    def test(self):
        current_time = int(time.time())
        cust_id = f"{current_time}.PythonTest"
        inv_id = f"{current_time}.3DSTestiNov24"

        self.request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
        self.request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

        self.request.Set(GatewayRequest.CURRENCY, "USD")
        self.request.Set(GatewayRequest.AMOUNT, "9.99")  # bill 9.99 now

        self.request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
        self.request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
        self.request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")

        self.request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St")
        self.request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
        self.request.Set(GatewayRequest.BILLING_STATE, "NV")
        self.request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
        self.request.Set(GatewayRequest.BILLING_COUNTRY, "US")
        self.request.Set(GatewayRequest.MERCHANT_ACCOUNT, "59")  # 3DS 1.0 MID.

        # Risk/Scrub Request Setting
        self.request.Set(GatewayRequest.SCRUB, "IGNORE")
        self.request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
        self.request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

        # Request 3DS
        self.request.Set(GatewayRequest.USE_3D_SECURE, "TRUE")
        self.request.Set(GatewayRequest.BROWSER_USER_AGENT,
                         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36")
        self.request.Set(GatewayRequest.BROWSER_ACCEPT_HEADER,
                         "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")

        # Perform the Lookup transaction.
        self.service.PerformPurchase(self.request, self.response)
        reason_code = self.response.Get(GatewayResponse.REASON_CODE)  # reason code 202 is expected
        self.assertTrue(reason_code == GatewayCodes.REASON_3DSECURE_AUTHENTICATION_REQUIRED, "Perform 3D Lookup")

        # Setup the 2nd request.
        self.request = GatewayRequest()
        self.request.Set(GatewayRequest.MERCHANT_ID, self.merchant_id)
        self.request.Set(GatewayRequest.MERCHANT_PASSWORD, self.merchant_password)

        self.request.Set(GatewayRequest.CVV2, "999")
        self.request.Set(GatewayRequest.REFERENCE_GUID, self.response.Get(GatewayResponse.TRANSACT_ID))

        # In a real transaction this would include the PARES returned from the Authentication
        # On dev we send through the SimulatedPARES + TRANSACT_ID
        pares = "SimulatedPARES" + self.response.Get(GatewayResponse.TRANSACT_ID)
        self.request.Set(GatewayRequest.PARES, pares)

        # Risk/Scrub Request Setting
        self.request.Set(GatewayRequest.SCRUB, "IGNORE")
        self.request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
        self.request.Set(GatewayRequest.AVS_CHECK, "IGNORE")

        # Perform the Purchase transaction.
        self.assertTrue(
            self.service.PerformPurchase(self.request, self.response),
            "Perform Purchase"
        )


if __name__ == '__main__':
    unittest.main()
