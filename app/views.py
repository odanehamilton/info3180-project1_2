from app import app
from flask import render_template, request, redirect, url_for,jsonify,session
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField, IntegerField, RadioField #,FileField
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
     #image = FileField('image', [validators.regexp('\w+\.jpg$')])


###
# Routing for your application.
### 

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
       # image = request.form['image']


        # write the information to the database
        newprofile = Myprofile(first_name=first_name,
                               last_name=last_name, username=username, age=age, sex=sex)#, image=image)
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


###
# The functions below should be applicable to all Flask apps.
###


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
