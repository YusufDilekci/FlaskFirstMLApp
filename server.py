from flask import Flask, jsonify, render_template, url_for, request, redirect, flash
from business.validation.LoginValidation import LoginForm
from business.validation.ContactValidation import ContactForm
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os
import datetime
import requests
import smtplib

from database.engine import Contact, session
from trained_model import predict_model


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = "some secret string"

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route("/")
def home():
    current_date = datetime.datetime.now().year
    return render_template("index.html", date = current_date)

@app.route("/guess/<name>")
def guess(name):
    agify_api_url =  f'https://api.agify.io?name={name}'
    agify_response = requests.get(agify_api_url).json()

    genderize_api_url = f'https://api.genderize.io?name={name}'
    genderize_response = requests.get(genderize_api_url).json()

    return render_template("guess.html", name=name, age=agify_response['age'], gender=genderize_response['gender'])


@app.route("/blog")
def get_all_posts():
    api_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    response = requests.get(api_url).json()
        
    return render_template("blog.html", post_list = response)

@app.route("/post/<int:id>")    
def get_post_by_id(id):
    api_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    response = requests.get(api_url).json()
    post = [blog for blog in response if blog['id'] == id]

    return render_template("post.html", post = post)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        return add_contact(request)
    
    return render_template("contact.html", form=form)
    
@app.route("/add_contact", methods=['POST'])
def add_contact(request):
    fname = request.form['fname']
    lname= request.form['lname']
    email = request.form['email']
    text = request.form['comment']

    new_contact = Contact(fname=fname, lname=lname, email=email, comment=text)
    session.add(new_contact)
    session.commit()
    print("Saved to database")

    # send_email(email)
    return redirect(url_for('home'))


def send_email(fromMail):
    toMail = 'ydilekci1@gmail.com'

    fromaddr = fromMail
    toaddrs  = f"To: {toMail}".split()

    msg = ("From: %s\r\nTo: %s\r\n\r\n"
        % (fromaddr, ", ".join(toaddrs)))
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        msg = msg + line

    print("Message length is", len(msg))

    server = smtplib.SMTP('localhost')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()    
    if(request.method == 'POST' and form.validate()):
        print("Veritabani sorgusu kullanicinin yetkilendirmesi var mi?")
        return redirect('/success')
        
    return render_template('login.html', form=form)    


@app.route("/classify-image", methods=['GET', 'POST'])
def classify_image():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            prediction = predict_model(filename=file_path)
            return jsonify({'prediction': prediction}) 
               
    return render_template("classify_image.html")


def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)




