from flask import Flask, render_template, request
from forms import SignUpForm
from utils.functions_back import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'

# GARY HIGHWAY(ew) x NEAL SHORE(ns)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # Insert Reviews
        if "add_review_submit" in request.form:
            intersection_id = request.form.get('intersection_review_id')
            lighting_review = request.form.get('lighting_review')
            quality_review = request.form.get('quality_review')
            traffic_review = request.form.get('traffic_review')
            va_review = request.form.get('va_review')
            comments = request.form.get('comments')
            insert_review(intersection_id, lighting_review, quality_review, traffic_review, va_review, comments)
            return render_template('index.html')

        # Update Reviews
        if "update_submit" in request.form:
            review_number = request.form.get('reviewNumber')
            new_comment = request.form.get('updateField')
            oldReview, newReview = update_review(review_number, new_comment)
            return render_template('index.html', 
                                    reviewUpdateNew = newReview, 
                                    reviewUpdateOld = oldReview)

        # Delete Reviews
        if "delete_submit" in request.form:
            delete_number = request.form.get("reviewNum")
            delete_review(delete_number)
            return render_template('index.html')

        # advanced queries
        if "runQuery1" in request.form:
            return render_template('index.html', resultQuery1 = runQuery1())
        if "runQuery2" in request.form:
            return render_template('index.html', resultQuery2 = runQuery2())



        # show intersection and info given streets
        street_ew = request.form['ew']
        street_ns = request.form['ns']
        
        intersectionID, comments, overallRating, visualAppeal, lightingRating, qualityRating, trafficRating, views = get_intersection_info(street_ew, street_ns)
        return render_template('index.html',
                                IntersectionNameEW=street_ew + ' &',
                                IntersectionNameNS=street_ns,
                                comments = comments,
                                overallRating = overallRating,
                                visualAppeal = visualAppeal,
                                lightingRating = lightingRating,
                                qualityRating = qualityRating,
                                trafficRating = trafficRating,
                                viewURL = views,
                                display="display:''"
                                )
        
    else:
        return render_template('index.html',display="display:none")


@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run()

