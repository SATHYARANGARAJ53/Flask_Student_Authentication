from flask import Flask,render_template,request,redirect,flash,url_for
from models import db,StudentModel
from flask_bcrypt import Bcrypt


app=Flask(__name__)

app.secret_key = 'student'
bcrypt = Bcrypt(app)
# Configure the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db' #ur db uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)  # initialise the database with flask app


#create the database tables before the first request
with app.app_context():
    #db.drop_all()
    db.create_all() 


#home page
@app.route('/')
def home():
    return render_template('home.html')

#get
@app.route('/main')
def main():
    
    students=StudentModel.query.all() # Fetch all student records from the database
    return render_template('index.html',students=students)


#post
@app.route('/create',methods=['GET','POST'])
def create():
    if request.method =='GET':
        return render_template('create.html')
    
    if request.method=='POST':
        first_name=request.form['first_name']  # This retrieves the value entered by the user in the input field with the name attribute set to first_name
        last_name=request.form['last_name']
        email=request.form['email']
        password=request.form['password']
        gender=request.form['gender']

        students=StudentModel(  # the data that we set to first_name from user is stored in model and insert into db
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender
        )
        db.session.add(students)
        db.session.commit()
        return redirect('/main')  


#delete
@app.route('/<int:id>/delete',methods=['POST'])
def delete(id):
    students=StudentModel.query.get(id)  

    if not students:
        abort(404)
    db.session.delete(students)
    db.session.commit()
    return redirect('/main')
    
#update
@app.route('/<int:id>/edit',methods=['GET','POST'])
def update(id):
    students=StudentModel.query.get(id)
    if not students:
        abort(404)
    if request.method =='POST':
        students.first_name=request.form['first_name']  # This retrieves the value entered by the user in the input field with the name attribute set to first_name
        students.last_name=request.form['last_name']
        students.email=request.form['email']
        students.password=request.form['password']
        students.gender=request.form['gender']
 
        db.session.commit()
        return redirect('/main')
    return render_template('update.html', students=students)


#login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':

        email=request.form['email']
        password=request.form['password']
        students=StudentModel.query.filter_by(email=email).first() #Query for student with matching email.

        #Authenticate user by checking if password matches
        if students and bcrypt.check_password_hash(students.password, password):
            
            return redirect('/main')
        else:
            flash('Invalid email or password','danger')
    return render_template('login.html')


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']

        # Check if the email already exists in the database
        existing_user = StudentModel.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please log in or use a different email.','danger')

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')

        new_student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            gender=gender
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect('/login')  # Redirect to login page after successful signup
    return render_template('signup.html')

#forgetpassword
@app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if request.method=='POST':
        email=request.form.get('email')
        new_password=request.form.get('new_password')
        confirm_password=request.form.get('confirm_password')

        student =StudentModel.query.filter_by(email=email).first()

        if not student:
            flash('Email is not registered','danger')
            return render_template('signup.html')
        
        if new_password!=confirm_password:
            flash('password do not match','danger')
            return redirect(url_for("forgot_password"))

        hashed_password=bcrypt.generate_password_hash(new_password).decode('utf-8')
        student.password=hashed_password
        db.session.flush()  # Ensures pending changes are flushed to the database
        db.session.commit()

        flash('Password changed succesfully','success')
        return redirect(url_for("login"))

    return render_template('forgotpassword.html')


if __name__=='__main__':
    app.run(debug=True) # run the app


#  GET request: When a user navigates to http://localhost:5000/create in their browser, the browser sends a GET request by default. Flask recognizes this and sets request.method to 'GET'.
# In this code, if request.method == 'GET' would be True, so Flask renders the form template create.html.

# POST request: When a user fills out the form and submits it, the form sends a POST request to the server.