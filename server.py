from flask import Flask, render_template, request
from forms import SignUpForm
from utils.functions_back import get_intersection_info


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        street_ew = request.form['nm']
        street_ns = request.form['ew']
        print(street_ew, street_ns)
    else:
        return render_template('index.html')


@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run()

