# Attend-Up

## Introduction
 An attendance tracking system, using the facial recognition feature simplifies the task of manually logging attendance.
 Facial recognition is one of the most important biometric recognition techniques. Have implemented it using dlib's state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on the Labeled Faces in the Wild benchmark.

## Table of Contents
1. [Functionality Supported](#functionality-supported)
2. [Built using](#Built-using)
3. [Instructions to run](#Instructions-to-run)
4. [The Web Application](#The-Web-Application)



## Functionality Supported
 * Admin login
 * Register new employees by adding employee photo to the training dataset.
 * View attendance records of all employees. Attendance can be filtered by date or employee.
 * You can also delete an employees image and data with their name.



## Built using
 * OpenCV - Open Source Computer Vision and Machine Learning software library.
 * Dlib - C++ Library containing Machine Learning Algorithms.
 * face_recognition by Adam Geitgey.
 * Flask - Python framework for web development.

 ## Face Detection
 * Dlib's HOG facial detector.

 ## Facial Landmark Detection
 * Dlib's 68 point shape predictor.

 ## Extraction of Facial Embeddings
 * face_recognition by Adam Geitgey.



## Instructions to run
 * Clone the project and download the source code.
 * Read install.txt and download the requirements.
 * Once inside the folder, run the following command: python3 app.py
 * Go to: localhost:5500 in your browser
 * Log in with username: admin and password: 1234.
 * First Register yourself by clicking on add user.
 * Log your attendance by clicking on mark attendance.

 

## The Web Application

 ![image](https://user-images.githubusercontent.com/86554470/170824448-5480c7c6-1c4b-41e7-b2b2-404c8cf54ae1.png)

 ![image](https://user-images.githubusercontent.com/86554470/170824504-a2cfece5-6d2d-414c-a2f0-76612d2d0e73.png)

 ![image](https://user-images.githubusercontent.com/86554470/170824532-7181375c-be44-4c00-9174-872189909f25.png)

 ![image](https://user-images.githubusercontent.com/86554470/170824559-e6f34965-f1c5-4725-ac02-1448c4b3b8f3.png)

