from flask import Flask, render_template, request, redirect, url_for, flash,send_file
from flask_login import LoginManager, login_user, login_required, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from models import db, User, File
import os
from werkzeug.utils import secure_filename
from utils.encrypt_data import encrypt_file
from utils.decrypt_data import decrypt_file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key
app.config['UPLOAD_FOLDER'] = 'uploads'
db.init_app(app)
with app.app_context():
    db.create_all() 
login_manager = LoginManager(app)
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


def get_file_paths(sender_username, receiver_username):
    sender = User.query.filter_by(username=sender_username).first()
    receiver = User.query.filter_by(username=receiver_username).first()

    print(f"Sender: {sender}")
    print(f"Receiver: {receiver}")

    if sender and receiver:
        file = File.query.filter_by(sender_id=sender.id, receiver_id=receiver.id).first()
        print(f"File: {file}")

        if file:
            print(f"File URL: {file.file_url}")
            print(f"Keys URL: {file.keys_url}")
            return file.file_url, file.keys_url

    flash('No file found for the given sender and receiver usernames.')
    return None, None
@app.route('/home')
def home():
    # Implement your home route logic here
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        receiver_username = request.form.get('receiver_username') 
         # Get the receiver username from the form
       
        receiver = User.query.filter_by(username=receiver_username).first()  
        if file and receiver:
            filename = secure_filename(file.filename)
            original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(original_file_path)
            print("file saved")
            
            # Encrypt the file
            encrypted_file_path, keys_file_path = encrypt_file(original_file_path)
            print(encrypted_file_path,"dxfd")
            # Delete the original file
            os.remove(original_file_path)
            
            try:
                
                new_file = File(file_url=encrypted_file_path, sender_id=current_user.id, 
                                receiver_id=receiver.id, keys_url=keys_file_path)
                db.session.add(new_file)
                db.session.commit()
                print('File uploaded and encrypted successfully!')
            except Exception as e:
                print('Error:', e)
            return redirect(url_for('view'))
    return render_template('upload.html')


@app.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    if request.method == 'POST':
        sender_username = request.form.get('sender_username')
        receiver_username = request.form.get('receiver_username')
        
        print(f"Sender: {sender_username}, Receiver: {receiver_username}")
        
        # Retrieve the file and key file paths from the database
        file_url, keys_url = get_file_paths(sender_username, receiver_username)
        
        print(f"File URL: {file_url}, Keys URL: {keys_url}")
        
        if file_url and keys_url:
            # Decrypt the file
            decrypted_file_path = decrypt_file(file_url, keys_url)
            
            print(f"Decrypted File Path: {decrypted_file_path}")
            
            # Send the decrypted file to the client
            return send_file(decrypted_file_path, as_attachment=True)

    return render_template('view.html')




if __name__ == '__main__':
    
    app.run(debug=True)