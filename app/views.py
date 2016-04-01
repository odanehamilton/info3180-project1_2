from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField, PasswordField, FileField, IntegerField, RadioField
from wtforms import validators
from wtforms.validators import Required
from app.models import Myprofile
from app.forms import LoginForm

from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid

class ProfileForm(Form):
     id_num = TextField('ID')
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])
     username = TextField('Username', validators=[Required()])
     age = IntegerField('Age', validators=[Required()])
     sex = RadioField('Sex', choices=[('Male','Male'),('Female','Female')])
     image = FileField('image', [validators.regexp('\w+\.jpg$')])





@app.before_request
def before_request():
    g.user = current_user

    
    

###
# Routing for your application.
### 
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    usernames = Myprofile.query.all()
    if request.method == 'POST':
        for names in usernames:
            if request.form['username'] == names.username and request.form['password'] == names.password:
                session['logged_in'] = True
                return redirect(url_for('profile_view', id_num=names.id_num))
        else:
            error = "Invalid login data"
    return render_template('login.html', error=error)
    
    
@app.route('/logout')
def logout():
    """Render website's logout page."""
    session.pop('logged_in', None)
    return redirect(url_for('home'))

    

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/profile/', methods=['POST','GET'])
def profile_add():
    db.create_all()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        age = request.form['age']
        sex = request.form['sex']
        image = request.form['image']


        # write the information to the database
        newprofile = Myprofile(first_name=first_name,
                               last_name=last_name, username=username, age=age, sex=sex, image=image)
        db.session.add(newprofile)
        db.session.commit()

        return "{} {} was added to the database".format(request.form['first_name'],
                                             request.form['last_name']) + render_template('home.html')
        

    form = ProfileForm()
    return render_template('profile_add.html',
                           form=form)
                           
                           

@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    profiles = Myprofile.query.all()
    
    return render_template('profile_list.html',
                            profiles=profiles)

@app.route('/profile/<int:id_num>')
def profile_view(id_num):
    profile = Myprofile.query.get(id_num)
    return render_template('profile_view.html',profile=profile)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
