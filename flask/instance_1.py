from flask import Flask, url_for, request
app = Flask(__name__)
app.config['SECRECT_KEY'] = 'mrsoft'

@app.route('/')
def hello():
    return 'hello world!'

@app.route('/index')
def idx():
    return 'this is index'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'user:%s'%username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'post:%s'%post_id

@app.route('/url/')
def get_url():
#    return url_for('show_post', post_id = 2)
    return url_for('static', filename='css/style.css')

@app.route('/login', methods = ['POST', 'GET', 'PUT'])
def login():
    if request.method == 'GET':
        return 'this is get request'
    elif request.method == 'POST':
        pass
    else:
        pass

if __name__ == '__main__':
    app.run(debug=True)
