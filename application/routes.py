from application import app, db, api
from application.course_list import course_list
from application.forms import LoginForm, RegisterForm
from application.models import User, Course, Enrollment
from flask import jsonify, render_template, request, url_for, redirect, Response, flash, session
from application import functions
from flask_restx import Resource


##################################################################

@api.route('/api', '/api/')
class GetAndPost(Resource):
    # GET all
    def get(self):
        return jsonify(User.objects.all())

    # POST
    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'],
                    last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))


@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    # GET one
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    # PUT
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))

    # DELETE
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

##################################################################


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("index.html")


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Summer 2022"
    classes = Course.objects.all()
    # classes = Course.objects.order_by("+courseID") sort by courseID
    # courses_data = functions.take_courses()
    return render_template("courses.html", courses=classes, term=term)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('home'))
    return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/home")
        else:
            flash("Login wrong. Check your enter and try again.", "danger")
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route("/enrollment", methods=['GET', 'POST'])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Ooops! You are already registered in this course {courseTitle}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")

    classes = course_list(user_id)
    return render_template("enrollment.html", title="Enrollment", classes=classes)


# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     jdata = None
#     if idx is None:
#         jdata = functions.take_courses()
#     else:
#         courses_data = functions.take_courses()
#         jdata = courses_data[int(idx)]
#     return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    # User(user_id=1, first_name="Christian", last_name="Hur", email="christian@gmail.com", password="123456").save()
    # User(user_id=2, first_name="Mary", last_name="Jane", email="maryjane@gmail.com", password="111").save()
    users = User.objects.all()
    return render_template("user.html", users=users)
