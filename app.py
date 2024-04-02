from  flask import Flask,render_template,request,url_for,redirect
import  mysql.connector
# from flask_session import Session
# from flask_bcrypt import Bcrypt
app = Flask(__name__)
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
        Phone=request.form['phone']
        place=request.form['place']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into users( Name,Mail,pwd, phno,place) values(%s,%s,%s,%s,%s)',[Name,Mail,Pwd,Phone,place])
        cursor.execute('select * from users')
        sql= cursor.fetchall()
        print('sql sortred data all..............',sql)
        mydb.commit()
        data={'name':Name,'mail':Mail,'pwd':Pwd,'ph':Phone,'place':place}
        if data['mail']and data['pwd']:
            print(data['mail'],data['pwd']) 
            return redirect(url_for('login'))
        else:
            return  render_template('register')
    return render_template('register.html')
@app.route('/login',methods=['GET','POST']) 
def  login():
    if request.method =='POST':
        user=request.form['name']  
        pwd=request.form['pwd']
        if user == 'user':
            return [user,pwd]
        else:
            return  redirect(url_for('register'))    
    return render_template('login.html')   

    
app.run(use_reloader=True,debug=True)      