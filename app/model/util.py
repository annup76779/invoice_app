class NotValidInvoiceFile(BaseException):
    def __init__(self, message = None):
        BaseException.__init__(self)
        if message is None:
            self.message = "invoice provided is not valid."
        else:
            self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message