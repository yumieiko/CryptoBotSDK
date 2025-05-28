class Invoice:
    def __init__(self,
                 invoice_id: int,
                 hash: str,
                 currency_type: str,
                 amount: str,
                 bot_invoice_url: str,
                 mini_app_invoice_url: str,
                 web_app_invoice_url: str,
                 status: str,
                 created_at: str,
                 comment = None,
                 hidden_message = None,
                 payload = None
                 ):
        self.invoice_id = invoice_id
        self.hash = hash
        self.currency_type = currency_type
        self.amount = amount
        self.bot_invoice_url = bot_invoice_url
        self.mini_app_invoice_url = mini_app_invoice_url
        self.web_app_invoice_url = web_app_invoice_url
        self.status = status
        self.created_at = created_at
        self.comment = comment
        self.hidden_message = hidden_message
        self.payload = payload

    def get(self):
        def invoice_id(self):
            return self.invoice_id
        def hash(self):
            return self.hash
        def currency_type(self):
            return self.currency_type
        def amount(self):
            return self.amount
        def bot_invoice_url(self):
            return self.bot_invoice_url
        def mini_app_invoice_url(self):
            return self.mini_app_invoice_url
        def web_app_invoice_url(self):
            return self.web_app_invoice_url
        def status(self):
            return self.status
        def comment(self):
            return self.comment
        def hidden_message(self):
            return self.hidden_message
        def payload(self):
            return self.payload