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


@app.route('/app', methods = ['GET', 'POST'])
@require_login()
def manager():
    """Handles the main app function."""

    # Get needed data from database
    projects = sql.Project.query.filter_by(user_id = g.user)
    return render_template(
        'manager.html',
        projects = projects,
        sql = sql
    )
