import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

##
# CONFIG
##

BASEDIR = os.path.abspath(os.path.dirname(__name__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASEDIR, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


##
# Models
##

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(255),
        index=True,
        unique=True,
    )
    description = db.Column(db.Text())

##
# ROUTES
##


@app.route('/')
def index():
    # get the data
    all_projects = Project.query.all()
    return render_template(
        'index.html',
        all_projects=all_projects
    )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if not request.form:
        return render_template('update.html')
    else:
        # handle the form
        data = request.form
        name = data['name']
        description = data['description']
        # check if exists
        if Project.query.filter_by(name=name).count():
            print('already exists')
        else:
            # save values to the database
            new_proj = Project(name=name, description=description)
            db.session.add(new_proj)
            db.session.commit()
        # return to index
        return redirect(url_for('index'), code=303)


@app.route('/delete/<int:project_id>')
def delete(project_id):
    proj = Project.query.get(project_id)
    db.session.delete(proj)
    db.session.commit()
    # return to index
    return redirect(url_for('index'), code=303)


def initial_data():
    try:
        print(" * checking initial data")
        if Project.query.count() == 0:
            print('loading initial data')
            initial_project = Project(
                name='Day 1: HTML/CSS',
                description="""HTML and CSS were fun!
                but maybe not lining up images and words
                """
            )
            db.session.add(initial_project)
            db.session.commit()
    except Exception as e:
        if 'no such table' not in str(e):
            raise e


initial_data()

# start the server if running the file
if __name__ == '__main__':
    app.run(debug=True)
