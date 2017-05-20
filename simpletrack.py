from flask import Flask, request, g, render_template, jsonify
from datetime import date
import sqlite3

DATABASE = 'simpletrack.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db


@app.before_request
def before_request():
    if not hasattr(g, 'db'):
        g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# -----------------------


def get_issue(limit = None):
    stmt = "SELECT ROWID, * FROM issues ORDER BY ROWID DESC"
    if limit:
        stmt += " LIMIT {}".format(limit)
    return g.db.execute(stmt)


def insert_issue(description):
    stmt = 'INSERT INTO issues (`description`, `status`, `date`) VALUES (:description, :status, :date)'
    g.db.execute(stmt, {'description': description,
                        'status': 'open', 'date': date.today()})
    g.db.commit()


def update_issue(rowid, status):
    stmt = 'UPDATE issues SET `status` = :status WHERE ROWID = :rowid'
    g.db.execute(stmt, {'status': status, 'rowid': rowid})
    g.db.commit()


def delete_issue(rowid):
    stmt = 'DELETE FROM issues WHERE ROWID = :rowid'
    g.db.execute(stmt, {'rowid': rowid})
    g.db.commit()

# ----------------------

@app.route('/')
def index():
    cssmap = {'open': 'bg-warning', 'pending': 'bg-info',
              'resolved': 'bg-success', 'rejected': 'bg-danger'}
    return render_template('base.html', issues=get_issue(None), cssmap=cssmap)


@app.route('/add', methods=['POST'])
def add_issue():
    if request.form['description']:
        insert_issue(request.form['description'])
        return jsonify(issue=request.form['description'], message="Added Issue")
    else:
        return jsonify(message="Adding Issue Failed")


# false sense of security in only allowing POST
@app.route('/<status>/<int:rowid>', methods=['POST'])
def change_status(rowid, status):
    update_issue(rowid, status)
    return jsonify(message="Issue #{0} successfully marked as {1}.".format(rowid, status))


@app.route('/delete/<int:rowid>', methods=['POST'])
def remove_issue(rowid):
    delete_issue(rowid)
    return jsonify(message="Issue #{0} deleted.".format(rowid))

@app.route('/get/<int:limit>', methods=['GET'])
def get_issues(limit):
    # sqlite doesn't support slices?
    return jsonify((i[1],i[3]) for i in get_issue(limit))

if __name__ == '__main__':
    app.run()
