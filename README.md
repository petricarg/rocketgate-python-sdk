![rocketgate-python-sdk](http://rocketgate.com/images/logo_rocketgate.png)

RocketGate Gateway Python SDK
===========

The Python 3.x Software Development Kit and Test Scripts

Documentation is available in RocketGate's helpdesk at https://help.rocketgate.com/support/solutions/28000015702

Docs related to this repository are located at:

1. GatewayService: https://help.rocketgate.com/support/solutions/articles/28000018238-gatewayservice
2. GatewayRequest: https://help.rocketgate.com/support/solutions/articles/28000018237-gatewayrequest
3. GatewayResponse: https://help.rocketgate.com/support/solutions/articles/28000018236-gatewayresponse
4. GatewayResponse Error / Decline Codes: https://help.rocketgate.com/support/solutions/articles/28000018169-gatewayresponse-error-decline-codes


## Running integration tests
From the root of the project, using your installed Python Interpreter, run the following command:
```shell
python3 -m unittest discover ./tests -p '*.py'
```