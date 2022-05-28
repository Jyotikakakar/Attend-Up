import face_recognition as fr
import cv2
import os
import re

"""
user_one = fr.load_image_file("Bradley2.jpg")
f_loc = fr.face_locations(user_one)[0]
f_enc = fr.face_encodings(user_one)[0]

user_two = fr.load_image_file("user_two.jpg")
ftwo_loc = fr.face_locations(user_two)[0]
ftwo_enc = fr.face_encodings(user_two)[0]

results = fr.compare_faces([f_enc], ftwo_enc)
print(results)
"""

# Declare all the list
known_face_encodings = []
known_face_names = []
known_faces_filenames = []

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
#print(known_faces_filenames)

