#coding=utf-8
from flask import Flask, redirect, url_for, render_template, request, jsonify


import pymysql
class sql:
    def __init__(self):
        self.db = pymysql.connect('192.168.0.81', 'root', '2009ZJ50', 'flask')
        self.cur = self.db.cursor()
    def sql_insert(self,sql_methed):
        self.methed = sql_methed
        self.cur.execute(sql_methed)
        self.db.commit()
    def sql_select(self,name,pwd):
        self.name = name
        self.pwd = pwd
        sql = "select * from user_info where user_name='%s' && user_pass='%s'" % (self.name, self.pwd)
        print(sql)
        status = self.cur.execute(sql)
        if status==1:
            return 1
        else:
            return 0



app = Flask(__name__)

@app.route('/admin')
def admin():
    return "hello admin!!"
@app.route('/guest/<g>')
def guest(g):
    return "hello %s....." % g

@app.route('/')
def index():
    ip = get_ip()
    return render_template('index.html', jay = ip)

@app.route('/login', methods=['POST'])
def login():
    ip = get_ip()
    user = request.form.get('name')
    passwd = request.form.get('pwd')
    sql_login = sql()
    a = sql_login.sql_select(user, passwd)
    if a == 1:
        return render_template('HomePge.html')
    elif len(passwd) == 0:
        msg = '密码不能为空'
        return render_template('index.html', jaa = msg, jay = ip)
    else:
        msg = '用户名或密码错误'
        return render_template('index.html', jaa = msg, jay = ip)

@app.route('/passport',methods=['POST'])
def register():
    return render_template('register.html')

@app.route('/zhuce',methods=['POST'])
def zhuce():
    user_name = str(request.form.get('user_name'))
    user_pwd = str(request.form.get('user_pwd'))
    user_email = str(request.form.get('user_email'))
    print(user_email)
    user_phone = str(request.form.get('user_phone'))
    s = "INSERT into user_info(user_name,user_pass,user_email,phone_num,create_time) VALUES ('%s','%s','%s','%s',NOW())" % (user_name, user_pwd, user_email, user_phone)
    print(s)
    insert_user = sql()
    insert_user.sql_insert(s)
    return '注册成功'

# @app.route('/user/<name>')
# def user(name):
#     if name == 'admin':
#         return redirect(url_for('admin'))
#     else:
#         return redirect(url_for('guest', g=name))


# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'


@app.route('/ip', methods=['GET'])
def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
