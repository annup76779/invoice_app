"user admin routes codebase"
from flask import jsonify, request, send_file, abort
from app import db, current_app
from sqlalchemy.exc import IntegrityError
from app.admin import admin_bp
from app.model.util import NotValidInvoiceFile
from app.model import Invoice, Admin
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime
import os


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
    except:
        return jsonify(status = False, response = "Something went wrong.")

@admin_bp.route("/download")
@jwt_required()
def download():
    date = request.args.get("date")
    month = request.args.get("month")
    year = request.args.get("year")

    if date.isnumeric() and month.isnumeric() and year.isnumeric():
        status, file_= Invoice.to_csv(date, month, year)
        print(status, file_)
        if status and file_:
            file_reader = open(os.path.join(current_app.static_folder, "today_csv.csv"), "rb")
            return send_file(file_reader, as_attachment = True, download_name = f"{date}-{month}-{year}_csv.csv")
    return abort(404)

@admin_bp.route("/delete")
@jwt_required()
def delete():
    date = request.args.get("date")
    month = request.args.get("month")
    year = request.args.get("year")

    if date.isnumeric() and month.isnumeric() and year.isnumeric():
        try:
            db.session.query(Invoice).filter(Invoice.updated_on==datetime(int(year), int(month), int(date))).delete(synchronize_session=False)
            db.session.commit()
            return jsonify(status = True, msg="Deleted")
        except Exception as error:
            return jsonify(status = False, msg="Couldn't delete", error=  str(error))

    return jsonify(status = False, msg="Error deleting Invoice")