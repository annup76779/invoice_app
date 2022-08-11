import sqlalchemy as sa
import pandas as pd
from datetime import datetime
from app.model.util import NotValidInvoiceFile
from app import db, current_app, crypt

class Admin(db.Model):
    '''admin class'''
    __tablename__ = "admin"

    admin_id = sa.Column(sa.Integer, primary_key=True)
    admin_key = sa.Column(sa.String(60), nullable=False)

    def verify(self, provided_key):
        return crypt.check_password_hash(self.admin_key, provided_key)

    def set_admin_key(self, provided_key):
        self.admin_key = crypt.generate_password_hash(provided_key)


class Invoice(db.Model):
    """invoice table"""
    __tablename__ = "invoice"

    invoice_no = sa.Column(sa.String(10), primary_key=True)
    number = sa.Column(sa.String(14), nullable = False)
    password = sa.Column(sa.String(60), nullable = False)
    email = sa.Column(sa.String(120))
    route_plan = sa.Column(sa.String(20))
    customer_name = sa.Column(sa.String(225))
    invoice_date = sa.Column(sa.Date)
    invoice_amount = sa.Column(sa.String(20))
    paid_amount = sa.Column(sa.String(20))
    balance_amount = sa.Column(sa.String(20))
    pending_since = sa.Column(sa.String(20))
    cash = sa.Column(sa.String(20))
    cheque_amount = sa.Column(sa.String(25))
    bank_name = sa.Column(sa.String(256))
    cheque_number = sa.Column(sa.String(35))
    cheque_date = sa.Column(sa.String(15))
    neft_amount = sa.Column(sa.String(30))
    utrn_number = sa.Column(sa.String(35))
    neft_date = sa.Column(sa.String(15))
    common_cheque = sa.Column(sa.String(10))
    no_collection = sa.Column(sa.String(10))
    reason = sa.Column(sa.UnicodeText)
    note_2000 = sa.Column(sa.String(8))
    note_500 = sa.Column(sa.String(8))
    note_200 = sa.Column(sa.String(8))
    note_100 = sa.Column(sa.String(8))
    note_50 = sa.Column(sa.String(8))
    note_20 = sa.Column(sa.String(8))
    note_10 = sa.Column(sa.String(8))
    coins = sa.Column(sa.String(8))
    total = sa.Column(sa.String(25))
    transaction = sa.Column(sa.String(10))
    status = sa.Column(sa.String(10))  

    def __init__(self, *args, file_io=None):
        if len(args) == 33:
            self.invoice_no =str( args[6])
            self.number =str(args[0])
            self.password =str( args[1])
            self.email =str( args[2])
            self.route_plan =str( args[3])
            self.customer_name =str( args[4])
            self.invoice_date = args[5].date()
            self.invoice_amount =str( args[7])
            self.paid_amount =str( args[8])
            self.balance_amount =str( args[9])
            self.pending_since = str(args[10])
            self.cash = str(args[11])
            self.cheque_amount = str(args[12])
            self.bank_name = str(args[13])
            self.cheque_number = str(args[14])
            self.cheque_date = str(args[15])
            self.neft_amount = str(args[16])
            self.utrn_number = str(args[17])
            self.neft_date = str(args[18])
            self.common_cheque = str(args[19])
            self.no_collection = str(args[20])
            self.reason = str(args[21])
            self.note_2000 = str(args[22])
            self.note_500 = str(args[23])
            self.note_200 = str(args[24])
            self.note_100 = str(args[25])
            self.note_50 = str(args[26])
            self.note_20 = str(args[27])
            self.note_10 = str(args[28])
            self.coins = str(args[29])
            self.total = str(args[30])
            self.transaction = str(args[31])
            self.status = str(args[32])
            db.session.add(self)
        else:
            try:
                self.df = pd.read_csv(file_io, header=0,names=[x for x in range(33)]) # making dataframe 
                if len(self.df.columns) != 33:
                    raise Exception
                try:
                    self.df[14] = self.df[14].fillna(0)
                    self.df[14] = self.df[14].astype(int)
                    self.df[17] = self.df[17].fillna(0)
                    self.df[17] = self.df[17].astype(int)
                    self.df[20] = self.df[20].fillna(False)
                    self.df[20] = self.df[20].astype(bool)
                    for i in range(22, 31):
                        self.df[i] = self.df[i].fillna(0)
                        self.df[i] = self.df[i].astype(int)
                    self.df[5] = pd.to_datetime(self.df[5])
                except Exception as error:
                    print(error)
                    raise NotValidInvoiceFile("Invalid Date provided") from error
                self.merge_to_table()
            except Exception as error:
                raise NotValidInvoiceFile() from error

    def merge_to_table(self):
        already_inserted_invoice_no = Invoice.query.with_entities(Invoice.invoice_no).order_by(Invoice.invoice_date).all() # getting all the invoice no. in the list yet
        already_inserted_invoice_no = {inv_no[0] for inv_no in already_inserted_invoice_no[:1000]} # checking in last 1000 should be enought
        repeated_invoice_in_sheet = dict()
        i=-1
        for invoice_no in self.df[6]:
            i+=1
            if invoice_no in already_inserted_invoice_no:
                invoice = Invoice.query.get(invoice_no)
                invoice.invoice_no = str(self.df.iloc[i, 6])
                invoice.number = str(self.df.iloc[i, 0])
                invoice.password = str(self.df.iloc[i, 1])
                invoice.email = str(self.df.iloc[i, 2])
                invoice.route_plan = str(self.df.iloc[i, 3])
                invoice.customer_name = str(self.df.iloc[i, 4])
                invoice.invoice_date = self.df.iloc[i,5].date()
                invoice.invoice_amount = str(self.df.iloc[i, 7])
                invoice.paid_amount = str(self.df.iloc[i, 8])
                invoice.balance_amount = str(self.df.iloc[i, 9])
                invoice.pending_since = str(self.df.iloc[i, 10])
                invoice.cash = str(self.df.iloc[i, 11])
                invoice.cheque_amount = str(self.df.iloc[i, 12])
                invoice.bank_name = str(self.df.iloc[i, 13])
                invoice.cheque_number = str(self.df.iloc[i, 14])
                invoice.cheque_date = str(self.df.iloc[i, 15])
                invoice.neft_amount = str(self.df.iloc[i, 16])
                invoice.utrn_number = str(self.df.iloc[i, 17])
                invoice.neft_date = str(self.df.iloc[i, 18])
                invoice.common_cheque = str(self.df.iloc[i, 19])
                invoice.no_collection = str(self.df.iloc[i, 20])
                invoice.reason = str(self.df.iloc[i, 21])
                invoice.note_2000 = str(self.df.iloc[i, 22])
                invoice.note_500 = str(self.df.iloc[i, 23])
                invoice.note_200 = str(self.df.iloc[i, 24])
                invoice.note_100 = str(self.df.iloc[i, 25])
                invoice.note_50 = str(self.df.iloc[i, 26])
                invoice.note_20 = str(self.df.iloc[i, 27])
                invoice.note_10 = str(self.df.iloc[i, 28])
                invoice.coins = str(self.df.iloc[i, 29])
                invoice.total = str(self.df.iloc[i, 30])
                invoice.transaction = str(self.df.iloc[i, 31])
                invoice.status = str(self.df.iloc[i, 32])
            else:
                if invoice_no not in repeated_invoice_in_sheet:
                    invoice = Invoice(*tuple(self.df.iloc[i]))
                    repeated_invoice_in_sheet[invoice_no] = invoice
                else:
                    rp_invoice = repeated_invoice_in_sheet[invoice_no]
                    rp_invoice.invoice_no = str(self.df.iloc[i, 6])
                    rp_invoice.number = str(self.df.iloc[i, 0])
                    rp_invoice.password = str(self.df.iloc[i, 1])
                    rp_invoice.email = str(self.df.iloc[i, 2])
                    rp_invoice.route_plan = str(self.df.iloc[i, 3])
                    rp_invoice.customer_name = str(self.df.iloc[i, 4])
                    rp_invoice.invoice_date = self.df.iloc[i,5].date()
                    rp_invoice.invoice_amount = str(self.df.iloc[i, 7])
                    rp_invoice.paid_amount = str(self.df.iloc[i, 8])
                    rp_invoice.balance_amount = str(self.df.iloc[i, 9])
                    rp_invoice.pending_since = str(self.df.iloc[i, 10])
                    rp_invoice.cash = str(self.df.iloc[i, 11])
                    rp_invoice.cheque_amount = str(self.df.iloc[i, 12])
                    rp_invoice.bank_name = str(self.df.iloc[i, 13])
                    rp_invoice.cheque_number = str(self.df.iloc[i, 14])
                    rp_invoice.cheque_date = str(self.df.iloc[i, 15])
                    rp_invoice.neft_amount = str(self.df.iloc[i, 16])
                    rp_invoice.utrn_number = str(self.df.iloc[i, 17])
                    rp_invoice.neft_date = str(self.df.iloc[i, 18])
                    rp_invoice.common_cheque = str(self.df.iloc[i, 19])
                    rp_invoice.no_collection = str(self.df.iloc[i, 20])
                    rp_invoice.reason = str(self.df.iloc[i, 21])
                    rp_invoice.note_2000 = str(self.df.iloc[i, 22])
                    rp_invoice.note_500 = str(self.df.iloc[i, 23])
                    rp_invoice.note_200 = str(self.df.iloc[i, 24])
                    rp_invoice.note_100 = str(self.df.iloc[i, 25])
                    rp_invoice.note_50 = str(self.df.iloc[i, 26])
                    rp_invoice.note_20 = str(self.df.iloc[i, 27])
                    rp_invoice.note_10 = str(self.df.iloc[i, 28])
                    rp_invoice.coins = str(self.df.iloc[i, 29])
                    rp_invoice.total = str(self.df.iloc[i, 30])
                    rp_invoice.transaction = str(self.df.iloc[i, 31])
                    rp_invoice.status = str(self.df.iloc[i, 32])

    @staticmethod
    def update_invoice(*args):
        if len(args) == 33:
            invoice = Invoice.query.get(args[6])
            invoice.invoice_no =str(args[6])
            invoice.number =str(args[0])
            invoice.password =str(args[1])
            invoice.email =str(args[2])
            invoice.route_plan =str(args[3])
            invoice.customer_name =str(args[4])
            invoice.invoice_date = args[5].date()
            invoice.invoice_amount =str(args[7])
            invoice.paid_amount =str(args[8])
            invoice.balance_amount =str(args[9])
            invoice.pending_since = str(args[10])
            invoice.cash = str(args[11])
            invoice.cheque_amount = str(args[12])
            invoice.bank_name = str(args[13])
            invoice.cheque_number = str(args[14])
            invoice.cheque_date = str(args[15])
            invoice.neft_amount = str(args[16])
            invoice.utrn_number = str(args[17])
            invoice.neft_date = str(args[18])
            invoice.common_cheque = str(args[19])
            invoice.no_collection = str(args[20])
            invoice.reason = str(args[21])
            invoice.note_2000 = str(args[22])
            invoice.note_500 = str(args[23])
            invoice.note_200 = str(args[24])
            invoice.note_100 = str(args[25])
            invoice.note_50 = str(args[26])
            invoice.note_20 = str(args[27])
            invoice.note_10 = str(args[28])
            invoice.coins = str(args[29])
            invoice.total = str(args[30])
            invoice.transaction = str(args[31])
            invoice.status = str(args[32])
            db.session.add(invoice)

    def to_dict(self):
        return {
            "balance_amount": self.balance_amount,
            "bank_name": self.bank_name,
            "cash": self.cash,
            "cheque_amount": self.cheque_amount,
            "cheque_date": self.cheque_date,
            "cheque_number": self.cheque_number,
            "coins": self.coins,
            "common_cheque": self.common_cheque,
            "customer_name": self.customer_name,
            "email": self.email,
            "invoice_amount": self.invoice_amount,
            "invoice_date": self.invoice_date.strftime("%d-%m-%Y"),
            "invoice_no": self.invoice_no,
            "neft_amount": self.neft_amount,
            "neft_date": self.neft_date,
            "no_collection": self.no_collection,
            "note_10": self.note_10,
            "note_100": self.note_100,
            "note_20": self.note_20,
            "note_200": self.note_200,
            "note_2000": self.note_2000,
            "note_50": self.note_50,
            "note_500": self.note_500,
            "number": self.number,
            "paid_amount": self.paid_amount,
            "password": self.password,
            "pending_since": self.pending_since,
            "reason": self.reason,
            "route_plan": self.route_plan,
            "status": self.status,
            "total": self.total,
            "transaction": self.transaction,
            "utrn_number": self.utrn_number
        }