
import firebase_admin
from firebase_admin import credentials, firestore
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import dropbox
from dropbox.files import WriteMode

load_dotenv()

def connect(): # Connect to  Firebase
   
    #firestore configuration
    cred = credentials.Certificate(os.getenv('FIREBASE_SDK'))
    firebase_admin.initialize_app(cred)
    print('Firebase connected')


def rename_file(Class,Section,Subject,Date): # Provide a new name for the PDF file to the format Class_Section_Subject_Date 
    time = str(datetime.now())
    time = time.replace(' ', '__')
    time = time.replace(':', '_')
    time = time.replace('.', '_')
    file_new_name = f'{Class}_{Section}_{Subject}_{Date}_{time}'
    print('Updated Name:',file_new_name)
    return file_new_name


def file_upload(file_path,new_name,access_token): # Upload the file to Dropbox and return the URL
     # Dropbox Configuration   
    dbx = dropbox.Dropbox(access_token)
    print('Dropbox connected')
    dropbox_path = f'/Assignments/{new_name}.pdf'
    file = file_path.read()
    dbx.files_upload(file, dropbox_path, mode=WriteMode('overwrite'))
    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
    link = shared_link_metadata.url.replace('dl=0', 'raw=1')
    print('File uploaded')
    return link


def store_metadata(class_name, section, subject, file_url, date, notes = "Not Added"): # Store the metadata in Firestore arguments are class name, section, subject, file url, date and notes respectively
    data = {
        "class": class_name,
        "section": section,
        "subject": subject,
        "notes": notes,
        "date": date,
        "file_url": file_url,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    db = firestore.client()
    
    try:
        db.collection("assignments").add(data)
        print("Document added.")
    except Exception as e:
        print("Error adding document:", e)

def login(username,password): #Login Funtion for teachers to uplaod the data 
    db =firestore.client()
    username = username.lower().replace(' ', '')
    password = password.lower().replace(' ', '')
    try:
        docs = db.collection("Users").where('Username', '==', username).where('Password', '==', password).get()
        if docs:
            for doc in docs:
                print(f'Login Succesfully\n Name = {doc.to_dict()['Name']}\n Username = {doc.to_dict()['Username']}\n Subject = {doc.to_dict()['Subject']}')
                return True, doc.to_dict()['Name'],doc.to_dict()['Username'], doc.to_dict()['Subject']
        else:
            print('Invalid username or password')
            return False, None, None, None
    except Exception as e: 
        print('Error fetching document:', e)
        return False, None, None, None
    
def register(user,username,password,subject):# Register function for teachers to register themselves in the database
    db = firestore.client()
    username = username.lower().replace(' ', '')
    password = password.lower().replace(' ', '')
    try:
        docs = db.collection('Users').where('Username', '==', username).where("Password", '==', password).get()
        if docs:
            print('username already exists')
            return False
        else:
            data = {
                'Name': user,
                'Username': username,
                'Password': password,
                'Subject': subject
            }
            check = db.collection('Users').add(data)
            print('User regirstered succesfully')
            return True
    except Exception as e:
        print('Error fetching document:', e)
        return False
    
def student (Class,Section, Subject, Date):
    db = firestore.client()
    try:
        docs = db.collection('assignments').where('class', '==', Class).where('subject', '==', Subject).where('section', '==', Section).where('date', '==', Date).get()
        if docs:
            for doc in docs:
                print(f"Document ID: {doc.id} => {doc.to_dict()}")
                data = doc.to_dict()
                return data['class'], data['section'], data['subject'], data['notes'], data['date'], data['file_url']
        else:
            print('No data found')
    except Exception as e:
        print('Error fetching document:', e)



def get_access_token():
    url = "https://api.dropboxapi.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("REFRESH_TOKEN"),
    }
    auth = (os.getenv("API_KEY"), os.getenv("API_SECRET"))

    response = requests.post(url, data=data, auth=auth)
    
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    else:
        print("Failed to get access token:", response.text)
        return None




