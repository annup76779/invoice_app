"user admin routes codebase"
from flask import jsonify, request
from app import db, current_app
from sqlalchemy.exc import IntegrityError
from app.admin import admin_bp
from app.model.util import NotValidInvoiceFile
from app.model import Invoice, Admin
from flask_jwt_extended import create_access_token, jwt_required


@admin_bp.route("/login", methods=["POST"])
def login():
    password = request.form.get("password") 
    admin = Admin.query.get(1)
    if admin.verify(password):
        access_token = create_access_token(admin.admin_id)
        return jsonify(status = True, access_token = access_token, expires_in_days = current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES").days)
    return jsonify(status = False)


@admin_bp.route("/upload_invoice", methods=["POST"])
@jwt_required()
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
    except Exception as error:
        return jsonify(status = False, response = "Something went wrong.", msg=str(error))
