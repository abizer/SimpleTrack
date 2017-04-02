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
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# -----------------------


def get_issues():
    issues = g.db.execute('SELECT ROWID, * FROM issues ORDER BY ROWID DESC')
    return issues


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
    cssmap = {'open': 'bg-danger', 'pending': 'bg-warning',
              'resolved': 'bg-success'}  # don't like this
    return render_template('base.html', issues=get_issues(), cssmap=cssmap)


@app.route('/add', methods=['POST'])
def add_issue():
    if request.form['description']:
        insert_issue(request.form['description'])
        return jsonify(issue=request.form['description'], message="Added Issue")
    else:
        return jsonify(issue=request.form['description'], message="Adding Issue Failed")


# false sense of security in only allowing POST
@app.route('/<status>/<int:rowid>', methods=['POST'])
def change_status(rowid, status):
    update_issue(rowid, status)
    return jsonify(message="Issue #{0} successfully marked as {1}.".format(rowid, status))


@app.route('/delete/<int:rowid>', methods=['POST'])
def remove_issue(rowid):
    delete_issue(rowid)
    return jsonify(message="Issue #{0} deleted.".format(rowid))

if __name__ == '__main__':
    app.run()
