""""
Copyright notice:
(c) Copyright 2024 RocketGate
All rights reserved.

The copyright notice must not be removed without specific, prior
written permission from RocketGate.

This software is protected as an unpublished work under the U.S. copyright
laws. The above copyright notice is not intended to effect a publication of
this work.
This software is the confidential and proprietary information of RocketGate.
Neither the binaries nor the source code may be redistributed without prior
written permission from RocketGate.

The software is provided "as-is" and without warranty of any kind, express, implied
or otherwise, including without limitation, any warranty of merchantability or fitness
for a particular purpose.  In no event shall RocketGate be liable for any direct,
special, incidental, indirect, consequential or other damages of any kind, or any damages
whatsoever arising out of or in connection with the use or performance of this software,
including, without limitation, damages resulting from loss of use, data or profits, and
whether or not advised of the possibility of damage, regardless of the theory of liability.
"""

import xml.sax
import http.client
import random
import socket
import ssl
from urllib.parse import urlsplit


class GatewayRequest:
    VERSION_INDICATOR = "version"
    VERSION_NUMBER = "PY3.6"

    ######################################################################
    #
    #	Define constant hash values.
    #
    ######################################################################

    ACCOUNT_HOLDER = "accountHolder"
    ACCOUNT_NO = "accountNo"
    AFFILIATE = "affiliate"
    ALLOW_CARD_DEBIT_CREDIT = "ALLOW_CARD_DEBIT_CREDIT"
    AMOUNT = "amount"
    AVS_CHECK = "avsCheck"
    BILLING_ADDRESS = "billingAddress"
    BILLING_CITY = "billingCity"
    BILLING_COUNTRY = "billingCountry"
    BILLING_STATE = "billingState"
    BILLING_TYPE = "billingType"
    BILLING_ZIPCODE = "billingZipCode"
    BROWSER_ACCEPT_HEADER = "browserAcceptHeader"
    BROWSER_COLOR_DEPTH = "BrowserColorDepth"
    BROWSER_JAVA_ENABLED = "BrowserJavaEnabled"
    BROWSER_LANGUAGE = "BrowserLanguage"
    BROWSER_SCREEN_HEIGHT = "BrowserScreenHeight"
    BROWSER_SCREEN_WIDTH = "BrowserScreenWidth"
    BROWSER_TIME_ZONE = "BrowserTimeZone"
    BROWSER_USER_AGENT = "browserUserAgent"
    CAPTURE_DAYS = "captureDays"
    CARDNO = "cardNo"
    CARD_HASH = "cardHash"
    CLONE_CUSTOMER_RECORD = "cloneCustomerRecord"
    CLONE_TO_CUSTOMER_ID = "cloneToCustomerID"
    COF_FRAMEWORK = "cofFramework"
    CURRENCY = "currency"
    CUSTOMER_FIRSTNAME = "customerFirstName"
    CUSTOMER_LASTNAME = "customerLastName"
    CUSTOMER_PASSWORD = "customerPassword"
    CUSTOMER_PHONE_NO = "customerPhoneNo"
    CVV2 = "cvv2"
    CVV2_CHECK = "cvv2Check"
    EMAIL = "email"
    EMBEDDED_FIELDS_TOKEN = "embeddedFieldsToken"
    EXPIRE_MONTH = "expireMonth"
    EXPIRE_YEAR = "expireYear"
    FAILED_GUID = "failedGUID"
    FAILED_REASON_CODE = "failedReasonCode"
    FAILED_RESPONSE_CODE = "failedResponseCode"
    FAILED_SERVER = "failedServer"
    FAILURE_URL = "FAILUREURL"
    GATEWAY_CONNECT_TIMEOUT = "gatewayConnectTimeout"
    GATEWAY_PORTNO = "gatewayPortNo"
    GATEWAY_PROTOCOL = "gatewayProtocol"
    GATEWAY_READ_TIMEOUT = "gatewayReadTimeout"
    GATEWAY_SERVER = "gatewayServer"
    GATEWAY_SERVLET = "gatewayServlet"
    GATEWAY_URL = "gatewayURL"
    GENERATE_POSTBACK = "generatePostback"
    GOOGLE_PAY_TOKEN = "GOOGLEPAYTOKEN"
    IOVATION_BLACK_BOX = "iovationBlackBox"
    IOVATION_RULE = "iovationRule"
    IPADDRESS = "ipAddress"
    LANGUAGE = "LANGUAGE"
    MERCHANT_ACCOUNT = "merchantAccount"
    MERCHANT_CASCADED_AUTH = "MERCHANTCASCADEDAUTH"
    MERCHANT_CUSTOMER_ID = "merchantCustomerID"
    MERCHANT_DESCRIPTOR = "merchantDescriptor"
    MERCHANT_DESCRIPTOR_CITY = "merchantDescriptorCity"
    MERCHANT_DESCRIPTOR_TRIAL = "merchantDescriptorTrial"
    MERCHANT_ID = "merchantID"
    MERCHANT_INVOICE_ID = "merchantInvoiceID"
    MERCHANT_PASSWORD = "merchantPassword"
    MERCHANT_PRODUCT_ID = "merchantProductID"
    MERCHANT_SITE_ID = "merchantSiteID"
    OMIT_RECEIPT = "omitReceipt"
    ONCLICK_LOGO_URL = "onClickLogoURL"
    PARES = "PARES"
    PARTIAL_AUTH_FLAG = "partialAuthFlag"
    PAYINFO_TRANSACT_ID = "payInfoTransactID"
    PAYMENT_LINK_TOKEN = "PAYMENTLINKTOKEN"
    PREFERRED_MERCHANT_ACCOUNT = "preferredMerchantAccount"
    PROCESSOR_3DS = "PROCESSOR3DS"
    REBILL_AMOUNT = "rebillAmount"
    REBILL_COUNT = "rebillCount"
    REBILL_END_DATE = "rebillEndDate"
    REBILL_FREQUENCY = "rebillFrequency"
    REBILL_REACTIVATE = "REBILLREACTIVATE"
    REBILL_RESCHEDULE = "REBILLRESCHEDULE"
    REBILL_RESUME = "rebillResume"
    REBILL_START = "rebillStart"
    REBILL_SUSPEND = "rebillSuspend"
    REFERENCE_GUID = "referenceGUID"
    REFERENCE_SCHEME_SETTLEMENT_DATE = "schemeSettleDate"
    REFERENCE_SCHEME_TRANSACTION_ID = "schemeTranId"
    REFERRAL_NO = "referralNo"
    REFERRED_CUSTOMER_ID = "referredCustomerID"
    REFERRER_URL = "referrerURL"
    REFERRING_MERCHANT_ID = "referringMerchantID"
    ROUTING_NO = "routingNo"
    SAVINGS_ACCOUNT = "savingsAccount"
    SCRUB = "scrub"
    SCRUB_ACTIVITY = "scrubActivity"
    SCRUB_NEGDB = "scrubNegDB"
    SCRUB_PROFILE = "scrubProfile"
    SHOW_PAYMENT_FORM = "SHOW_PAYMENT_FORM"
    SS_NUMBER = "ssNumber"
    STYLE_SHEET = "style"
    STYLE_SHEET2 = "style2"
    STYLE_SHEET3 = "style3"
    SUB_MERCHANT_ID = "subMerchantID"
    SUCCESS_URL = "SUCCESSURL"
    THREATMETRIX_SESSION_ID = "threatMetrixSessionID"
    TRANSACTION_TYPE = "transactionType"
    TRANSACT_ID = REFERENCE_GUID
    TRANSLATIONS = "translations"
    UDF01 = "udf01"
    UDF02 = "udf02"
    USERNAME = "username"
    USE_3D_SECURE = "use3DSecure"
    USE_PRIMARY_SCHEMEID = "usePrimarySchemeID"
    XSELL_CUSTOMER_ID = "xsellCustomerID"
    XSELL_MERCHANT_ACCOUNT = "xsellMerchantAccount"
    XSELL_MERCHANT_ID = "xsellMerchantID"
    XSELL_REFERENCE_XACT = "xsellReferenceXact"
    _3DSECURE_ACS_TRANSACTION_ID = "_3DSECURE_ACS_TRANSACTION_ID"
    _3DSECURE_ACS_WINDOW_SIZE = "_3DSECURE_ACS_WINDOW_SIZE"
    """
    An override field that a merchant can pass in to set the challenge window size to display to the end cardholder.
    
    The ACS will reply with content that is formatted appropriately to this window size to allow for the best user 
    experience.
    
    The sizes are width x height in pixels of the window displayed in the cardholder browser window.
    
    The possible values are:
    
    - 01 (250x400)
    - 02 (390x400)
    - 03 (500x600)
    - 04 (600x400)
    - 05 (Full page)
    """
    _3DSECURE_CHALLENGE_MANDATED_INDICATOR = "_3DSECURE_CHALLENGE_MANDATED_INDICATOR"
    _3DSECURE_DF_REFERENCE_ID = "_3DSECURE_DF_REFERENCE_ID"
    _3DSECURE_DS_TRANSACTION_ID = "_3DSECURE_DS_TRANSACTION_ID"
    _3DSECURE_LOOKUP_CHALLENGE_INDICATOR = "_3DSECURE_LOOKUP_CHALLENGE_INDICATOR"
    """
    Whether or not to request a challenge step-up flow from the ACS 
    
    - 01 - No preference
    - 02 - No challenge requested
    - 03 - Challenge requested (3DS Requestor Preference)
    - 04 - Challenge requested (Mandate)
    """
    _3DSECURE_REDIRECT_URL = "_3DSECURE_REDIRECT_URL"
    _3DSECURE_THREE_DS_SERVER_TRANSACTION_ID = "_3DSECURE_THREE_DS_SERVER_TRANSACTION_ID"
    _3D_CAVV_ALGORITHM = "THREEDCAVVALGORITHM"
    _3D_CAVV_UCAF = "ThreeDCavvUcaf"
    _3D_CHECK = "ThreeDCheck"
    _3D_ECI = "ThreeDECI"
    _3D_PARESSTATUS = "THREEDPARESSTATUS"
    _3D_VERSION = "THREEDVERSION"
    _3D_VERSTATUS = "THREEDVERSTATUS"
    _3D_XID = "ThreeDXID"

    def __init__(self):
        """Constructor for class."""

        self.parameterList = {}
        self.Set(GatewayRequest.VERSION_INDICATOR, GatewayRequest.VERSION_NUMBER)

    def Set(self, key, value):
        """Sets a value in the parameter list."""

        self.Clear(key)  # Have key value? Delete it
        self.parameterList[key] = str(value)  # Save the value

    def Clear(self, key):
        """Clears a value in the parameter list."""

        if key in self.parameterList:  # Have key value?
            del self.parameterList[key]  # Delete it

    def Get(self, key):
        """Gets a value from the parameter list."""

        if key in self.parameterList:  # Have key value?
            return self.parameterList[key]  # Return the value
        return None  # Don't have a value

    def ToXML(self):
        """Creates an XML document from the hash list."""

        #
        #	Build the document header.
        #
        xmlDocument = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        xmlDocument += "<gatewayRequest>"

        #
        #	Loop over each key-value pairs and create
        #	and open tag for the key.
        #
        for key, value in self.parameterList.items():
            xmlDocument += "<"
            xmlDocument += key
            xmlDocument += ">"

            #
            #	Clean up the value and add it to the tag.
            #
            myValue = str(value)  # In case it's not a string
            myValue = myValue.replace("&", "&amp;")
            myValue = myValue.replace("<", "&lt;")
            myValue = myValue.replace(">", "&gt;")
            xmlDocument += myValue

            #
            #
            #	Add the closing tag for this element.
            #
            xmlDocument += "</"
            xmlDocument += key
            xmlDocument += ">"

        #
        #	Close and return the document.
        #
        xmlDocument += "</gatewayRequest>"
        return xmlDocument  # Final document


class GatewayResponse(xml.sax.handler.ContentHandler):

    VERSION_INDICATOR = "version"

    ######################################################################
    #
    #	Define constant hash values.
    #
    ######################################################################

    ACS_URL = "acsURL"
    AUTH_NO = "authNo"
    AVS_RESPONSE = "avsResponse"
    BALANCE_AMOUNT = "balanceAmount"
    BALANCE_CURRENCY = "balanceCurrency"
    BANK_RESPONSE_CODE = "bankResponseCode"
    BILLING_ADDRESS = "billingAddress"
    BILLING_CITY = "billingCity"
    BILLING_COUNTRY = "billingCountry"
    BILLING_STATE = "billingState"
    BILLING_ZIPCODE = "billingZipCode"
    CARD_BIN = "cardBin"
    CARD_COUNTRY = "cardCountry"
    CARD_DEBIT_CREDIT = "cardDebitCredit"
    CARD_DESCRIPTION = "cardDescription"
    CARD_EXPIRATION = "cardExpiration"
    CARD_HASH = "cardHash"
    CARD_ISSUER_NAME = "cardIssuerName"
    CARD_ISSUER_PHONE = "cardIssuerPhone"
    CARD_ISSUER_URL = "cardIssuerURL"
    CARD_LAST_FOUR = "cardLastFour"
    CARD_REGION = "cardRegion"
    CARD_TYPE = "cardType"
    CAVV_RESPONSE = "cavvResponse"
    CUSTOMER_FIRSTNAME = "customerFirstName"
    CUSTOMER_LASTNAME = "customerLastName"
    CVV2_CODE = "cvv2Code"
    ECI = "ECI"
    EMAIL = "email"
    EXCEPTION = "exception"
    IOVATION_DEVICE = "IOVATIONDEVICE"
    IOVATION_RESULTS = "IOVATIONRESULTS"
    IOVATION_RULE_COUNT = "IOVATIONRULECOUNT"
    IOVATION_RULE_REASON_ = "IOVATIONRULEREASON_"
    IOVATION_RULE_SCORE_ = "IOVATIONRULESCORE_"
    IOVATION_RULE_TYPE_ = "IOVATIONRULETYPE_"
    IOVATION_SCORE = "IOVATIONSCORE"
    IOVATION_TRACKING_NO = "IOVATIONTRACKINGNO"
    IS_BANK_HARD_DECLINE = "isBankHardDecline"
    JOIN_AMOUNT = "joinAmount"
    JOIN_DATE = "joinDate"
    LAST_BILLING_AMOUNT = "lastBillingAmount"
    LAST_BILLING_DATE = "lastBillingDate"
    LAST_REASON_CODE = "lastReasonCode"
    MERCHANT_ACCOUNT = "merchantAccount"
    MERCHANT_ADVICE_CODE = "merchantAdviceCode"
    MERCHANT_CUSTOMER_ID = "merchantCustomerID"
    MERCHANT_INVOICE_ID = "merchantInvoiceID"
    MERCHANT_PRODUCT_ID = "merchantProductID"
    MERCHANT_SITE_ID = "merchantSiteID"
    PAREQ = "PAREQ"
    PARES = "PARES"
    PAYMENT_LINK_URL = "PAYMENT_LINK_URL"
    PAY_HASH = CARD_HASH
    PAY_LAST_FOUR = CARD_LAST_FOUR
    PAY_TYPE = "payType"
    PROCESSOR_3DS = "PROCESSOR3DS"
    REASON_CODE = "reasonCode"
    REBILL_AMOUNT = "rebillAmount"
    REBILL_CURRENCY = "rebillCurrency"
    REBILL_DATE = "rebillDate"
    REBILL_END_DATE = "rebillEndDate"
    REBILL_FREQUENCY = "rebillFrequency"
    REBILL_STATUS = "rebillStatus"
    RESPONSE_CODE = "responseCode"
    RETRIEVAL_ID = "retrievalNo"
    ROCKETPAY_INDICATOR = "rocketPayIndicator"
    SCHEME_SETTLEMENT_DATE = "schemeSettlementDate"
    SCHEME_TRANSACTION_ID = "schemeTransactionID"
    SCRUB_RESULTS = "scrubResults"
    SETTLED_AMOUNT = "approvedAmount"
    SETTLED_CURRENCY = "approvedCurrency"
    TRANSACTION_TIME = "transactionTime"
    TRANSACT_ID = "guidNo"
    _3DSECURE_ACS_TRANSACTION_ID = "_3DSECURE_ACS_TRANSACTION_ID"
    _3DSECURE_CAVV_ALGORITHM = "_3DSECURE_CAVV_ALGORITHM"
    _3DSECURE_CAVV_UCAF = "_3DSECURE_CAVV_UCAF"
    _3DSECURE_CHALLENGE_MANDATED_INDICATOR = "_3DSECURE_CHALLENGE_MANDATED_INDICATOR"
    _3DSECURE_DEVICE_COLLECTION_JWT = "_3DSECURE_DEVICE_COLLECTION_JWT"
    _3DSECURE_DEVICE_COLLECTION_URL = "_3DSECURE_DEVICE_COLLECTION_URL"
    _3DSECURE_DS_TRANSACTION_ID = "_3DSECURE_DS_TRANSACTION_ID"
    _3DSECURE_LOOKUP_CHALLENGE_INDICATOR = "_3DSECURE_LOOKUP_CHALLENGE_INDICATOR"
    _3DSECURE_LOOKUP_REFERENCE_GUID = "_3DSECURE_LOOKUP_REFERENCE_GUID"
    _3DSECURE_LOOKUP_SIGNATURE = "_3DSECURE_LOOKUP_SIGNATURE"
    _3DSECURE_PARESSTATUS = "_3DSECURE_PARESSTATUS"
    _3DSECURE_STEP_UP_JWT = "_3DSECURE_STEP_UP_JWT"
    _3DSECURE_STEP_UP_URL = "_3DSECURE_STEP_UP_URL"
    _3DSECURE_THREE_DS_SERVER_TRANSACTION_ID = "_3DSECURE_THREE_DS_SERVER_TRANSACTION_ID"
    _3DSECURE_VERSION = "_3DSECURE_VERSION"
    _3DSECURE_VERSTATUS = "_3DSECURE_VERSTATUS"
    _3DSECURE_XID = "_3DSECURE_XID"

    def __init__(self):
        """Constructor for class."""

        self.parameterList = {}  # Fresh list
        self.haveOpenTag = 0  # Haven't seen <gatewayResponse>
        self.valueBuffer = ""  # No value yet

    def Set(self, key, value):
        """Sets a value in the parameter list."""

        if key in self.parameterList:  # Have key value?
            del self.parameterList[key]  # Delete it
        self.parameterList[key] = str(value)  # Save the value

    def Reset(self):
        """Clears all elements in a response."""

        del self.parameterList  # Kill old list
        self.parameterList = {}  # Start with fresh list

    def Get(self, key):
        """Gets a value from the parameter list."""

        if key in self.parameterList:  # Have key value?
            return self.parameterList[key]  # Return the value
        return None  # Don't have a value

    def SetFromXML(self, xmlDocument):
        """Sets values in a response object using an XML document."""

        #
        #	Initialize the parsing.
        #
        self.haveOpenTag = 0  # Haven't tried to open
        self.valueBuffer = ""  # No value yet

        #
        #	Parse the input string.
        #
        try:
            xml.sax.parseString(xmlDocument, self)

        #
        #	If there was a parsing error, set the error codes and quit.
        #
        except xml.sax.SAXException as ex:
            self.Set(GatewayResponse.EXCEPTION, ex.getMessage() + ": " + xmlDocument)
            self.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_REQUEST_ERROR)
            self.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_XML_ERROR)

        #
        #	If there was some other type of exception, set the error codes and quit.
        #
        except:
            self.Set(GatewayResponse.EXCEPTION, "Unhandled exception: " + xmlDocument)
            self.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
            self.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_BUGCHECK)

    def startElement(self, name, attrs):
        """Handler for start of XML element."""

        if name == "gatewayResponse":  # Opening of document?
            self.haveOpenTag = 1  # Have seen open tag
        self.valueBuffer = ""  # Start with clean value

    def characters(self, data):
        """Handler for element string"""

        if self.haveOpenTag:  # Seen open yet?
            self.valueBuffer += data

    def endElement(self, name):
        """Handler for end of XML element."""

        if name != "gatewayResponse":  # Opening of document?
            self.Set(name, self.valueBuffer)


class GatewayService:
    ######################################################################
    #
    #	Define constants
    #
    ######################################################################

    ROCKETGATE_SERVLET = "/gateway/servlet/ServiceDispatcherAccess"
    ROCKETGATE_CONNECT_TIMEOUT = 10
    ROCKETGATE_READ_TIMEOUT = 90
    ROCKETGATE_PORTNO = 443
    ROCKETGATE_USER_AGENT = "RG Client - Python " + str(GatewayRequest.VERSION_NUMBER)

    LIVE_HOST = "gateway.rocketgate.com"
    LIVE_HOST_16 = "gateway-16.rocketgate.com"
    LIVE_HOST_17 = "gateway-17.rocketgate.com"

    TEST_HOST = "dev-gateway.rocketgate.com"

    def __init__(self):
        """Constructor for class."""

        self.testMode = 0  # Default to live
        self.rocketGateHost = GatewayService.LIVE_HOST
        self.rocketGateServlet = GatewayService.ROCKETGATE_SERVLET
        self.rocketGatePortNo = GatewayService.ROCKETGATE_PORTNO
        self.rocketGateConnectTimeout = GatewayService.ROCKETGATE_CONNECT_TIMEOUT
        self.rocketGateReadTimeout = GatewayService.ROCKETGATE_READ_TIMEOUT

    def SetTestMode(self, yesNo):
        """Selects test/development mode."""

        if yesNo:  # Setting test mode?
            self.testMode = 1  # Set to test mode
            del self.rocketGateHost  # Delete old host list
            self.rocketGateHost = GatewayService.TEST_HOST
        else:
            self.testMode = 0  # Set to live mode
            del self.rocketGateHost  # Delete old host list
            self.rocketGateHost = GatewayService.LIVE_HOST

    def SetHost(self, hostName):
        """Sets the host used by the service"""

        del self.rocketGateHost  # Delete old host list
        self.rocketGateHost = hostName  # Use this host

    def SetPortNo(self, portNo):
        """Sets the port number used by the service."""

        try:
            value = int(portNo)  # Get numeric value
            if value > 0:  # Have a valid value?
                self.rocketGatePortNo = value
        except:
            pass

    def SetServlet(self, servlet):
        """Sets servlet used by the service."""

        self.rocketGateServlet = servlet  # End point

    def SetConnectTimeout(self, timeout):
        """Sets connection timeout"""

        try:
            value = int(timeout)  # Get numeric value
            if value > 0:  # Have a valid value?
                self.rocketGateConnectTimeout = value
        except:
            pass

    def SetReadTimeout(self, timeout):
        """Sets read timeout"""

        try:
            value = int(timeout)  # Get numeric value
            if value > 0:  # Have a valid value?
                self.rocketGateReadTimeout = value
        except:
            pass

    def SendTransaction(self, serverName, request, response):
        """Sends a transaction to a named host."""

        #
        #	Gather overrides for transaction.
        #
        connection = None
        urlServlet = request.Get(GatewayRequest.GATEWAY_SERVLET)
        urlPortNo = request.Get(GatewayRequest.GATEWAY_PORTNO)

        #
        #	Determine the final servlet name.
        #
        if urlServlet is None:  # None specified?
            urlServlet = self.rocketGateServlet

        #
        #	Determine the final port number.
        #
        if urlPortNo is None:
            urlPortNo = self.rocketGatePortNo
        else:
            try:
                int(urlPortNo)  # Make sure this is numeric
            except:
                urlPortNo = self.rocketGatePortNo

        #
        #	Get the connection timeout.
        #
        connectTimeout = request.Get("gatewayConnectTimeout")
        if connectTimeout is None:
            connectTimeout = self.rocketGateConnectTimeout
        else:
            try:
                int(connectTimeout)  # Make sure this is numeric
            except:
                connectTimeout = self.rocketGateConnectTimeout

        #
        #	Get the read timeout.
        #
        readTimeout = request.Get("gatewayReadTimeout")
        if readTimeout is None:
            readTimeout = self.rocketGateReadTimeout
        else:
            try:
                int(readTimeout)  # Make sure this is numeric
            except:
                readTimeout = self.rocketGateReadTimeout

        #
        #	Prepare the values that will go into the post operation.
        #
        response.Reset()  # Clear any response data
        requestXML = request.ToXML()  # Get message string
        headers = {"Content-Type": "text/xml", "User-Agent": GatewayService.ROCKETGATE_USER_AGENT}

        #
        #	Create the HTTP handler and post our request.
        #
        try:
            connection = http.client.HTTPSConnection(serverName, urlPortNo, timeout=connectTimeout)
            connection.request("POST", urlServlet, requestXML, headers)
            connection.sock.settimeout(readTimeout)

            #
            #	Read the response.
            #
            results = connection.getresponse()
            body = results.read()  # Get the response data
            if isinstance(body, bytes):
                body = body.decode("utf-8")

            #
            #	If the response was not '200 OK', we must quit
            #
            if results.status != 200:
                response.Set(GatewayResponse.EXCEPTION, str(results.status) + ": " + body)
                response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
                response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_RESPONSE_READ_ERROR)
                return GatewayCodes.RESPONSE_SYSTEM_ERROR  # System error

        #
        #	If there was a timeout, return an error.
        #
        except socket.timeout as ex:
            response.Set(GatewayResponse.EXCEPTION, str(ex))
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_UNABLE_TO_CONNECT)
            return GatewayCodes.RESPONSE_SYSTEM_ERROR  # System error

        #
        #	If the read timed out, return an error.
        #
        except ssl.SSLError as ex:
            response.Set(GatewayResponse.EXCEPTION, str(ex))
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_RESPONSE_READ_TIMEOUT)
            return GatewayCodes.RESPONSE_SYSTEM_ERROR  # System error

        #
        #	If there was some other type of socket problem, return an error.
        #
        except socket.error as ex:
            response.Set(GatewayResponse.EXCEPTION, str(ex))
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
            exString = str(ex)
            if 'Connection refused' in exString:
                response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_UNABLE_TO_CONNECT)
            else:
                response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_RESPONSE_READ_ERROR)
            return GatewayCodes.RESPONSE_SYSTEM_ERROR  # System error

        #
        #	Catch general exceptions.
        #
        except Exception as ex:
            response.Set(GatewayResponse.EXCEPTION, str(ex))
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_RESPONSE_READ_ERROR)
            return GatewayCodes.RESPONSE_SYSTEM_ERROR  # System error

        #
        #	Other exceptions must be caught too.
        #
        except:
            response.Set(GatewayResponse.EXCEPTION, "Unhandled POST exception")
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_RESPONSE_READ_ERROR)
            return GatewayCodes.RESPONSE_SYSTEM_ERROR  # System error

        #
        #	Clean up the connection when we are all done.
        #
        finally:
            if connection is not None:
                connection.close()  # Done with connection

        #
        #	Parse the response XML and return the response code.
        #
        response.SetFromXML(body)  # Set from response body

        response_code = response.Get(GatewayResponse.RESPONSE_CODE)
        reason_code = response.Get(GatewayResponse.REASON_CODE)

        if response_code is None or reason_code is None:
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_REQUEST_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_XML_ERROR)

        return response.Get(GatewayResponse.RESPONSE_CODE)  # Give back results

    def PerformTransaction(self, request, response):
        """Performs the transaction described in a gateway request."""

        #
        #	If EMBEDDED_FIELDS_TOKEN is provided, send the request to the corresponding endpoint
        #
        fullUrl = request.Get(GatewayRequest.GATEWAY_URL)
        if fullUrl is None:
            if request.Get(GatewayRequest.PAYMENT_LINK_TOKEN) is not None:
                fullUrl = request.Get(GatewayRequest.PAYMENT_LINK_TOKEN)
            elif request.Get(GatewayRequest.EMBEDDED_FIELDS_TOKEN) is not None:
                fullUrl = request.Get(GatewayRequest.EMBEDDED_FIELDS_TOKEN)

        if fullUrl is not None:
            try:
                parsedUrl = urlsplit(fullUrl)
                request.Set(GatewayRequest.GATEWAY_SERVER, parsedUrl.hostname)
                request.Set(GatewayRequest.GATEWAY_SERVLET,
                            parsedUrl.path + ("?" + parsedUrl.query if parsedUrl.query is not None else ""))
                if parsedUrl.port is not None:
                    request.Set(GatewayRequest.GATEWAY_PORTNO, parsedUrl.port)
            except Exception as ex:
                response.Set(GatewayResponse.EXCEPTION, str(ex))
                response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_REQUEST_ERROR)
                response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_INVALID_URL)
                return 0  # Validation error: Invalid URL

        #
        #	If the request specifies a server name, use it. Otherwise, use the default.
        #
        server_name = request.Get(GatewayRequest.GATEWAY_SERVER)
        if server_name is not None:  # Override?
            server_list = [server_name]  # Use this name
        else:
            try:
                if self.rocketGateHost != GatewayService.LIVE_HOST:
                    server_list = [self.rocketGateHost]
                else:
                    server_list = socket.gethostbyname_ex(self.rocketGateHost)[2]
            except socket.gaierror:
                server_list = [GatewayService.LIVE_HOST_16, GatewayService.LIVE_HOST_17]

            server_list = [
                GatewayService.LIVE_HOST_16 if server == "69.20.127.91"
                else GatewayService.LIVE_HOST_17 if server == "72.32.126.131"
                else server
                for server in server_list
            ]

        #
        #	Clear any error tracking that may be leftover.
        #
        request.Clear(GatewayRequest.FAILED_SERVER)
        request.Clear(GatewayRequest.FAILED_RESPONSE_CODE)
        request.Clear(GatewayRequest.FAILED_REASON_CODE)
        request.Clear(GatewayRequest.FAILED_GUID)

        #
        #	Randomly pick an endpoint.
        #
        if len(server_list) > 1:  # Have multiples?
            index = random.randint(0, len(server_list) - 1)
            if index > 0:  # Want to change?
                swapper = server_list[0]  # Save the first one
                server_list[0] = server_list[index]
                server_list[index] = swapper  # And swap

        #
        #	Loop over the hosts and try to send the transaction to each host in the list until it succeeds or fails
        #	due to an unrecoverable error.
        #
        index = 0  # Start at first position
        while index < len(server_list):  # Loop over list
            results = self.SendTransaction(server_list[index], request, response)

            #
            #	If the transaction was successful, we are done
            #
            if results == GatewayCodes.RESPONSE_SUCCESS:  # Success?
                return 1  # (TRUE) All done

            #
            #	If the transaction is not recoverable, quit.
            #
            if results != GatewayCodes.RESPONSE_SYSTEM_ERROR:  # Unrecoverable?
                return 0  # (FALSE) Must quit

            #
            #	Save any errors in the response so they can be transmitted along with the next request.
            #
            request.Set(GatewayRequest.FAILED_SERVER, server_list[index])
            request.Set(GatewayRequest.FAILED_RESPONSE_CODE, response.Get(GatewayResponse.RESPONSE_CODE))
            request.Set(GatewayRequest.FAILED_REASON_CODE, response.Get(GatewayResponse.REASON_CODE))
            request.Set(GatewayRequest.FAILED_GUID, response.Get(GatewayResponse.TRANSACT_ID))
            index += 1  # Next index

        #
        #	If we ran out of places to send this, just quit.
        #
        return 0  # Must quit

    def PerformTargetedTransaction(self, request, response):
        """Sends a transaction to a server based upon the GUID."""

        #
        #	Clear any error tracking that may be leftover.
        #
        request.Clear(GatewayRequest.FAILED_SERVER)
        request.Clear(GatewayRequest.FAILED_RESPONSE_CODE)
        request.Clear(GatewayRequest.FAILED_REASON_CODE)
        request.Clear(GatewayRequest.FAILED_GUID)

        #
        #	This transaction must go to the host that processed a previous referenced transaction.  Get the GUID of the
        #	reference transaction.
        #
        referenceGUID = request.Get(GatewayRequest.REFERENCE_GUID)
        if referenceGUID is None:  # Don't have reference?
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_REQUEST_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_INVALID_REFGUID)
            return 0  # And quit

        #
        #	Strip off the bits that indicate which server should be used.
        #
        if len(referenceGUID) > 15:  # Live servers?
            siteString = referenceGUID[0:2]  # Get first two digits
        else:
            siteString = referenceGUID[0:1]  # Get first digit

        #
        #	Try to turn the site string into a number.
        #
        try:
            siteNo = int(siteString, 16)  # Get site number
        except:  # Parsing error?
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_REQUEST_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_INVALID_REFGUID)
            return 0  # And quit

        #
        #	Build the hostname to which the transaction should be directed.
        #
        server_name = request.Get("gatewayServer")
        if server_name is None:  # Don't have one?
            server_name = self.rocketGateHost  # Start with default
            separator = server_name.find(".")  # Find first .
            if separator > 0:  # Did we find it?
                server_name = "{0}-{1}{2}".format(
                    server_name[0:separator],
                    str(siteNo),
                    server_name[separator:]
                )  # Full server name
        #
        #	Send the transaction to the specified host.
        #
        results = self.SendTransaction(server_name, request, response)
        if results == GatewayCodes.RESPONSE_SUCCESS:  # Did server return 0?
            return 1  # This succeeded
        return 0  # This failed

    def PerformConfirmation(self, request, response):
        """Performs the confirmation pass that tells the server we have received the transaction reply."""

        #
        #	Verify that we have a transaction ID for the confirmation message.
        #
        confirmGUID = response.Get(GatewayResponse.TRANSACT_ID)
        if confirmGUID is None:  # Don't have reference?
            response.Set(GatewayResponse.EXCEPTION, "BUG-CHECK - Missing confirmation GUID")
            response.Set(GatewayResponse.RESPONSE_CODE, GatewayCodes.RESPONSE_SYSTEM_ERROR)
            response.Set(GatewayResponse.REASON_CODE, GatewayCodes.REASON_BUGCHECK)
            return 0  # And quit

        #
        #	Add the GUID to the request and send it back to the original server for confirmation.
        #
        confirmResponse = GatewayResponse()  # Need a new response object
        request.Set(GatewayRequest.TRANSACTION_TYPE, "CC_CONFIRM")
        request.Set(GatewayRequest.REFERENCE_GUID, confirmGUID)
        results = self.PerformTargetedTransaction(request, confirmResponse)
        if results:  # Success?
            return 1  # Yes - We are done

        #
        #	If the confirmation failed, copy the reason and response code
        #	into the original response object to override the success.
        #
        response.Set(GatewayResponse.RESPONSE_CODE, confirmResponse.Get(GatewayResponse.RESPONSE_CODE))
        response.Set(GatewayResponse.REASON_CODE, confirmResponse.Get(GatewayResponse.REASON_CODE))
        return 0  # And quit

    def PerformAuthOnly(self, request, response):
        """Performs an auth-only transaction."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "CC_AUTH")
        results = self.PerformTransaction(request, response)
        if results:  # Success?
            results = self.PerformConfirmation(request, response)
        return results  # Return results

    def PerformTicket(self, request, response):
        """Performs a Ticket operation for a previous auth-only transaction."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "CC_TICKET")
        return self.PerformTargetedTransaction(request, response)  # Return results

    def PerformPurchase(self, request, response):
        """Performs a complete purchase transaction."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "CC_PURCHASE")
        results = self.PerformTransaction(request, response)
        if results:  # Success?
            results = self.PerformConfirmation(request, response)
        return results  # Return results

    def PerformCredit(self, request, response):
        """Performs a Credit operation for a previous transaction."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "CC_CREDIT")

        #
        #	If this is a reference GUID, send the transaction to the appropriate server.  Otherwise use the normal
        #	transaction distribution.
        #
        referenceGUID = request.Get(GatewayRequest.REFERENCE_GUID)
        if referenceGUID is not None:  # Have reference?
            results = self.PerformTargetedTransaction(request, response)
        else:
            results = self.PerformTransaction(request, response)
        return results  # Return results

    def PerformVoid(self, request, response):
        """Performs a Void operation for a previous transaction."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "CC_VOID")
        return self.PerformTargetedTransaction(request, response)  # Return results

    def PerformCardScrub(self, request, response):
        """Performs scrubbing on a card/customer"""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "CARDSCRUB")
        return self.PerformTransaction(request, response)  # Return results

    def PerformRebillCancel(self, request, response):
        """Schedules cancellation of rebilling."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "REBILL_CANCEL")
        return self.PerformTransaction(request, response)  # Return results

    def PerformRebillUpdate(self, request, response):
        """Updates terms of a rebilling."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "REBILL_UPDATE")

        #
        #	If there is no prorated charge, just perform the update.
        #
        amount = request.Get(GatewayRequest.AMOUNT)
        if amount is None:  # No charge?
            return self.PerformTransaction(request, response)  # Return results

        #
        #	If the amount will not result in a chage, just perform the update.
        #
        try:  # Check the amount
            value = float(amount)  # Make sure this is valid
            if value <= 0.0:  # Not chargeable?
                return self.PerformTransaction(request, response)  # Return results
        except:  # Not a valid amount
            pass

        #
        #	If there is a charge, perform the update and confirm the charge.
        #
        results = self.PerformTransaction(request, response)
        if results:  # Success?
            results = self.PerformConfirmation(request, response)
        return results  # Return results

    def PerformCardUpload(self, request, response):
        """Uploads card data to the servers."""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "CARDUPLOAD")
        return self.PerformTransaction(request, response)  # Return results

    def PerformLookup(self, request, response):
        """Performs GUID lookup"""

        request.Set(GatewayRequest.TRANSACTION_TYPE, "LOOKUP")
        referenceGUID = request.Get(GatewayRequest.REFERENCE_GUID)
        if referenceGUID is not None:  # Have reference?
            results = self.PerformTargetedTransaction(request, response)
        else:
            results = self.PerformTransaction(request, response)
        return results

    def GenerateXsell(self, request, response):
        """Adds an entry to the XsellQueue."""

        # Apply the transaction type to the request
        request.Set(GatewayRequest.TRANSACTION_TYPE, "GENERATEXSELL")
        request.Set(GatewayRequest.REFERENCE_GUID, request.Get(GatewayRequest.XSELL_REFERENCE_XACT))

        if request.Get(GatewayRequest.REFERENCE_GUID) is not None:
            return self.PerformTargetedTransaction(request, response)
        else:
            return self.PerformTransaction(request, response)

    def BuildPaymentLink(self, request, response) -> bool:
        """Creates an embeddable RocketGate hosted payment link"""

        if request.Get(GatewayRequest.EMBEDDED_FIELDS_TOKEN) is not None:
            embedded_fields_token = request.Get(GatewayRequest.EMBEDDED_FIELDS_TOKEN)
            gateway_url = embedded_fields_token.replace("EmbeddedFieldsProxy", "BuildPaymentLinkSubmit")
            request.Set(GatewayRequest.GATEWAY_URL, gateway_url)
        else:
            request.Set(GatewayRequest.GATEWAY_SERVLET, "/hostedpage/servlet/BuildPaymentLinkSubmit")

        self.PerformTransaction(request, response)

        return (response.Get(GatewayResponse.RESPONSE_CODE) == GatewayCodes.RESPONSE_SUCCESS and
                response.Get(GatewayResponse.PAYMENT_LINK_URL) is not None)


class GatewayCodes:

    # Static response codes
    RESPONSE_SUCCESS = "0"
    '''Function succeeded'''
    RESPONSE_BANK_FAIL = "1"
    '''Bank decline/failure'''
    RESPONSE_RISK_FAIL = "2"
    '''Risk failure'''
    RESPONSE_SYSTEM_ERROR = "3"
    '''Server/recoverable error'''
    RESPONSE_REQUEST_ERROR = "4"
    '''Invalid request'''

    # Static reason codes
    REASON_SUCCESS = "0"
    '''Function succeeded'''

    REASON_NOMATCHING_XACT = "100"
    REASON_CANNOT_VOID = "101"
    REASON_CANNOT_CREDIT = "102"
    REASON_CANNOT_TICKET = "103"
    REASON_DECLINED = "104"
    REASON_DECLINED_OVERLIMIT = "105"
    REASON_DECLINED_CVV2 = "106"
    REASON_DECLINED_EXPIRED = "107"
    REASON_DECLINED_CALL = "108"
    REASON_DECLINED_PICKUP = "109"
    REASON_DECLINED_EXCESSIVE = "110"
    REASON_DECLINED_INVALID_CARDNO = "111"
    REASON_DECLINED_INVALID_EXPIRATION = "112"
    REASON_BANK_UNAVAILABLE = "113"
    REASON_DECLINED_AVS = "117"
    REASON_INVALID_REGION = "120"
    REASON_USER_DECLINED = "123"
    REASON_NETWORK_MISMATCH = "125"
    REASON_CELLPHONE_BLACKLISTED = "126"
    REASON_FULL_FAILURE = "127"
    REASON_DECLINED_PIN = "129"
    REASON_DECLINED_AVS_AUTOVOID = "150"
    REASON_DECLINED_CVV2_AUTOVOID = "151"
    REASON_INVALID_TICKET_AMT = "152"
    REASON_INTEGRATION_ERROR = "154"
    REASON_DECLINED_CAVV = "155"
    REASON_UNSUPPORTED_CARDTYPE = "156"
    REASON_DECLINED_RISK = "157"
    REASON_INVALID_DEBIT_ACCOUNT = "158"
    REASON_INVALID_USER_DATA = "159"
    REASON_AUTH_HAS_EXPIRED = "160"
    REASON_PREVIOUS_HARD_DECLINE = "161"
    REASON_MERCHACCT_LIMIT = "162"
    REASON_DECLINED_CAVV_AUTOVOID = "163"
    REASON_DECLINED_STOLEN = "164"
    REASON_BANK_INVALID_TRANSACTION = "165"
    REASON_REFER_TO_MAKER = "166"
    REASON_CVV2_REQUIRED = "167"
    REASON_INVALID_TAX_ID = "169"

    REASON_RISK_FAIL = "200"
    REASON_CUSTOMER_BLOCKED = "201"
    REASON_3DSECURE_AUTHENTICATION_REQUIRED = "202"
    REASON_3DSECURE_NOT_ENROLLED = "203"
    REASON_3DSECURE_INELIGIBLE = "204"
    REASON_3DSECURE_REJECTED = "205"
    REASON_RISK_CARD_CATEGORY = "206"
    REASON_RISK_AVS_VS_ISSUER = "207"
    REASON_RISK_DUPLICATE_MEMBERSHIP = "208"
    REASON_RISK_DUPLICATE_CARD = "209"
    REASON_RISK_DUPLICATE_EMAIL = "210"
    REASON_RISK_EXCEEDED_MAX_PURCHASE = "211"
    REASON_RISK_DUPLICATE_PURCHASE = "212"
    REASON_RISK_VELOCITY_CUSTOMER = "213"
    REASON_RISK_VELOCITY_CARD = "214"
    REASON_RISK_VELOCITY_EMAIL = "215"
    REASON_IOVATION_DECLINE = "216"
    REASON_RISK_VELOCITY_DEVICE = "217"
    REASON_RISK_DUPLICATE_DEVICE = "218"
    REASON_RISK_1CLICK_SOURCE = "219"
    REASON_RISK_TOOMANYCARDS = "220"
    REASON_AFFILIATE_BLOCKED = "221"
    REASON_TRIAL_ABUSE = "222"
    REASON_3DSECURE_BYPASS = "223"
    REASON_RISK_NEWCARD_NODEVICE = "224"
    REASON_3DSECURE_INITIATION = "225"
    REASON_3DSECURE_FRICTIONLESS = "226"
    REASON_3DSECURE_FRICTIONLESS_FAILED_AUTH = "227"
    REASON_3DSECURE_SCA_REQUIRED = "228"
    REASON_3DSECURE_CARDHOLDER_CANCEL = "229"
    REASON_3DSECURE_ACS_TIMEOUT = "230"
    REASON_3DSECURE_INVALID_CARD = "231"
    REASON_3DSECURE_INVALID_TRANSACTION = "232"
    REASON_3DSECURE_ACS_TECHNICAL_ISSUE = "233"
    REASON_3DSECURE_EXCEEDS_MAX_CHALLENGES = "234"

    REASON_DNS_FAILURE = "300"
    REASON_UNABLE_TO_CONNECT = "301"
    REASON_REQUEST_XMIT_ERROR = "302"
    REASON_RESPONSE_READ_TIMEOUT = "303"
    REASON_RESPONSE_READ_ERROR = "304"
    REASON_SERVICE_UNAVAILABLE = "305"
    REASON_CONNECTION_UNAVAILABLE = "306"
    REASON_BUGCHECK = "307"
    REASON_UNHANDLED_EXCEPTION = "308"
    REASON_SQL_EXCEPTION = "309"
    REASON_SQL_INSERT_ERROR = "310"
    REASON_BANK_CONNECT_ERROR = "311"
    REASON_BANK_XMIT_ERROR = "312"
    REASON_BANK_READ_ERROR = "313"
    REASON_BANK_DISCONNECT_ERROR = "314"
    REASON_BANK_TIMEOUT_ERROR = "315"
    REASON_BANK_PROTOCOL_ERROR = "316"
    REASON_ENCRYPTION_ERROR = "317"
    REASON_BANK_XMIT_RETRIES = "318"
    REASON_BANK_RESPONSE_RETRIES = "319"
    REASON_BANK_REDUNDANT_RESPONSES = "320"
    REASON_WEBSERVICE_FAILURE = "321"
    REASON_PROCESSOR_BACKEND_FAILURE = "322"
    REASON_JSON_FAILURE = "323"
    REASON_GPG_FAILURE = "324"
    REASON_3DS_SYSTEM_FAILURE = "325"
    REASON_USE_DIFFERENT_SERVER = "326"

    REASON_XML_ERROR = "400"
    REASON_INVALID_URL = "401"
    REASON_INVALID_TRANSACTION = "402"
    REASON_INVALID_CARDNO = "403"
    REASON_INVALID_EXPIRATION = "404"
    REASON_INVALID_AMOUNT = "405"
    REASON_INVALID_MERCHANT_ID = "406"
    REASON_INVALID_MERCHANT_ACCOUNT = "407"
    REASON_INCOMPATIBLE_CARDTYPE = "408"
    REASON_NO_SUITABLE_ACCOUNT = "409"
    REASON_INVALID_REFGUID = "410"
    REASON_INVALID_ACCESS_CODE = "411"
    REASON_INVALID_CUSTDATA_LENGTH = "412"
    REASON_INVALID_EXTDATA_LENGTH = "413"
    REASON_INVALID_CUSTOMER_ID = "414"
    REASON_TRANSACTION_NOT_FOUND = "415"
    REASON_MISSING_INVOICE_ID = "416"
    REASON_TRANSACTION_PENDING = "417"
    REASON_INVALID_CURRENCY = "418"
    REASON_INCOMPATABLE_CURRENCY = "419"
    REASON_INVALID_REBILL_ARGS = "420"
    REASON_INVALID_COUNTRY_CODE = "422"
    REASON_INCOMPATABLE_COUNTRY = "424"
    REASON_INVALID_ACCOUNT_NO = "426"
    REASON_INVALID_ROUTING_NO = "427"
    REASON_INVALID_LANGUAGE_CODE = "428"
    REASON_INVALID_BANK_NAME = "429"
    REASON_INVALID_BANK_CITY = "430"
    REASON_INVALID_CUSTOMER_NAME = "431"
    REASON_INVALID_BANKDATA_LENGTH = "432"
    REASON_INVALID_PIN_NO = "433"
    REASON_INVALID_PHONE_NO = "434"
    REASON_INVALID_ACCOUNT_HOLDER = "435"
    REASON_INCOMPATIBLE_DESCRIPTORS = "436"
    REASON_INVALID_REFERRAL_DATA = "437"
    REASON_INVALID_SITEID = "438"
    REASON_DUPLICATE_INVOICE_ID = "439"
    REASON_EXISTING_MEMBERSHIP = "440"
    REASON_INVOICE_NOT_FOUND = "441"
    REASON_INVALID_BATCH_DURATION = "442"
    REASON_MISSING_CUSTOMER_ID = "443"
    REASON_MISSING_CUSTOMER_NAME = "444"
    REASON_MISSING_CUSTOMER_ADDRESS = "445"
    REASON_MISSING_CVV2 = "446"
    REASON_MISSING_PARES = "447"
    REASON_NO_ACTIVE_MEMBERSHIP = "448"
    REASON_INVALID_CVV2 = "449"
    REASON_INVALID_3D_DATA = "450"
    REASON_INVALID_CLONE_DATA = "451"
    REASON_REDUNDANT_SUSPEND_OR_RESUME = "452"
    REASON_INVALID_PAYINFO_TRANSACT_ID = "453"
    REASON_INVALID_CAPTURE_DAYS = "454"
    REASON_INVALID_SUBMERCHANT_ID = "455"
    REASON_INVALID_COF_FRAMEWORK = "458"
    REASON_INVALID_REFERENCE_SCHEME_TRANSACTION = "459"
    REASON_INVALID_CUSTOMER_ADDRESS = "460"
    REASON_INVALID_CPF_FORMAT = "463"
    REASON_INVALID_GOOGLE_PAY_TOKEN = "464"
