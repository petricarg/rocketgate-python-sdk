import sys
import os
import time
import unittest

# Ensure the RocketGate module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RocketGate import GatewayService, GatewayRequest, GatewayResponse


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.service = GatewayService()
        self.service.SetTestMode(True)
        self.response = GatewayResponse()
        self.request = GatewayRequest()

        self.merchantId: int = 1
        self.merchantPassword: str = 'testpassword'

        # Merchant data
        self.merchant_id = 1
        self.merchant_password = 'testpassword'
        self.request.Set(GatewayRequest.MERCHANT_ID, self.merchant_id)
        self.request.Set(GatewayRequest.MERCHANT_PASSWORD, self.merchant_password)

        # Customer data
        self.request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
        self.request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
        self.request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")

        # Credit card data
        self.request.Set(GatewayRequest.CARDNO, "4111111111111111")
        self.request.Set(GatewayRequest.EXPIRE_MONTH, "02")
        self.request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
        self.request.Set(GatewayRequest.CVV2, "999")

        current_time = str(int(time.time()))
        self.customer_id = current_time + '.PythonTest'
        self.invoice_id = current_time + '.' + self.get_test_name()

        self.request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, self.customer_id)
        self.request.Set(GatewayRequest.MERCHANT_INVOICE_ID, self.invoice_id)

    def get_test_name(self):
        """
        Abstract method to be implemented by subclasses to return the test name.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_service(self):
        return self.service

    def get_request(self):
        return self.request

    def get_response(self):
        return self.response
