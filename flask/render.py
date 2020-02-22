from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/user/<username>')
def show_user_profile(username):
    mydic = {'key1':111,
             'key2':222}

    return render_template('user.html', name=username, dic=mydic)

if __name__ == '__main__':
    app.run(debug=True)
