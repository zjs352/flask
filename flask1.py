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
def index(name=None):
    return render_template('index.html', name=name)

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
        return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200
    else:
        return jsonify({'ip': request.environ['HTTP_X_FORWARDED_FOR']}), 200

if __name__ == '__main__':
    app.run(port=80,debug='false',host='0.0.0.0')