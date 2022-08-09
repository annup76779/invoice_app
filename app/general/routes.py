"user admin routes codebase"
from flask import jsonify, request
from datetime import datetime
from app import db
from sqlalchemy.exc import IntegrityError
from app.general import general_bp
from app.model import Invoice

@general_bp.route("/get")
def get_invoice():
    number = request.args.get("number")
    password = request.args.get("password")
    invoice_no = request.args.get("invoice_no")
    invoice_date = request.args.get("invoice_date")
    if invoice_no is not None:
        invoice = Invoice.query.filter_by(invoice_no = invoice_no, number=number, password=password).one_or_none()
        return jsonify(status = True, response = invoice.to_dict())

    elif invoice_date is not None:
        invoice_date = datetime.strptime(invoice_date, "%d-%m-%Y").date()
        invoices = Invoice.query.filter_by(invoice_date = invoice_date, number=number, password=password).all()
        print([invo.to_dict() for invo in invoices])
        return jsonify(status = True, response = [invo.to_dict() for invo in invoices])
    else:
        invoices = Invoice.query.filter_by(number=number, password=password).all()
        print(invoices)
        return jsonify(status = True, response = [invo.to_dict() for invo in invoices])


@general_bp.route("/update_invoice", methods=["PUT"])
def post_invoice():
    invoice_no = request.form.get('invoice_no')
    number = request.form.get('number')
    password = request.form.get('password')
    email = request.form.get('email')
    route_plan = request.form.get('route_plan')
    customer_name = request.form.get('customer_name')
    invoice_date = request.form.get('invoice_date')
    invoice_amount = request.form.get('invoice_amount')
    paid_amount = request.form.get('paid_amount')
    balance_amount = request.form.get('balance_amount')
    pending_since = request.form.get('pending_since')
    cash = request.form.get('cash')
    cheque_amount = request.form.get('cheque_amount')
    bank_name = request.form.get('bank_name')
    cheque_number = request.form.get('cheque_number')
    cheque_date = request.form.get('cheque_date')
    neft_amount = request.form.get('neft_amount')
    utrn_number = request.form.get('utrn_number')
    neft_date = request.form.get('neft_date')
    common_cheque = request.form.get('common_cheque')
    no_collection = request.form.get('no_collection')
    reason = request.form.get('reason')
    note_2000 = request.form.get('note_2000')
    note_500 = request.form.get('note_500')
    note_200 = request.form.get('note_200')
    note_100 = request.form.get('note_100')
    note_50 = request.form.get('note_50')
    note_20 = request.form.get('note_20')
    note_10 = request.form.get('note_10')
    coins = request.form.get('coins')
    total = request.form.get('total')
    transaction = request.form.get('transaction')
    status = request.form.get('status')

    invoice_date = datetime.strptime(invoice_date, '%d-%m-%Y')
    Invoice.update_invoice(number, password, email, route_plan, customer_name, invoice_date, invoice_no, invoice_amount, paid_amount, balance_amount, pending_since, cash, cheque_amount, bank_name, cheque_number, cheque_date, neft_amount, utrn_number, neft_date, common_cheque, no_collection, reason, note_2000, note_500, note_200, note_100, note_50, note_20, note_10, coins, total, transaction, status)
    db.session.commit()
    return jsonify(status = True)

#