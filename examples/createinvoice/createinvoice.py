from CryptoBotSDK.cryptobot import CryptoBot
from os import getenv

def main():
    cb = CryptoBot(getenv("cbtestnet"), True)
    invoices = cb.createInvoice("100", "USDT")
    
    print(invoices.invoice_id())

main()