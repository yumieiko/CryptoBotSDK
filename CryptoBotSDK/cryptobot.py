import json
from requests import get, post
from .types.Invoice import Invoice
from .types.Check import Check

class CryptoBot():
    def __init__(self, api_key: str, isTestnet = False):
        """
        CryptoBot is class for using the library
        Params:
        api_key = using for communicate with the cryptobot api
        isTestnet = (Optional) Using for testing the bot with testnet
        """

        self.headers = {'Content-Type': 'application/json', 'Crypto-Pay-API-Token': api_key}  
        if isTestnet:
            self.url = "https://testnet-pay.crypt.bot/api"
        else:
            self.url = "https://pay.crypt.bot/api"

    def createInvoice(self, 
                           amount: str,
                           asset: str, 
                           fiat = None,
                           accepted_assets = None,
                           descriptoion = None,
                           hidden_message = None,
                           paid_btn_name = None,
                           paid_btn_url = None,
                           payload = None,
                           expires_in = None,
                           allow_comments = True,
                           allow_anonymous = True,
                           currency_type = "crypto"):
        """
        createInvoice - function for creating a payment invoice
        
        Params:
            amount {string} - amount of the invoice, in fload
            asset {string}- Currency code, (BTC, TON, ETH)
            fiat {string} | Optional - Fiat code, (RUB, EUR, USD)
            accepted_assets {string} | Optional - List of cryptocurrency alphabetic codes separated comma. Assets which can be used to pay the invoice. Available only if currency_type is “fiat”. 
            descriptoion {string} | Optional - description of invoice
            hidden_message {string} | Optional - Text of the message which will be presented to a user after the invoice is paid. Up to 2048 characters.
            paid_btn_name {string} | Optional - Label of the button which will be presented to a user after the invoice is paid ( viewItem , openChannel , openBot , callback )
            paid_btn_url {string} | Optional - Required if paid_btn_name is specified. URL opened using the button which will be presented to a user after the invoice is paid. You can set any callback link 
            payload {string} | Optional - Any data you want to attach to the invoice (for example, user ID, payment ID, ect). Up to 4kb.
            expires_in {int} | Optional - You can set a payment time limit for the invoice in seconds. Values between 1-2678400 are accepted
            allow_comments {bool} | Optional - allow comments
            allow_anonymous {bool} | Optional - allow anonymous pay
            currency_type {string} | Optional - crypto or fiat):

        Responce
            Invoice - Invoice DataClass       
        """
        
        data_payload = {
            "currency_type": currency_type,
            "amount": amount,
            "asset": asset,
            "allow_anonymous": allow_anonymous,
            "allow_comments": allow_comments
        }

        if fiat is not None: data_payload.update({"fiat": fiat})
        if accepted_assets is not None: data_payload.update({"accepted_assets": accepted_assets})
        if descriptoion is not None: data_payload.update({"descriptoion": descriptoion})
        if hidden_message is not None: data_payload.update({"hidden_message": hidden_message})
        if paid_btn_name is not None: data_payload.update({"paid_btn_name": paid_btn_name})
        if paid_btn_url is not None: data_payload.update({"paid_btn_url": paid_btn_url})
        if payload is not None: data_payload.update({"payload": payload})
        if expires_in is not None: data_payload.update({"expires_in": expires_in})

        req = post(f"{self.url}/createInvoice", json=data_payload, headers=self.headers)
        jsonobj = json.loads(json.dumps(req.json()))["result"]

        # FIXME: Implement the items loop, because cryptobot can give a items list
        if "items" in jsonobj:
            pass

        comment_res = "not_provided_stuff"
        if "comment" in jsonobj: comment_res = jsonobj['comment']
        hidden_message_res = "not_provided_stuff"
        if "hidden_message" in jsonobj: hidden_message_res = jsonobj['comment']
        payload_res = "not_provided_stuff"
        if "payload" in jsonobj: payload_res = jsonobj['payload']
        

        return Invoice(
            invoice_id=jsonobj['invoice_id'],
            hash=jsonobj['hash'],
            currency_type=jsonobj['currency_type'],
            amount=jsonobj['amount'],
            bot_invoice_url=jsonobj['bot_invoice_url'],
            mini_app_invoice_url=jsonobj['mini_app_invoice_url'],
            web_app_invoice_url=jsonobj['web_app_invoice_url'],
            status=jsonobj['status'],
            created_at=jsonobj['created_at'],
            comment=comment_res,
            hidden_message=hidden_message_res,
            payload=payload_res
        )
    
    def getInvoices(self,
                    asset = None,
                    fiat = None,
                    invoice_ids = None,
                    status = None,
                    offset = None,
                    count = None):
        data_payload = {}
        if fiat is not None: data_payload.update({"fiat": fiat})
        if invoice_ids is not None: data_payload.update({"invoice_ids": invoice_ids})
        if status is not None: data_payload.update({"status": status})
        if asset is not None: data_payload.update({"asset": asset})
        if offset is not None: data_payload.update({"offset": offset})
        if count is not None: data_payload.update({"count": count})

        items = []

        req = get(f"{self.url}/getInvoices", headers=self.headers, json=data_payload)
        for i in req.json()["result"]["items"]:
            comment_res = "not_provided_stuff"
            if "comment" in i: comment_res = i['comment']
            hidden_message_res = "not_provided_stuff"
            if "hidden_message" in i: hidden_message_res = i['comment']
            payload_res = "not_provided_stuff"
            if "payload" in i: payload_res = i['payload']
            items.append(Invoice(
                invoice_id=i['invoice_id'],
                hash=i['hash'],
                currency_type=i['currency_type'],
                amount=i['amount'],
                bot_invoice_url=i['bot_invoice_url'],
                mini_app_invoice_url=i['mini_app_invoice_url'],
                web_app_invoice_url=i['web_app_invoice_url'],
                status=i['status'],
                created_at=i['created_at'],
                comment=comment_res,
                hidden_message=hidden_message_res,
                payload=payload_res
            ))
        return items
    
    
    def checkInvoice(self, invoice: Invoice):
        """
        checkInvoice - Check invoice Status
        Params:
            invoice {Invoice} - Invoice DataClass

        Responce: 
            have a three station
                active
                paid
                expierd
        """
        invoice_id = invoice.invoice_id()
        req = self.getInvoices(invoice_ids=invoice_id)
        if req[0]:
            return req[0].status()
        else:
            return "notfound"
        
    def deleteInvoice(self, invoice: Invoice):
        """
        deleteInvoice - delete a invoice created by your app
        Params:
            invoice {Invoice} - invoice dataclass

        Responce:
            fail - on error
            succes - on succes

        """
        data_payload = {"invoice_id": invoice.invoice_id()}
        res = post(f"{self.url}/deleteInvoice", json=data_payload, headers=self.headers)
        if res.status_code != 200:
            return "fail"
        return "succes"

    def createCheck(self,
                    amount: str,
                    asset = "USDT",
                    pin_to_user_id = None,
                    pin_to_username = None
                    ):
        
        """
        createCheck - Function for creating checks using app balance

        WARNING: for use this u need to enable checks in app settings!

        Params:

            amount {string} - amount of check
            asset {string} | Optional - asset, currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC”, default is USDT
            pin_to_user_id {int} | Optional - pin check only for user, pin by userid
            pin_to_username {string} | Optional - pin check only for user, pin by username

        Responce:

            Check - Check DataClass
        """

        data_payload = {
            "asset": asset,
            "amount": amount
        }
        if pin_to_user_id is not None: data_payload.update({"pin_to_user_id": pin_to_user_id})
        if pin_to_username is not None: data_payload.update({"pin_to_username": pin_to_username})

        req = post(f"{self.url}/createCheck", json=data_payload, headers=self.headers)

        if req.json()["ok"] == False:
            return f"Error code: {req.json()["error"]["code"]} | name: {req.json()["error"]["name"]}"
        
        activated_at_res = "check_not_activated"
        if req.json()["result"]["status"] == "activated": activated_at_res = req.json()["result"]["activated_at"]
        
        return Check(check_id=req.json()["result"]["check_id"],
                     hash=req.json()["result"]["hash"],
                     asset=req.json()["result"]["asset"],
                     amount=req.json()["result"]["amount"],
                     bot_check_url=req.json()["result"]["bot_check_url"],
                     status=req.json()["result"]["status"],
                     created_at=req.json()["result"]["created_at"],
                     activated_at=activated_at_res)
    
    def deleteCheck(self, check: Check):
        """
        deleteCheck - delete a check created by your app
        Params:
            check {Check} - check dataclass

        Responce:
            fail - on error
            succes - on succes

        """
        data_payload = {"check_id": check.check_id()}
        res = post(f"{self.url}/deleteCheck", json=data_payload, headers=self.headers)
        if res.status_code != 200:
            return "fail"
        return "succes"
    
    def getChecks(self, 
                  asset = None,
                  check_ids = None,
                  status = None,
                  offset = None,
                  count = None):
        data_payload = {}
        if asset is not None: data_payload.update({"asset": asset})
        if check_ids is not None: data_payload.update({"check_ids": check_ids})
        if status is not None: data_payload.update({"status": status})
        if offset is not None: data_payload.update({"offset": offset})
        if count is not None: data_payload.update({"count": count})

        items = []

        req = get(f"{self.url}/getChecks", headers=self.headers, json=data_payload)
        for i in req.json()["result"]["items"]:
            activated_res = "check_not_activated"
            if "activated_at" in i: activated_res = i['activated_at']
            items.append(Check(
                check_id=i["check_id"],
                hash=i['hash'],
                asset=i["asset"],
                amount=i["amount"],
                bot_check_url=i["bot_check_url"],
                status=i["status"],
                created_at=i["created_at"],
                activated_at=activated_res
            ))
        return items
    
    def checkCheck(self, check: Check):
        """
        checkCheck - View Check Status
        Params:
            check {Check} - Check DataClass

        Responce: 
            have a three station
                active
                activated
        """
        check_id = check.check_id()
        req = self.getChecks(check_ids=check_id)
        if req[0]:
            return req[0].status()
        else:
            return "notfound"
        

        
        
        



