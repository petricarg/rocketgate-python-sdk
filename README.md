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

## Install RocketGate SDK
```shell
pip install RocketGate
```

## Run examples

Clone this repository and run examples from `./examples` folder 
with `python3 ./examples/AuthOnly.py`

```bash
cd ~
git clone https://github.com/rocketgate/rocketgate-python-sdk
cd ~/rocketgate-python-sdk
python3 ./examples/AuthOnly.py
```


Expect to see output like:

```bash
Auth Only succeeded
GUID:  100019354857297
Response Code:  0
Reason Code:  0
AuthNo:  942499
AVS:  None
CVV2:  None
Card Hash:  8Yz0jmvTGdDaZV9g58L+9mJ+0jw2fodvgktC/jS8GSs=
Card Region:  1,2
Card Description:  CLASSIC
Account:  70
Scrub:  NEGDB=0,PROFILE=0,ACTIVITY=1
```

## Using your local github clone for testing 
If you want to test the modifications of your local version
set `PYTHONPATH` env variable with the path to your 
local repository and you can run examples from `./examples` folder.

```bash
cd ~
git clone https://github.com/rocketgate/rocketgate-python-sdk
cd ~/rocketgate-python-sdk
export PYTHONPATH=~/rocketgate-python-sdk
python3 ./examples/AuthOnly.py
```

Expect to see output like:

```bash
Auth Only succeeded
GUID:  10001935007BB5F
Response Code:  0
Reason Code:  0
AuthNo:  400966
AVS:  None
CVV2:  None
Card Hash:  8Yz0jmvTGdDaZV9g58L+9mJ+0jw2fodvgktC/jS8GSs=
Card Region:  1,2
Card Description:  CLASSIC
Account:  70
Scrub:  NEGDB=0,PROFILE=0,ACTIVITY=1
```