import re
from flask import render_template
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app, db
from src.login import require_login
from src import sql


@require_login()
@app.route('/new_company', methods = ['GET', 'POST'])
def new_company():
    """Handle new company form."""

    company_name = request.values.get('company_name')
    if not company_name:
         return render_template('companyedit.html')

    if add_company(company_name):
        flash('Company added successfully!')
    return redirect(url_for('manager'))


def add_company(name: str):
    """Validate input and add valid company to db."""

    # Validate name
    name_regex = '^(?![ _.-])(?!.*[ _.-]{2})[\w _.-]{4,128}(?<![ _.-])$'
    if re.match(name_regex, name) is None:
        flash('Invalid company name!')
        return False
    # Check for same name company in db
    company = sql.Company.query.filter_by(name = name, user_id = g.user).one_or_none()
    if company is not None and company.name == name:
        flash(f'There already exists a company with that name.')
        return False
    # If all checks successful, create company
    db.session.add(sql.Company(name = name, user_id = g.user))
    db.session.commit()
    return True
