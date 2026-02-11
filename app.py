from flask import Flask, render_template, request
from functions import login, connect, rename_file, file_upload, store_metadata, student, register, get_access_token

app = Flask(__name__)
connect()

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    check, name, user, subject = login(username, password)
    if check:
        return render_template('upload.html', teacher_subject = subject, teacher_name = name, teacher_username = user)
    else:
        return render_template('login.html', error='Invalid credentials')
    
@app.route('/upload')
def upload_page():
    teacher_name = request.args.get('teacher_name')
    teacher_username = request.args.get('teacher_username')
    teacher_subject = request.args.get('teacher_subject')
    return render_template(
        'upload.html',
        teacher_name=teacher_name,
        teacher_username=teacher_username,
        teacher_subject=teacher_subject)

@app.route('/upload', methods=['POST'])
def upload_post():
    file = request.files['assignment_file']
    class_name = request.form['class']
    section = request.form['section']
    subject = request.form['teacher_subject'].lower()
    date = request.form['date']
    teacher_username = request.form['teacher_username']
    teacher_name = request.form['teacher_name']
    notes = request.form['notes']

    if file and class_name and section and subject and date:
        name  = rename_file(class_name, section,subject, date)
        access_token = get_access_token()
        file_link = file_upload(file,name,access_token)
        store_metadata(class_name, section, subject, file_link, date, notes)
        return render_template(
            'upload_success.html',
            file_link=file_link,
            class_name=class_name,
            section=section,
            teacher_subject=subject,
            date=date,
            notes=notes,
            teacher_username=teacher_username,
            teacher_name=teacher_name
        )
    else:
        return render_template('upload.html', error='Please fill all the fields')
@app.route('/assignments', methods=['POST'])
def assignments_fetch():
    class_name = request.form['class']
    section = request.form['section']  
    subject = request.form['subject'].lower()
    date = request.form['date']
    try:
        Class, Section, Subject, Notes, Date, File_url = student(class_name, section, subject, date)
        return render_template('assignments_success.html', class_name=Class, section=Section, subject=Subject, date=Date, notes=Notes, file_url=File_url)
    except Exception as e:
        print('Error fetching document:', e)
        return render_template('assignments.html', error='No data found')
    
@app.route('/assignments')
def assignments_page():
    return render_template('assignments.html')

@app.route('/teacherregistration')
def register_page():
    return render_template('register.html')
@app.route('/teacherregistration', methods=['POST'])
def registeration():
    username = request.form['username']
    password = request.form['password']
    rpassword = request.form['rpassword']
    name = request.form['name']
    subject = request.form['subject']
    if password == rpassword:
        check = register(name, username, password, subject)
        if check :
            return render_template('register_success.html', name = name, username = username, password = password, subject = subject)
        else:
            return render_template('register.html', error='Username already exists')


if __name__ == '__main__':
    app.run(debug=True)
