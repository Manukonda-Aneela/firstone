from  flask import Flask,render_template,request,url_for,redirect,flash,abort,session
import  mysql.connector
from flask_session import Session
from flask_bcrypt import Bcrypt
from dmail import sendmail
from Stoken import token
from itsdangerous import URLSafeTimedSerializer
from keys import secret_key,salt1,salt2 
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key= secret_key
app.config['SESSION_TYPE']='filesystem'
sk_test_51Oy5SBSIRJzZRUrGIfELymNnGK8DI1kYoC3EyHIwcctCFnHP15qcW1XgBORUDmbT83k73BuIwUh0GIuvIMqjYm0o00z2FlphRI

mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='users')
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/register',methods=['GET','POST']) 
# vqvj uzhh wbvt idhk
def register():
    if request.method=='POST':
        print(request.form)
        Name=request.form['name']
        Mail=request.form['email']
        Pwd=request.form['password']
        pwd=bcrypt.generate_password_hash(Pwd)
        Phone=request.form['phone']
        place=request.form['place']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select mail  from users where mail=%s',[Mail])
        count = cursor.fetchone()
        print(count)
        cursor.close()
        if count ==1:
            flash('Email Already In Use')
            return render_template ('register.html')
    
        userdata={'name':Name,'mail':Mail,'pwd':Pwd,'ph':Phone,'place':place}
        subject='Email Authentication'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(userdata,salt=salt1),_external=True)}"
        sendmail(to=Mail,subject=subject,body=body)
        flash('confirmation link sent to mail')
        return  render_template('register.html')
    return render_template('register.html')
@app.route('/confirm/<token>') 
def confirm(token):
    try:
        anee=URLSafeTimedSerializer('aneela@ is tester in the mnc company')
        userdata=anee.loads(token,salt=salt1,max_age=200)
    except Exception as e:
        return 'this link is expiredd sorry for  register next time' 
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into users( Name,Mail,pwd, phno,place) values(%s,%s,%s,%s,%s)',[userdata['name'],userdata['mail'],userdata['pwd'],userdata['ph'],userdata['place']])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST']) 
def  login():
    if session .get('user'):
        return redirect(url_for('Dashboard'))
    if request.method =='POST':
        Mail=request.form['name']  
        Pwd=request.form['pwd']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select Mail,pwd from users where Mail =%s',[Mail])
        mail,password =cursor.fetchone()
        cursor.execute('select Name from users where Mail=%s',[Mail])
        username=cursor.fetchone()[0]
        cursor.close()
        # print('..........',username)
        if Mail == mail and Pwd==password:
            session['user']=username
            return redirect(url_for('Dashboard'))
        else:
            flash('Invalid username & passwod')
            return  redirect(url_for('login'))    
    return render_template('login.html') 
@app.route('/reset',methods=['GET','POST']) 
def reset():
    if request.method=="POST":
        Mail=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where mail=%s',[Mail])
        count = cursor.fetchone()[0]
        cursor.close()
        if count == 1:
            subject='Reset password link'        
            body=f"your reset password link\n\nfollow this link takes for next step-{url_for('forgot',token=token(Mail,salt=salt2),_external=True)}"
            sendmail(to=Mail,subject=subject,body=body)
            flash('reset message send to mail')
            return redirect(url_for('reset'))
    return render_template('reset.html') 
@app.route('/forgot/<token>',methods=['GET','POST'])
def forgot(token):
    try :
        anee = URLSafeTimedSerializer(secret_key)
        user = anee.loads(token,salt=salt2,max_age=200)
    except Exception as e:
        abort(404, 'This link expiredddd.....!')
    else:
        if request.method == 'POST':
            newpwd = request.form['npwd']
            confirmpwd = request.form['cpwd']
            if newpwd == confirmpwd:
                cursor = mydb.cursor(buffered=True)
                cursor.execute('update users set pwd=%s where Email=%s',[newpwd,user])
                mydb.commit()
                cursor.close()
                flash('password updated successfully .....! ')
                return redirect(url_for('login'))
            else:
                flash('sorry password not correct......')
                return render_template('forgot.html')
    return render_template('forgot.html')
@app.route('/logout') 
def logout():
    if session.get('user'):
        session.pop('user')
        flash('session loggout  out .....')
        return  redirect(url_for('login')) 
    else:
        return  redirect(url_for('login')) 
    # return  redirect(url_for('login'))  
@app.route('/Dashboard') 
def Dashboard():
    if session.get('user'):
        return render_template('Dashboard.html') 
    else:
        return redirect(ur_for('login')) 
@app.route('/addnotes',methods=['GET','POST']) 
def addnotes():
    if request.method=='POST':
        print(request.form)
        a=request.form['title']
        c=request.form['content']
        w=request.form['added']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into notes( Title,content,added_by) values(%s,%s,%s)', [a,c,w])
        mydb.commit()
        cursor.close()
        flash('ur notes created......')
        return redirect(url_for('Dashboard'))
    return render_template('addnotes.html') 
@app.route('/viewnotes')
def viewnotes():
    cursor=mydb.cursor()
    cursor.execute('select * from notes')
    aneela= cursor.fetchall()
    print(aneela)
    return render_template('views.html',aneela=aneela)    



app.run(use_reloader=True,debug=True)
    



    
      