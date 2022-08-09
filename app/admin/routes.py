"user admin routes codebase"
from flask import jsonify, request
from app import db
from sqlalchemy.exc import IntegrityError
from app.admin import admin_bp
from app.model.util import NotValidInvoiceFile
from app.model import Invoice


@admin_bp.route("/upload_invoice", methods=["POST"])
def upload_invoice():
    try:
        invoice_csv_file = request.files["invoice_csv_file"]
        _ = Invoice(None,file_io = invoice_csv_file)
        db.session.commit()
        return jsonify(status = True, response = "Invoice updated successfully.")
    except NotValidInvoiceFile as error:
        return jsonify(status = False, response = error.message)
    except IntegrityError as error:
        return jsonify(status = False, response = "In your excel there is any `invoice number` which is already used in invoice before last 1000 invoices. Please check it and upload again.")
    except:
        return jsonify(status = False, response = "Something went wrong.")