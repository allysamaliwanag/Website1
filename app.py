from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from werkzeug.security import check_password_hash
from sqlalchemy import or_
from flask import session, flash
import bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask import render_template
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import Session
from collections import defaultdict
from flask import jsonify, make_response
from sqlalchemy.exc import NoResultFound
from enum import Enum

serializer = URLSafeTimedSerializer('your-secret-key')
app = Flask(__name__, static_folder='static')
app.secret_key = 'mysecretkey123'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/rfid'
app.config['UPLOAD_FOLDER'] = 'stdpics'


db = SQLAlchemy(app)

def save_image(file):
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath
    return None



class Report(db.Model):
   
    __tablename__ = 'reports'

    reportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    section = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.Text)
    role = db.Column(db.String(255))
    status = db.Column(db.String(255))
    grade_level = db.Column(db.String(255))
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    attendance = db.Column(db.String(10))
    role = db.Column(db.String(20), default='student')  # Default role is 'student'
    image = db.Column(db.String(255))  # Assuming you store the image path as a string
    studentID = db.Column(db.String(10), unique=True, nullable=False)  # Add the studentID field
    section = db.Column(db.String(50), nullable=True)
    grade_level = db.Column(db.String(255))
    nfcTag = db.Column(db.String(255))
    
    def __init__(self, username, password, name, email, studentID, attendance='Absent', role='student', image=None):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.name = name
        self.email = email
        self.attendance = attendance
        self.studentID = studentID  # Set the studentID
        self.role = role
        self.image = image

    @classmethod
    def get_all_students(cls):
        return cls.query.all()

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentID = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    grade_level = db.Column(db.String(255))
    date = db.Column(db.Date)
    status = db.Column(db.Enum('Present', 'Absent'))
    section = db.Column(db.String(255))


    def __init__(self, studentID, name, email, grade_level, date, status, section):
        self.studentID = studentID
        self.name = name
        self.email = email
        self.grade_level = grade_level
        self.date = date
        self.status = status
        self.section = section
    # Add any additional methods or properties as needed

    def __repr__(self):
        return f"<AttendanceRecord(studentID='{self.studentID}', date='{self.date}', status='{self.status}')>"


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacherID = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='teacher')  # Default role is 'teacher'
    image = db.Column(db.String(255))  # Assuming you store the image path as a string
    section = db.Column(db.String(50))
    grade_level = db.Column(db.String(255))
    
    def __init__(self, teacherID, username, password, name, email, section, role='teacher', image=None):
        self.teacherID = teacherID
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.section = section
        self.role = role
        self.image = image


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Received username: {username}, password: {password}")
        
        role = None  # Initialize role as None

        # Check for student login
        student = Student.query.filter_by(username=username).first()
        print(f"Student: {student}")
        if student and bcrypt.checkpw(password.encode('utf-8'), student.password.encode('utf-8')):
            role = 'student'

        # Check for teacher login
        teacher = Teacher.query.filter_by(username=username, password=password).first()
        if teacher:
            role = 'teacher'

        # Check for admin login
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            role = 'admin'

        if role:
            flash(f'Login successful as {role.capitalize()}!', 'success')
            username = username.strip()
            session['username'] = username  # Store the username in the session
        if role == 'student':
                flash(f'Login successful as {role.capitalize()}!', 'success')
                return redirect(url_for('student_dashboard'))
        elif role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
        elif role == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            # Invalid login
            flash('Invalid username or password. Please try again.', 'error')
            print(f"Role: {role}")

    return render_template('login.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Fetch the current admin user based on their identifier (e.g., username)
        username = "admin"  # Replace with the actual admin's username
        current_admin = Admin.query.filter_by(username=username).first()

        if not current_admin:
            flash('Admin not found', 'error')
        else:
            # Check if the old password matches the current admin's password (you can improve this logic)
            if current_admin.password != old_password:
                flash('Old password is incorrect', 'error')
            elif new_password != confirm_password:
                flash('New password and confirm password do not match', 'error')
            else:
                # Update the admin's password in the database
                current_admin.password = new_password  # You should hash the new password before storing it in a real application
                db.session.commit()
                flash('Password successfully updated', 'success')
                return redirect(url_for('admin_dashboard'))

    return render_template('reset_password.html')

# Update the /student_registration route
@app.route('/student_registration', methods=['GET', 'POST'])
def student_registration():
    if request.method == 'POST':
        student_id = request.form['studentID']
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        role = 'student'  # You can set the role directly

        # Handle image upload
        uploaded_file = request.files['profilePicture']
        image_path = save_image(uploaded_file)

        # Check if the username already exists
        existing_student = Student.query.filter_by(username=username).first()
        if existing_student:
            flash('Username already exists. Please choose another username.', 'error')
        else:
            # Create a new student record
            new_student = Student(studentID=student_id, username=username, password=password, name=name, email=email, role=role, image=image_path)

            # Add and commit the new student record to the database
            db.session.add(new_student)
            db.session.commit()

            flash('Student registration successful!', 'success')
            return redirect(url_for('student_registration'))

    return render_template('student_registration.html')

# routing
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))

@app.route('/student')
def student_dashboard():
    # Get the currently logged-in student based on their session
    username = session.get('username')  # Replace with the actual logged-in username
    
    if username:
        student = Student.query.filter_by(username=username).first()
        if student:
            student.image = 'stdpics/My_project.jpg'
            
            return render_template('student.html', student=student)
        else:
            flash('Student not found', 'error')
            print("Student not found in the database.")
    else:
        flash('Username not found in the session', 'error')
        print("Username not found in the session.")

    print("Redirecting to login page.")
    return redirect(url_for('login'))

@app.route('/register_teacher', methods=['POST'])
def register_teacher():
    if request.method == 'POST':
        teacherID = request.form['teacherID']
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        section = request.form['section']
        
        # Handle image upload
        uploaded_file = request.files['profilePicture']
        image_path = save_image(uploaded_file)

        # Check if the username already exists
        existing_teacher = Teacher.query.filter_by(username=username).first()
        if existing_teacher:
            flash('Username already exists. Please choose another username.', 'error')
        else:
            # Create a new teacher record
            new_teacher = Teacher(teacherID=teacherID, username=username, password=password, name=name, email=email,section=section, image=image_path)

            # Add and commit the new teacher record to the database
            db.session.add(new_teacher)
            db.session.commit()

            flash('Teacher registration successful!', 'success')
            return redirect(url_for('teacher_registration'))

    return render_template('teacher_registration.html')

@app.route('/manage_reports')
def manage_reports():
    return render_template('reports.html')

@app.route('/teacher')
def teacher_dashboard():
    teacher_username = session.get('username')
    if teacher_username:
        teacher = Teacher.query.filter_by(username=teacher_username).first()
        if teacher:
            teacher_section = teacher.section

            # Fetch student data for the teacher's section, including attendance data
            students = Student.query.filter_by(section=teacher_section).all()

            return render_template('teacher.html', teacher=teacher, students=students)
    
    return redirect(url_for('login'))

@app.route('/get_students_for_section', methods=['GET'])
def get_students_for_section():
    teacher_username = session.get('username')
    if teacher_username:
        teacher = Teacher.query.filter_by(username=teacher_username).first()
        if teacher:
            teacher_section = teacher.section  # Get the teacher's section

            # Fetch student data for the teacher's section
            students = Student.query.filter_by(section=teacher_section).all()

            # Prepare the student data as a list of dictionaries
            student_data = [{
                'studentID': student.studentID,
                'name': student.name,
                'email': student.email,
                'section': student.section
            } for student in students]

            return jsonify(student_data)

    return jsonify([])  # Return an empty list if no students found or teacher not found
 # Return an empty list if no students found or teacher not found

@app.route('/manage_users', methods=['GET'])
def manage_users():
    return render_template('manage_users.html')

@app.route('/teacher_registration', methods=['GET'])
def teacher_registration():
    return render_template('teacher_registration.html')

@app.route('/search_students', methods=['POST'])
def search_students():
    search_query = request.form.get('searchQuery')
    teacher_section = request.form.get('teacherSection')  # Get the teacher's section from the request

    students = Student.query.filter(Student.studentID.ilike(f'%{search_query}%'))

    # Filter students based on the teacher's section
    if teacher_section:
        students = students.filter(Student.section == teacher_section)

    students = students.all()

    student_data = [{'studentID': student.studentID, 'name': student.name, 'email': student.email, 'section': student.section} for student in students]

    return jsonify({'data': student_data, 'success': True})

@app.route('/admin_registration', methods=['GET'])
def admin_registration_form():
    return render_template('admin_registration.html')

# Create a route to handle the form submission
@app.route('/admin_register', methods=['POST'])
def admin_register():
    # Get data from the form
    username = request.form['username']
    password = request.form['password']

    admin = Admin(username=username, password=password)
    db.session.add(admin)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/get_reports', methods=['GET'])
def get_reports():
    
    reports = Report.query.all()  # This retrieves all reports from the database

    # Create a list to store report data
    report_data = []

    for report in reports:
        # Assuming that the `grade_level` attribute is available in your Report model
        report_data.append({
            'reportID': report.reportID,
            'name': report.name,
            'section': report.section,
            'timestamp': report.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Format the timestamp
            'description': report.description,
            'role': report.role,
            'status': report.status,
            'grade_level': report.grade_level  # Include grade_level in the response
        })

    return jsonify({'data': report_data})

@app.route('/mark_resolved', methods=['POST'])
def mark_resolved():
    data = request.get_json()
    report_ids = data.get('reportIDs')

    if report_ids:
        # Update the status of the selected reports to 'Solved' in the database
        for report_id in report_ids:
            report = Report.query.get(report_id)
            if report:
                report.status = 'Resolved'
                db.session.commit()
            else:
                # Handle the case where the report doesn't exist
                pass  # You can add your error handling logic here

        return jsonify({'message': 'Reports marked as resolved successfully'})
    else:
        return jsonify({'error': 'No report IDs provided'}), 400
    
@app.route('/mark_unresolved', methods=['POST'])
def mark_unresolved():
    data = request.get_json()
    report_ids = data.get('reportIDs')
 
    if report_ids:
        for report_id in report_ids:
            report = Report.query.get(report_id)
            if report:
                report.status = 'Unresolved'
                db.session.commit()
            else:
               pass 
        return jsonify({'message': 'Reports marked as Unresolved successfully'})
    else:
        return jsonify({'error': 'No report IDs provided'}), 400

@app.route('/delete_reports', methods=['POST'])
def delete_reports():
    try:
        data = request.get_json()
        report_ids = data.get('reportIDs')

        # Validate and ensure that the report_ids are integers

        for report_id in report_ids:
            if not report_id.isdigit():
                return jsonify({'error': 'Invalid report ID format'})

        # Delete the selected reports from the database
        for report_id in report_ids:
            report = Report.query.get(report_id)
            if report:
                db.session.delete(report)

        db.session.commit()

        return jsonify({'message': 'Reports deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)})
 
@app.route('/update_teacher_section/<teacher_id>', methods=['POST'])
def update_teacher_section(teacher_id):
    new_section = request.form.get('newSection')

    # Update the teacher's section in the database (replace with your actual database operation)
    teacher = Teacher.query.filter_by(teacherID=teacher_id).first()
    if teacher:
        teacher.section = new_section
        db.session.commit()
        flash('Section updated successfully!', 'success')
    else:
        flash('Teacher not found', 'error')

    return redirect(url_for('teacher_dashboard'))

@app.route('/get_reports_for_section', methods=['GET'])
def get_reports_for_section():
    teacher_username = session.get('username')
    if teacher_username:
        teacher = Teacher.query.filter_by(username=teacher_username).first()
        if teacher:
            teacher_section = teacher.section

            # Filter reports by the teacher's section
            reports = Report.query.filter_by(section=teacher_section, status='Unresolved').all()

            # Prepare the report data as a list of dictionaries
            report_data = [{
                'name': report.name,
                'section': report.section,
                'timestamp': report.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Format the timestamp
                'description': report.description,
                'status': report.status
            } for report in reports]

            return jsonify(report_data)
    
    return jsonify([]) 
        
@app.route('/get_attendance_for_section', methods=['GET'])
def get_attendance_for_section():
    teacher_username = session.get('username')
    if teacher_username:
        teacher = Teacher.query.filter_by(username=teacher_username).first()
        if teacher:
            teacher_section = teacher.section

            # Fetch attendance data for the teacher's section from the database
            # Replace this with your actual data fetching logic
            students = Student.query.filter_by(section=teacher_section).all()

            # Prepare the attendance data as a list of dictionaries
            student_data = [{
                'studentID': student.studentID,
                'name': student.name,
                'attendance': student.attendance
            } for student in students]

            return jsonify(student_data)

    return jsonify([])
    # Return an empty list if no data found or teacher not found

# Example route to fetch students for a teacher's advising class and grade level
@app.route('/get_students_for_section_and_grade', methods=['GET'])
def get_students_for_section_and_grade():
    teacher_username = session.get('username')
    if teacher_username:
        teacher = Teacher.query.filter_by(username=teacher_username).first()
        if teacher:
            teacher_section = teacher.section
            teacher_grade_level = teacher.grade_level  # Get the teacher's grade level

            # Fetch student data for the teacher's section and grade level
            students = Student.query.filter_by(section=teacher_section, grade_level=teacher_grade_level).all()

            # Prepare the student data as a list of dictionaries
            student_data = [{
                'studentID': student.studentID,
                'name': student.name,
                'email': student.email,
                'section': student.section,
                'grade_level': student.grade_level
            } for student in students]

            return jsonify(student_data)

    return jsonify([])  # Return an empty list if no students found or teacher not found

@app.route('/attendance')
def view_attendance():
    # Get the currently logged-in username from the session
    username = session.get('username')

    # Initialize student_attendance to an empty list
    student_attendance = []

    # Query the attendance data based on the role (student or teacher) and the username
    if username:
        if username.startswith("student"):
            # For students, you need to use their studentID in the query
            student_attendance = AttendanceRecord.query.filter_by(student_id=username).all()
        elif username.startswith("teacher"):
            # For teachers, you need to use their section to filter the student attendance data
            teacher = Teacher.query.filter_by(username=username).first()
            if teacher:
                teacher_section = teacher.section
                student_attendance = AttendanceRecord.query.filter_by(grade_level=teacher.grade_level, section=teacher_section).all()

    return render_template('student.html', student_attendance=student_attendance)


@app.route('/get_all_students', methods=['GET'])
def get_all_students():
    try:
        students = Student.get_all_students()

        student_details = []
        for student in students:
            student_details.append({
                'studentID': student.studentID,
                'name': student.name,
                'email': student.email,
                'section': student.section,
                'grade_level': student.grade_level,
                'nfcTag': student.nfcTag,
                # Add more fields as needed
            })

        return jsonify(student_details)

    except Exception as e:
        # Log the exception for debugging
        print(f"Error fetching student records: {str(e)}")
        
        # Return an error response
        error_message = "An error occurred while fetching student records."
        return make_response(jsonify(error=error_message), 500)

@app.route('/search_student', methods=['GET'])
def search_student():
    student_id = request.args.get('studentID')  # Get the studentID from the request

    # Assuming you're using SQLAlchemy to interact with the database, replace this with your actual data retrieval logic
    student_data = Student.query.filter_by(studentID=student_id).first()

    if student_data:
        # Convert the student data to a dictionary and return it as JSON
        return jsonify({
            'studentID': student_data.studentID,
            'name': student_data.name,
            'email': student_data.email,
            'section': student_data.section,
            'attendance': student_data.attendance
            # Add other fields as needed
        })
    else:
        return jsonify({'error': 'Student not found'})

@app.route('/get_teacher_for_student', methods=['GET'])
def get_teacher_for_student():
    student_username = session.get('username')
    
    if student_username:
        student = Student.query.filter_by(username=student_username).first()
        
        if student:
            student_section = student.section  # Get the student's section
            student_grade_level = student.grade_level  # Get the student's grade level

            # Fetch the teacher with the same section and grade level as the student
            teacher = Teacher.query.filter_by(section=student_section, grade_level=student_grade_level).first()

            if teacher:
                teacher_info = {
                    'name': teacher.name,
                    'email': teacher.email,
                    'section': teacher.section,
                    'grade_level': teacher.grade_level
                }
                return jsonify(teacher_info)
            else:
                return jsonify({'error': 'Teacher not found for this section and grade level'})
        else:
            return jsonify({'error': 'Student not found'})
    else:
        return jsonify({'error': 'Student username not available'})


@app.route('/get_student_data', methods=['GET'])
def get_student_data():
    student_id = request.args.get('studentID')
    student = Student.query.filter_by(studentID=student_id).first()
    if student:
        student_data = {
            "studentID": student.studentID,
            "name": student.name,
            "email": student.email,
            "attendance": student.attendance,
            "section": student.section,
            "grade_level": student.grade_level,
            "nfcTag": student.nfcTag
            # Add more fields as needed
        }
        return jsonify(student_data)
    else:
        return jsonify({'error': 'Student not found'}, 404)

@app.route('/update_student_data/<string:student_id>', methods=['POST'])
def update_student_data(student_id):
    # Retrieve the student record from the database using the student ID
    student = Student.query.filter_by(studentID=student_id).first()

    if student:
        # Get the JSON data sent from the front-end
        data = request.json

        # Check if the data dictionary is not None
        if data is not None:
            # Update the student's data based on the JSON data
            student.name = data.get('name')
            student.email = data.get('email')
            student.nfcTag = data.get('nfcTag')
            student.section = data.get('section')
            student.grade_level = data.get('grade_level')

            # Commit the changes to the database
            db.session.commit()

            return jsonify({'message': 'Student data updated successfully'})
        else:
            return jsonify({'message': 'Invalid JSON data'}, 400)
    else:
        return jsonify({'message': 'Student not found'}, 404)

@app.route('/get_initial_attendance_data', methods=['GET'])
def get_initial_attendance_data():
    try:
        teacher_username = session.get('username')
        if teacher_username:
            teacher = Teacher.query.filter_by(username=teacher_username).first()
            if teacher:
                teacher_grade_level = teacher.grade_level
                teacher_section = teacher.section

                # Filter attendance records based on teacher's grade_level and section
                attendance_records = AttendanceRecord.query.filter_by(grade_level=teacher_grade_level, section=teacher_section).all()

                data = [
                    {
                        'studentID': record.studentID,
                        'name': record.name,
                        'email': record.email,
                        'date': record.date.strftime('%Y-%m-%d'),
                        'status': record.status,
                        'section': record.section
                    }
                    for record in attendance_records
                ]

                return jsonify(data)

        return jsonify([])  # No teacher data found in the session

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get filtered attendance data
@app.route('/get_filtered_attendance', methods=['POST'])
def get_filtered_attendance():
    try:
        filter_data = request.get_json()
        date = filter_data.get('date')
        status = filter_data.get('status')
        teacher_username = session.get('username')

        if teacher_username:
            teacher = Teacher.query.filter_by(username=teacher_username).first()
            if teacher:
                teacher_grade_level = teacher.grade_level
                teacher_section = teacher.section

                # Construct the filtering conditions
                date_condition = or_(
                    AttendanceRecord.date == date,
                    AttendanceRecord.date.ilike(f'%{date}%')
                )
                status_condition = or_(
                    AttendanceRecord.status == status,
                    AttendanceRecord.status.ilike(f'%{status}%')
                )

                # Apply the filters to the query
                filtered_data = AttendanceRecord.query.filter(
                    date_condition, status_condition,
                    AttendanceRecord.grade_level == teacher_grade_level,
                    AttendanceRecord.section == teacher_section
                ).all()

                data = [
                    {
                        'studentID': record.studentID,
                        'name': record.name,
                        'email': record.email,
                        'date': record.date.strftime('%Y-%m-%d'),
                        'status': record.status,
                        'section': record.section
                    }
                    for record in filtered_data
                ]

                return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify([])


@app.route('/get_filtered_attendance_records', methods=['GET'])
def get_filtered_attendance_records():
    if 'username' in session:
        username = session['username']

        # Query the database for the student's information based on the username
        student = Student.query.filter_by(username=username).first()

        if student:
            studentID = student.studentID
            selected_date = request.args.get('selectedDate')
            status_filter = request.args.get('statusFilter')

            # Query the database for attendance records based on studentID, date range, and status
            query = AttendanceRecord.query.filter_by(studentID=studentID)

            if selected_date:
                query = query.filter(AttendanceRecord.date == selected_date)
            if status_filter:
                query = query.filter(AttendanceRecord.status == status_filter)

            attendance_records = query.all()

            # Prepare the data to send to the frontend
            records_data = []
            for record in attendance_records:
                records_data.append({
                    'date': record.date.strftime('%Y-%m-%d'),
                    'status': record.status,
                })

            return jsonify(records_data)
        else:
            return jsonify({'error': 'Student not found'})
    else:
        return jsonify({'error': 'Session not established'})

@app.route('/delete_selected', methods=['POST'])
def delete_selected():
    data = request.get_json()
    report_ids = data.get('reportIDs')

    if report_ids:
        for report_id in report_ids:
            report = Report.query.get(report_id)
            if report:
                db.session.delete(report)
                db.session.commit()
            else:
                pass  # Handle the case where the report doesn't exist

        return jsonify({'message': 'Selected reports deleted successfully'})
    else:
        return jsonify({'error': 'No report IDs provided'}), 400
    
@app.route('/search_users', methods=['POST'])
def search_users():
    search_query = request.form['search_query']
    
    # Query both Student and Teacher tables for the search_query
    students = Student.query.filter(Student.name.like(f'%{search_query}%')).all()
    teachers = Teacher.query.filter(Teacher.name.like(f'%{search_query}%')).all()
    
    # Convert the results to dictionaries for JSON serialization
    student_data = [{'id': student.studentID, 'name': student.name, 'email': student.email, 'role': student.role, 'section': student.section} for student in students]
    teacher_data = [{'id': teacher.teacherID, 'name': teacher.name, 'email': teacher.email, 'role': teacher.role, 'section': teacher.section} for teacher in teachers]
    
    return jsonify({'students': student_data, 'teachers': teacher_data})

@app.route('/delete_user', methods=['POST'])
def delete_user():
    role = request.form['role']  # Get the role (student or teacher)
    user_id = request.form['userId']  # Get the user ID
    print(f"User ID: {user_id}, Role: {role}")
    
    if role == 'student':
        # Check if it's a student and delete by studentID
        student = Student.query.filter_by(studentID=user_id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({'message': 'Student deleted successfully'})

    elif role == 'teacher':
        # Check if it's a teacher and delete by teacherID
        teacher = Teacher.query.filter_by(teacherID=user_id).first()
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            return jsonify({'message': 'Teacher deleted successfully'})

    return jsonify({'error': 'User not found'})

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        user_id = request.form['userId']
        updated_name = request.form['name']
        updated_email = request.form['email']
        updated_role = request.form['role']
        updated_section = request.form['section']

        print(f'user_id: {user_id}, name: {updated_name}, email: {updated_email}, role: {updated_role}, section: {updated_section}')

        if updated_role == 'student':
            # Update a student
            student = Student.query.filter_by(id=user_id).first()
            if student:
                student.name = updated_name
                student.email = updated_email
                student.section = updated_section
            else:
                return jsonify({'message': 'Student not found'})

        elif updated_role == 'teacher':
            # Update a teacher
            teacher = Teacher.query.filter_by(id=user_id).first()
            if teacher:
                teacher.name = updated_name
                teacher.email = updated_email
                teacher.section = updated_section
            else:
                return jsonify({'message': 'Teacher not found'})
        else:
            return jsonify({'message': 'Invalid role'})

        db.session.commit()
        return jsonify({'message': 'Update successful'})

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': 'Update failed', 'error': str(e)})




   
if __name__ == '__main__':
    app.run(debug=True)