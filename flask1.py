from flask import Flask,redirect, url_for

app = Flask(__name__)

@app.route('/admin')
def admin():
    return "hello admin!!"
@app.route('/guest/<g>')
def guest(g):
    return "hello %s....." % g

@app.route('/')
def index():
    return "frist hello"

@app.route('/login')
def login():
    return "Login"

@app.route('/user/<name>')
def user(name):
    if name == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('guest', g=name))




if __name__ == '__main__':
    app.run(port=80,debug='false',host='192.168.0.103')