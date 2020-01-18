from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_wtf import FlaskForm
from wtforms import Form, TextField, StringField, TextAreaField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
import sqlite3
from flask import g


app = Flask(__name__)
app.secret_key='secret123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/campaign')
def campaign():
    return render_template('campaign.html')

@app.route('/source')
def source():
    return render_template('source.html')

@app.route('/sourceResult', methods=['GET', 'POST'])
def sourceResult():
    result = request.form['product']
    result1 = request.form['region']
    result2 = request.form['image type']
    result3 = request.form['language']
    result4 = request.form['date']
    result5 = request.form['industry']
    result6 = request.form['brand']
    result7 = request.form['description']
    return render_template('sourceResult.html', genPro=result, genReg=result1, genImg=result2, genLan=result3, genDat=result4, 
                    genInd=result5, genBra=result6, genDes=result7)

@app.route('/resultCampaign')
def resultCampaign():
    return render_template('resultCampaign2.html')

@app.route('/resultCampaign2', methods=['POST','GET'])
def resultCampaign2():
    result = request.form.get('date', default = False)
    result1 = request.form.get('division', default = False)
    result2 = request.form.get('campaigntype', default = False)
    result3 = request.form.get('industry', default = False)
    result4 = request.form.get('region', default = False)
    result5 = request.form.get('product', default = False)
    result6 = request.form.get('user', default = False)
    result7 = request.form.get('description', default = False)
    con1 = result+'_'+result1+'_'+result2+'_'+result3+'_'+result4+'_'+result5+'_'+result6+'_'+result7
    totalResult = [result,result1,result2,result3,result4,result5,result6,result7,con1]
    c = get_db().cursor()
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO geNames VALUES (?,?,?,?,?,?,?,?,?)',totalResult)
    conn.commit()
    return  redirect(url_for('campaign'))



class RegisterForm(Form):
    id = StringField('Id', [validators.length(min=2)])
    name = StringField('Name', [validators.length(min=1, max=50)])
    surname = StringField('Surname', [validators.length(min=1, max=100)])
    username = StringField('Username', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Ups... Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


conn = sqlite3.connect('database.db',check_same_thread=False)
c = conn.cursor()
conn.row_factory = sqlite3.Row

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        id = form.id.data
        name = form.name.data
        surname = form.surname.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        c = get_db().cursor()
        conn = get_db()
        c = conn.cursor()
        c.execute('INSERT INTO Admin(ID_User,Name,Surname,Username,Email,Password) VALUES(?,?,?,?,?,?)', (id,name,surname,username,email,password))
        conn.commit()
        conn.close()

        flash('You are now registered and can log in', 'success')


        return redirect(url_for('registrationSuccess'))
    return redirect(url_for('registrationSuccess'))

@app.route('/registrationSuccess')
def registrationSuccess():
    flash('You are registered as admin')
    return render_template('registrationSuccess.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #Create cursor
        c = get_db().cursor()
        conn = get_db()
        c = conn.cursor()

        #Get Admin by username
        result = c.execute('SELECT * FROM Admin WHERE Username = %s', [username])

        if result > 0:
            #Get stored hash
            data = c.fetchone()
            password = data['Password']

            #Comprare passwords

            if sha256_crypt.verify(password_candidate, password):
                flash('Password matched')
            else:
                flash('Password not matched')

        else:
            flash('No user')


    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

    
