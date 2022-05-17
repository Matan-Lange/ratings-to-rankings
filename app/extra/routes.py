import base64
import os
import subprocess
import sys
from datetime import datetime
import pdfkit
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, session, make_response
from flask_login import logout_user, login_required, current_user
from app import db
from app.models import Rates, Group, Question

extra = Blueprint('extra', __name__)


@extra.route('/exit&save')
def exit_and_save():
    session.clear()
    logout_user()
    flash("You have been logged out information saved!", category="info")
    return redirect(url_for('extra.home_page'))


# allow convert logo to pdf
def image_file_path_to_base64_string(filepath: str) -> str:
    '''
    Takes a filepath and converts the image saved there to its base64 encoding,
    then decodes that into a string.
    '''
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()


@extra.route('/download')
@login_required
def download_pdf():
    os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable)
    WKHTMLTOPDF_CMD = subprocess.Popen(
        ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')],
        stdout=subprocess.PIPE).communicate()[0].strip()

    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    wk_options = {
        'page-size': 'A4',
        'dpi': 400,
        'encoding': 'UTF-8'
    }

    groups = [str(item.number) for item in Group.query.all()]
    # pdf_data = db.session.query(Rates).filter(Rates.group.in_(groups)).filter_by(username=current_user.username).all()
    questions = [item.description for item in
                 Question.query.filter_by(professor_name=current_user.professor_name).all()]

    full_name = current_user.name
    project_names = db.session.query(Rates, Group).outerjoin(Group, Rates.group == Group.number
                                                             ).filter(Rates.group.in_(groups),
                                                                      Rates.username == current_user.username).all()

    img_string = image_file_path_to_base64_string('app/logo.jpg')

    renderd = render_template('pdf_template.html', pdf_data=project_names, date=datetime.today().date(),
                              questions=questions, full_name=full_name, img_string=img_string)

    # return renderd

    pdf = pdfkit.from_string(renderd, False, configuration=pdfkit_config, options=wk_options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

    return response


@extra.route('/')
@extra.route('/home')
def home_page():
    return render_template('home.html')
