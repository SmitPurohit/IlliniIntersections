from flask import Flask, render_template, request , session, redirect, url_for
from forms import SignUpForm
from utils.functions_back import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'


# GARY HIGHWAY(ew) x NEAL SHORE(ns)

@app.route('/', methods=['POST', 'GET'])
def home():
    if 'isAuth' not in session:
        session['isAuth'] = 0
    if session['isAuth'] != 1:
        authString = "Log In/Sign Up"
        displayLogout = "display:none"
    else:
        authString = session['username']
        displayLogout = ""
    if request.method == 'POST':
        # Insert Reviews
        if "add_review_submit" in request.form:
            if session['isAuth'] == 1:
                intersection_id = request.form.get('intersection_review_id')
                lighting_review = request.form.get('lighting_review')
                quality_review = request.form.get('quality_review')
                traffic_review = request.form.get('traffic_review')
                va_review = request.form.get('va_review')
                comments = request.form.get('comments')
                insert_review(intersection_id, lighting_review, quality_review, traffic_review, va_review, comments)
                

        # Update Reviews
        if "update_submit" in request.form:
            return redirect(url_for('admin'))

        # Delete Reviews
        if "deleteReview_submit" in request.form:
            return redirect(url_for('admin'))
        
        # Delete User
        if "deleteUser_submit" in request.form:
            return redirect(url_for('admin'))

        # advanced queries
        if "runQuery1" in request.form:
            return redirect(url_for('queries'))
        if "runQuery2" in request.form:
            return redirect(url_for('queries'))



        # show intersection and info given streets
        street_ew = request.form['ew']
        street_ns = request.form['ns']
        street_ew_Coordinates = geocode(street_ew+",Champaign,Illinois")
        street_ns_Coordinates = geocode(street_ns +",Champaign,Illinois" )
        
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
                                display="display:''",
                                authStatus = authString,
                                logoutDisplay = displayLogout,
                                lat = street_ew_Coordinates[0],
                                lng = street_ew_Coordinates[1], 
                                lat1 = street_ew_Coordinates[0],
                                lng1 = street_ew_Coordinates[1]

                                )
        
    else:
        return render_template('index.html',
                                display="display:none", 
                                authStatus = authString, 
                                logoutDisplay = displayLogout)

@app.route('/admin', methods= ['POST','GET'])
def admin():
    #update users
    if "update_submit" in request.form:
        review_number = request.form.get('reviewNumber')
        new_comment = request.form.get('updateField')
        oldReview, newReview = update_review(review_number, new_comment)
        return render_template('admin.html', 
                                reviewUpdateNew = newReview, 
                                reviewUpdateOld = oldReview)
    # Delete Reviews
    if "deleteReview_submit" in request.form:
        delete_number = request.form.get("reviewNum")
        delete_review(delete_number)
        return render_template('admin.html')
    
    # Delete User
    if "deleteUser_submit" in request.form:
        delete_name = request.form.get("delUsername")
        
        delete_user(delete_name)
        return render_template('admin.html')
    return render_template('admin.html')

@app.route('/queries', methods= ['POST','GET'])
def queries():
    # advanced queries
    if "runQuery1" in request.form:
        return render_template('queries.html', resultQuery1 = runQuery1())
    if "runQuery2" in request.form:
        return render_template('queries.html', resultQuery2 = runQuery2())
    return render_template('queries.html')
@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/logout')
def logout():
    session.pop('isAuth', None)
    return redirect(url_for('home'))


@app.route('/signup', methods = ['POST','GET'])
def signup():
    print(1)
    if request.method == 'POST':
        if "submit_adduser" in request.form:
            username = request.form['username']
            password = request.form['password']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            validCheck = user_signup(username,firstName,lastName,password)
            if validCheck == 0:
                return redirect(url_for('login'))
    return render_template('adduser.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    session['isAuth'] = 0
    if request.method == 'POST':
       
        if "submit_sign" in request.form:
            
            username = request.form['username']
            password = request.form['password']
            isAuth = user_auth(username,password)
            if isAuth == 1:
                
                session['isAuth'] = 1
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            return render_template("signup.html")
        return render_template("adduser.html")
    return render_template("signup.html")

if __name__ == '__main__':
    app.run()

# @app.route('/<var>')
# def redirection():
#     return redirect(url_for('home'))

#    if 'username' in session:
#       username = session['username']
#       return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
#    return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"

