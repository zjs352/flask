#coding=utf-8
from flask import Flask, redirect, url_for, render_template, request, jsonify

import os
import pymysql
class sql:
    def __init__(self):
        self.db = pymysql.connect('192.168.0.81', 'root', '', 'flask')
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

def system_status():
    dic = {}
    mem = os.popen("free -mh|awk 'NR==2 {print $7}'").read().strip()
    disk = os.popen("df -h|awk 'NR==2 {print $5}'").read().strip()
    cpu = os.popen("top -bn1|grep '%Cpu(s)'|awk '{print $2}'").read().strip()
    dic['mem'] = mem
    dic['disk'] = disk
    dic['cpu'] = cpu
    return dic



app = Flask(__name__)

@app.route('/admin',methods=['GET'])
def admin():
    cpu_info = system_status()
    mem = cpu_info['mem']
    disk = cpu_info['disk']
    cpu = cpu_info['cpu']
    if len(mem) == 0:
        mem = '暂时获取不到'
    if len(disk) == 0:
        disk = '暂时获取不到'
    if len(cpu) == 0:
        cpu = '暂时获取不到'
    return render_template('system_status.html',jay_mem=mem, jay_disk=disk, jay_cpu=cpu)
@app.route('/guest/<g>')
def guest(g):
    return "hello %s....." % g

@app.route('/')
def index():
    ip = get_ip()
    return render_template('index.html', jay = ip)

@app.route('/login', methods=['POST','GET'])
def login():
    ip = get_ip()
    user = request.form.get('name')
    passwd = request.form.get('pwd')
    sql_login = sql()
    a = sql_login.sql_select(user, passwd)
    if a == 1 and user != 'admin':
        return render_template('HomePge.html')
    elif a == 1 and user == 'admin':
        return redirect('admin')
    elif len(passwd) == 0:
        msg = '**密码不能为空**'
        return render_template('index.html', jaa = msg, jay = ip)
    else:
        msg = '**用户名或密码错误**'
        return render_template('index.html', jaa = msg, jay = ip)

@app.route('/passport',methods=['POST'])
def register():
    return render_template('register.html')

@app.route('/zhuce',methods=['POST'])
def zhuce():
    user_name = str(request.form.get('user_name'))
    user_pwd = str(request.form.get('user_pwd'))
    user_email = str(request.form.get('user_email'))
    user_phone = str(request.form.get('user_phone'))
    if len(user_name.strip()) == 0 or len(user_pwd.strip()) == 0:
        msg = "用户名密码不能为空"
        return render_template('register.html', empt=msg)
    elif user_name == 'admin':
        msg = 'admin已存在'
        return render_template('register.html', empt=msg)
    else:
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
