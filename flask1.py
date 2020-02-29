#coding=utf-8
from flask import Flask,redirect, url_for,render_template,request, jsonify
from werkzeug import secure_filename

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

@app.route('/login')
def login():
    return "Login"

@app.route('/user/<name>')
def user(name):
    if name == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('guest', g=name))


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


@app.route('/ip', methods=['GET'])
def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

if __name__ == '__main__':
    app.run(port=80,debug='false',host='0.0.0.0')
