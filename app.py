from flask import Flask, request, jsonify, render_template, session, Response
from flask_cors import CORS, cross_origin
import os
import psycopg2
import cv2
import numpy as np
import re
import json
import face_recognition as fr
import time
import requests

# We define the path of the current file
FILE_PATH = os.path.dirname(os.path.realpath(__file__))


# Create App
app = Flask(__name__)
# To avoid cors erros (idk)
CORS(app, support_credentials=True)

known_face_encodings = []
known_face_names = []
known_faces_filenames = []

@app.route('/')
@app.route('/home', methods = ['GET'] )
def home():
   return render_template('index.html')

def dataset():

    # known_face_encodings = []
    # known_face_names = []
    # known_faces_filenames = []

    
    # Walk in the folder to add every file name to known_faces_filenames
    for (dirpath, dirnames, filenames) in os.walk('knownusers/img/users/'):
        known_faces_filenames.extend(filenames)
        break

    for filename in known_faces_filenames:

        face = fr.load_image_file('knownusers/img/users/' + filename)

        # Extract the name of each employee and add it to known_face_names, here using re.sub() to replace numbers with empty string till the extension 
        known_face_names.append(re.sub("[0-9]",'', filename[:-4]))

        # Encode the face of every employee
        known_face_encodings.append(fr.face_encodings(face)[0])

    print(known_face_names)


@app.route('/get_data', methods = ['POST'] )
def data():
   return render_template('getdata.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    render_template('login.html')
    usname = 'admin'
    pwd = '1234'
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        if username == usname and password == pwd:
            session['loggedin'] = True
            session['username'] = username
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


# * ---------- Capture image -------- *
@app.route('/capture', methods=['POST', 'GET'])
def capture():
    dataset()
    return render_template('facerec.html')
    

def gen_frames():  # generate frame by frame from camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            capture(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def capture(frame):

    # Find all the faces and face encodings in the current frame of video
    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)

    # Initialize an array for the name of the detected users
    face_names = []

    json_to_export = {}

    # Loop in every faces detected
    for face_encoding in face_encodings:

        # See if there is a match
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # check the known face with the smallest distance to the new face
        face_distances = fr.face_distance(known_face_encodings, face_encoding)

        # Take the best one
        best_match_index = np.argmin(face_distances)

        # If we have a match
        if matches[best_match_index]:
            name = known_face_names[best_match_index]


                # * ---------- SAVE data to send to the API -------- *
            json_to_export['name'] = name
            json_to_export['hour'] = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
            json_to_export['date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
            # If you need to save a screenshot:
            json_to_export['picture_array'] = frame.tolist()

            date = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
            t = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'

                # * ---------- SEND data to API --------- *
                # Make a POST request to the API
            #r = request.post(url='http://127.0.0.1:5500/recieve_data', json=json_to_export)

            url = "http://127.0.0.1:5500/recieve_data"
            #data = {'name': name , 'hour': f'{time.localtime().tm_hour}:{time.localtime().tm_min}' , 'date': f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'}
            r = requests.get(f"http://127.0.0.1:5500/recieve_data?name={name}&date={date}&time={t}")
            
                # Print to status of the request:
            print("Status: ", r.status_code)

        # Store the name in an array to display it later
        face_names.append(name)

        # * --------- Display the results ---------- *
    for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Define the font of the name
        font = cv2.FONT_HERSHEY_DUPLEX
            # Display the name
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # Display the resulting image
    #cv2.imshow('Video', frame)
    #wait for 2 minutes
    #time.sleep(2)
    #cv2.destroyAllWindows()

@app.route('/attendance', methods=['GET'])
def attendance():
    return render_template('dashboard.html')

@app.route('/adduser', methods=['GET'])
def adduser():
    return render_template('adduser.html')

# * ---------- Get data from the face recognition ---------- *
@app.route('/recieve_data')
def get_data():
    params = request.args
    name = params['name']
    date = params['date']
    time = params['time']

    # if request.method == 'POST':
    #     print("route called")
    #     # Get the data
    #     json_data = request.get_json()
    #     print(json_data['name'])

    #     # Check if the user is already in the DB
    try:
        connection = psycopg2.connect(host='localhost', user='postgres',password='root1234', dbname='facerec', port=5432)
        cursor = connection.cursor()

        today =\
            f"SELECT * FROM users WHERE date = '{date}' AND name = '{name}'"
        cursor.execute(today)
        
        result = cursor.fetchall()

        if result:
            #update dep time
            update_user_query = f"UPDATE users SET departure_time = '{time}' WHERE name = '{name}' AND date = '{date}'"
            cursor.execute(update_user_query)
            connection.commit()

        else:
            #Create a new row for the user today
            insert_user_query = f"INSERT INTO users (name, date, arrival_time) VALUES ('{name}', '{date}', '{time}')"
            print(name)
            cursor.execute(insert_user_query)

        print("Result saved")

    except (Exception, psycopg2.DatabaseError) as error:
        print("database error: ", error)

    finally:
        connection.commit()
        if connection:
            cursor.close()
            connection.close()

            print("db connection closed")
            
    return "Data saved"

# * ---------- Get all the data of an employee ---------- *
@app.route('/get_employee/<string:name>', methods=['GET'])
def get_employee(name):
    answer_to_send = {}
    # Check if the user is already in the DB
    try:
        connection = psycopg2.connect(host='localhost', user='postgres',password='root1234', dbname='facerec', port=5432)
        cursor = connection.cursor()
        user_information = f"SELECT * FROM users WHERE name = '{name}'"
        cursor.execute(user_information)
        result = cursor.fetchall()
        connection.commit()
        # if the user exist in the db:
        if result:
            print('RESULT: ',result)
            # Structure the data and put the dates in string for the front
            for k,v in enumerate(result):
                answer_to_send[k] = {}
                for ko,vo in enumerate(result[k]):
                    answer_to_send[k][ko] = str(vo)
            print('answer_to_send: ', answer_to_send)
        else:
            answer_to_send = {'error': 'User not found...'}

    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return jsonify(answer_to_send)

# * --------- Get users data seen by the camera --------- *
@app.route('/spec_data', methods=['GET', 'POST'])
def get_spec_entries():
    print("hi")
    new_users = []
    # Check if the user is already in the DB
    if request.method == "POST":
        try:
            value = request.form.get("emp")
            print(value)
            connection = psycopg2.connect(host='localhost', user='postgres',password='root1234', dbname='facerec', port=5432)
            cursor = connection.cursor()
            last_entries = f"select * from users where name = '{value}' OR date = '{value}' ;"
            cursor.execute(last_entries)
            new_users = cursor.fetchall()
            # Send the request
            connection.commit()
            # if DB is not empty:
            if new_users:
                print("result printed")
            else:
                print("'error': 'DB is not connected or empty'")
        except (Exception, psycopg2.DatabaseError) as error:
            print("ERROR DB: ", error)
        print("hi")
        print(new_users)
    return render_template('getdata.html', users=new_users)


# * --------- Get users data seen by the camera --------- *
@app.route('/get_entries', methods=['GET', 'POST'])
def get_entries():
    print("hi")
    # Check if the user is already in the DB
    try:
        connection = psycopg2.connect(host='localhost', user='postgres',password='root1234', dbname='facerec', port=5432)
        cursor = connection.cursor()
        lasts_entries = f"SELECT * FROM users order by date desc;"
        cursor.execute(lasts_entries)
        users = cursor.fetchall()
        # Send the request
        connection.commit()
        # if DB is not empty:
        if users:
            print("result printed")
        else:
            print("'error': 'DB is not connected or empty'")
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    print("hi")
    print(users)
    return render_template('getdata.html', users=users)

# * ---------- Add new employee ---------- *
@app.route('/add_employee', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def add_employee():
    render_template('adduser.html')
    answer = ''
    if request.method == 'POST':
        try:
            # Get the picture from the request
            image_file = request.files['image']
            # Get the name from the request
            name = request.form['nameOfEmployee']
            # Store it in the folder of the know faces:
            file_path = os.path.join("knownusers/img/users", (name+".jpg"))
            image_file.save(file_path)
            answer = 'new employee succesfully added'
        except:
            answer = 'Error while adding new employee. Please try later'
        
    return render_template('adduser.html', jsonfile=json.dumps(answer))

# * ---------- Get employee list ---------- *
@app.route('/get_employee_list', methods=['GET'])
def get_employee_list():
    # Create a dict that will store the list of employee's name
    employee_list = {}
    # Walk in the user's folder to get the user list
    count = 0
    for file_name in os.listdir(f"{FILE_PATH}/knownusers/img/users/"):
        # Capture the employee's name with the file's name
        name = re.findall("(.*)\.jpg", file_name)
        if name:
            employee_list[count] = name[0]
        count += 1
    return jsonify(employee_list)

# * ---------- Delete employee ---------- *
@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    answer = " "
    print("Im here")
    if request.method == "POST":
       try:
            name = request.form.get("empname")
            print(name)
            file_path = os.path.join(f'knownusers/img/users/{name}.jpg')
            # Remove the picture of the employee from the user's folder:
            os.remove(file_path)
            connection = psycopg2.connect(host='localhost', user='postgres',password='root1234', dbname='facerec', port=5432)
            cursor = connection.cursor()
            delete = f"delete from users where name = '{name}';"
            cursor.execute(delete)
            connection.commit()
            answer = 'Employee succesfully removed'
       except:
            answer = 'Error while deleting new employee. Please try later'

    return render_template('deleteuser.html', jsonfile=json.dumps(answer))

# * -------------------- Run Server -------------------- *
if __name__ == '__main__':
    # * --- DEBUG MODE: --- *
    app.run(host='127.0.0.1', port=5500, debug=True)