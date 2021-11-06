from flask import Flask, render_template
from forms import SignUpForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)
if __name__ == '__main__':
    app.run()

