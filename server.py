from flask import Flask, render_template, request
from forms import SignUpForm
from utils.functions_back import get_intersection_info
from utils.functions_back import runQuery1
from utils.functions_back import runQuery2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'

# GARY HIGHWAY(ew) x NEAL SHORE(ns)
@app.route('/home', methods=['POST', 'GET'])
def home():
    print(request.form)
    print(type(request.form))
    if request.method == 'POST':
        if "runQuery1" in request.form:
            return render_template('index.html', resultQuery1 = runQuery1())
        if "runQuery2" in request.form:
            return render_template('index.html', resultQuery2 = runQuery2())
        street_ew = request.form['ew']
        street_ns = request.form['ns']
        intersectionID, comments, overallRating, visualAppeal, lightingRating, qualityRating, trafficRating, views = get_intersection_info(street_ew, street_ns)
        #print(intersectionID, comments, overallRating, visualAppeal)
        return render_template('index.html',
                                IntersectionNameEW=street_ew,
                                IntersectionNameNS=street_ns,
                                comments = comments,
                                overallRating = overallRating,
                                visualAppeal = visualAppeal,
                                lightingRating = lightingRating,
                                qualityRating = qualityRating,
                                trafficRating = trafficRating,
                                viewURL = views
                                )
        
    else:
        return render_template('index.html')


@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run()

