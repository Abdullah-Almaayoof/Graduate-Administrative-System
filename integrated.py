import csv
from pickle import FALSE
from datetime import date
from xml.dom.minidom import Identified
from flask import Flask
from flask import render_template, session, redirect, url_for, request
import mysql.connector, re

app = Flask(__name__)
app.secret_key = "LITERALLYANTHING"

mydb = mysql.connector.connect(
    host = "gib.c8rnuhqze26n.us-east-1.rds.amazonaws.com",
    user = "admin",
    password = "M5jp2GbGDqEW",
    database = "university"
)


@app.route("/", methods = ['GET', 'POST'])
def login():
    # session.clear()
    ##Error Message
    msg = ""
    
    c = mydb.cursor(dictionary = True)
    
    if "username" in session:
        return redirect('/info')
        
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        # print(username)
        # print(password)

        ##select statement into database and check if email and password exist there
        c.execute("Select * from users where uname = %s and password = %s", (username, password,))
        results = c.fetchone()
        c.close()

        ##check to see if user input is in database
        # print(results)
        if results == None:
            msg = "Not found, try again"
            return render_template('login.html', error = msg)
        else:
            session['username'] = username
            session['id'] = results['uid']
            session['fname'] = results['fname']
            session['lname'] = results['lname']
            if results['role'] != 'student':
                session['facultytype'] = results['role']
            session['reg'] = []
            return redirect('/info')
    
    
    return render_template('login.html', error = msg)


##What is the POINT IN THIS ROUTE
@app.route("/apply_to_graduate", methods = ['GET','POST'])
def apply_to_graduate():
    if 'username' not in session:
        return redirect("/")


    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )


    c = mydb.cursor(dictionary = True)
    ##use to retrieve basic information on user
    username = session['username']
    c.execute("Select student_id from advises_on where fid = %s ", (username,))
    results = c.fetchall()
    c.close()

    # print (results)
    return render_template('login.html',name = username, results = results)

@app.route("/admin_student_facultyList", methods = ['GET','POST'])
def admin_student_facultyList():
    if 'username' not in session:
        return redirect("/")
    
    default_value = 0
       
    

    # mydb = mysql.connector.connect(
    # host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    # user = "admin",
    # password = "iGoByAdham$4*8",
    # database = "AdvisingSystem_ADS_3"  
    # )
    c = mydb.cursor(dictionary = True)
    ##use to retrieve basic information on user
    
    c.execute("Select * from advises_on")
    results = c.fetchall()

    username = session['username']

    if request.method == 'POST':
       
      
        if request.form.get('Button', default_value) == "Back to Home":
            return redirect('/info')
        
        data = request.form.get ("Delete" , default_value)
        if data == "Delete":
            student = request.form.get('student_id', default_value)
            faculty = request.form.get('faculty_id',default_value)
            # print(student)
            c.execute("DELETE FROM advises_on WHERE fid = %s AND student_id = %s", (faculty, student,))
            mydb.commit()
            c.execute("Select * from advises_on")
            results = c.fetchall()
            c.close()

            return render_template('admin_student_facultyList.html', username = username, results = results)
        return render_template('admin_student_facultyList.html', username = username, results = results)

    return render_template('admin_student_facultyList.html', username = username, results = results)



@app.route("/faculty_studentList", methods = ['GET','POST'])
def faculty_studentList():
    if 'username' not in session:
        return redirect("/")
    default_value = 0
    
    
    # mydb = mysql.connector.connect(
    # host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    # user = "admin",
    # password = "iGoByAdham$4*8",
    # database = "AdvisingSystem_ADS_3"  
    # )
    c = mydb.cursor(dictionary = True, buffered=True)
    ##use to retrieve basic information on user
    username = session['username']
    # print(username)

    ##COULD DO IF STATEMENT FOR SYS ADMIN THAT ALLOWS THEM VIEW ALL
    ##Check TYPE USER
    c.execute("SELECT * FROM users WHERE uname = %s LIMIT 1", (username,))
    results = 0
    syscheck = c.fetchone()


    if syscheck['role'] == 'system_admin' or syscheck['role'] == 'grad_secretary' or syscheck['role'] == 'cac':
        c.execute("SELECT * FROM users WHERE role = 'student'")
        results = c.fetchall()
        # print(results)
    elif (syscheck['role'] == 'system_admin' or syscheck['role'] == 'grad_secretary') and request.method == 'GET':
        query = "%"+request.args.get("query")+"%"
        c.execute("SELECT * FROM users WHERE role = 'student' and (fname LIKE %s or lname LIKE %s)", (query, query))
        results = c.fetchall()
    elif request.method == 'GET':
        query = "%"+request.args.get("query")+"%"
        c.execute("Select * from users INNER JOIN advises_on ON advises_on.student_id = users.uid WHERE advises_on.fid = %s AND (users.fname = %s OR users.lname = %s)", (syscheck['uid'], query, query))
        results = c.fetchall()
    else:
        c.execute("Select * from users INNER JOIN advises_on ON advises_on.student_id = users.uid where advises_on.fid = %s", (syscheck['uid'],))
        results = c.fetchall()


    if request.method == 'POST':
        if request.form.get('Button', default_value) == "Back to Home":
            return redirect('/info')
        if request.form.get('Button', default_value) == "Back to Student List":
            return render_template('faculty_studentList.html',name = username, results = results)
        
    if request.method == 'POST':
        default_value = 0
        data = request.form.get ("getStudent_Transcript" , default_value)
        if data == "Transcript":
            student = request.form.get('student_id2', default_value)
            # print(student)
            c.execute("Select fname from users where uname = %s", (student,))
            student_name = c.fetchone()
            c.execute("Select * from takes_course where studentid = %s", (student,))
            results = c.fetchall()
            if (results == [] or results == None):
               return render_template('student_Transcript.html',msg = "No Transcript on File", username = student_name,results = results) 
            c.close()
            return render_template('student_Transcript.html',msg = "", username = student_name,results = results)
        

        data2 = request.form.get ("programStudy" , default_value)
        if data2 == "Program Study":
            student = request.form.get('student_id', default_value)
            # print(student)
            c.execute("Select fname from users where uid = %s", (student,))
            student_name = c.fetchone()
            c.execute("Select * from program_study where univ_id = %s", (student,))
            results = c.fetchall()
            if (results == [] or results == None):
                return render_template('student_programstudy.html',msg = "No Program Study Found", username = student_name['fname'],results = results)
            c.close()
            return render_template('student_programstudy.html', msg = "", username = student_name['fname'],results = results)

    # print (results)
    return render_template('faculty_studentList.html',name = username, results = results)

@app.route("/faculty_studentListsearch", methods = ['GET','POST'])
def faculty_studentListsearch():
    if 'username' not in session:
        return redirect("/")
    default_value = 0
    
    
    # mydb = mysql.connector.connect(
    # host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    # user = "admin",
    # password = "iGoByAdham$4*8",
    # database = "AdvisingSystem_ADS_3"  
    # )
    c = mydb.cursor(dictionary = True)
    ##use to retrieve basic information on user
    username = session['username']
    # print(username)

    ##COULD DO IF STATEMENT FOR SYS ADMIN THAT ALLOWS THEM VIEW ALL
    ##Check TYPE USER
    c.execute("SELECT * FROM users WHERE uname = %s LIMIT 1", (username,))
    results = 0
    syscheck = c.fetchone()


    if syscheck['role'] == 'system_admin' or syscheck['role'] == 'grad_secretary' or syscheck['role'] == 'cac':
        query = "%"+request.args.get("query")+"%"
        c.execute("SELECT * FROM users WHERE role = 'student' and (fname LIKE %s or lname LIKE %s)", (query, query))
        results = c.fetchall()
    else:
        c.execute("Select * from users INNER JOIN advises_on ON advises_on.student_id = users.uid where advises_on.fid = %s", (syscheck['uid'],))
        results = c.fetchall()


    if request.method == 'POST':
        if request.form.get('Button', default_value) == "Back to Home":
            return redirect('/info')
        if request.form.get('Button', default_value) == "Back to Student List":
            return render_template('faculty_studentList.html',name = username, results = results)
        
    if request.method == 'POST':
        default_value = 0
        data = request.form.get ("getStudent_Transcript" , default_value)
        if data == "Transcript":
            student = request.form.get('student_id2', default_value)
            # print(student)
            c.execute("Select fname from users where uname = %s", (student,))
            student_name = c.fetchone()
            c.execute("Select * from takes_course where studentid = %s", (student,))
            results = c.fetchall()
            if (results == [] or results == None):
               return render_template('student_Transcript.html',msg = "No Transcript on File", username = student_name,results = results) 
            c.close()
            return render_template('student_Transcript.html',msg = "", username = student_name,results = results)
        

        data2 = request.form.get ("programStudy" , default_value)
        if data2 == "Program Study":
            student = request.form.get('student_id', default_value)
            # print(student)
            c.execute("Select fname from users where uid = %s", (student,))
            student_name = c.fetchone()
            c.execute("Select * from program_study where univ_id = %s", (student,))
            results = c.fetchall()
            if (results == [] or results == None):
                return render_template('student_programstudy.html',msg = "No Program Study Found", username = student_name['fname'],results = results)
            c.close()
            return render_template('student_programstudy.html', msg = "", username = student_name['fname'],results = results)

    # print (results)
    return render_template('faculty_studentList.html',name = username, results = results)

@app.route("/assign_faculty_student", methods = ['GET','POST'])
def assign_faculty_student():

    
    if 'username' not in session:
        return redirect("/")


    default_value = 0
  
   
#     mydb = mysql.connector.connect(
#     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
#     user = "admin",
#     password = "iGoByAdham$4*8",
#     database = "AdvisingSystem_ADS_3"
# )


    
    c = mydb.cursor(dictionary = True, buffered = True)
    
    c.execute("Select * From advises_on")
    results = c.fetchall()
    if request.method == 'POST':

        if request.form.get('Button', default_value) == "Home":
            return redirect('/info')
       
        
        data = request.form.get ("Delete" , default_value)
        if data == "Delete":
            student = request.form.get('student_id', default_value)
            faculty = request.form.get('faculty_id',default_value)
            # print(student)
            c.execute("DELETE FROM advises_on WHERE fid = %s AND student_id = %s", (faculty, student,))
            mydb.commit()
            c.execute("Select * from advises_on")
            results = c.fetchall()
            c.close()

            return render_template('assign_faculty_student.html', results = results)
        

        faculty = request.form["faculty"]
        student = request.form["student"]
        # print ("faculty:", faculty)
        # print ("student:", student)
        c.execute( "Select * From users Where uid = %s",(student,))
        student_check = c.fetchall()
        # print("student_check:", student_check)
        if (student_check == [] or student_check == None):
            return render_template('assign_faculty_student.html', results = results,msg = "Invalid Insertion no student exists")
        


        c.execute("Select role From users where uid = %s", (faculty,))
        faculty_verify = c.fetchone()
        # print(faculty_verify)
        if (faculty_verify == [] or faculty_verify == None  or faculty_verify['role'] != "faculty"):
            return render_template('assign_faculty_student.html',results = results, msg = "Invalid Insertion no Faculty exist")
        
        c.execute("Select dname From advises_on WHERE fid = %s",(faculty,))
        department = c.fetchone()
        if (department == [] or department == None ):
            department = request.form["department"]
            if(department == ""):
                return render_template('assign_faculty_student.html',results = results, msg = "Enter a Department Name")
           


        c.execute("Select * From advises_on WHERE student_id = %s" , (student,))
        error_check = c.fetchall()
        if(error_check == [] or error_check == None):
            # print(department)
            c.execute("Select dname From advises_on WHERE fid = %s",(faculty,))
            department = c.fetchone()
            if (department == [] or department == None ):
                department = request.form["department"]
                if(department == ""):
                    return render_template('assign_faculty_student.html',results = results, msg = "Enter a Department Name")
                else:
                    c.execute("INSERT INTO advises_on (fid,dname,student_id) VALUES (%s,%s,%s)", (faculty,department,student,) )
                    mydb.commit()
            else:
                c.execute("INSERT INTO advises_on (fid,dname,student_id) VALUES (%s,%s,%s)", (faculty,department['dname'],student,) )
                mydb.commit()
           
            c.execute("Select * From advises_on")
            results = c.fetchall()
            c.close()
            return render_template('assign_faculty_student.html', results = results, msg = "")
        else: 
            return render_template('assign_faculty_student.html',results = results, msg = "Invalid Insertion student already assigned")
    return render_template('assign_faculty_student.html', results = results, msg = "")
            
       

@app.route("/review_grad_status", methods = ['GET', 'POST'])
def review_grad():

    if 'username' not in session:
        return redirect("/")

    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )
    

    c = mydb.cursor(dictionary = True)
    msg = ""

    if request.method == 'POST':
        if request.form['Button'] == "Back to Home":
            return redirect('/info')
        
        target = request.form.get('uid')
        print(target)
        # print(target)

        c.execute("UPDATE users SET is_alumni = 'yes' WHERE uid = %s", (target,))
        c.execute("UPDATE users SET grad_status = 'none' WHERE uid = %s", (target,))
        mydb.commit()

    
    ##First get applicable
    c.execute("SELECT uid, lname, fname, program FROM users where grad_status = 'sent' ORDER BY uid ASC")

    basic_info = c.fetchall()
    # print(basic_info)
    num_students = len(basic_info)
    for i in basic_info:
        username = i['uid'] 
        c.execute("SELECT * FROM takes_course where studentid = %s", (username,))
        program_curr = c.fetchall()
        i["program_study"] = program_curr
        # print(i["program_study"])

        c = mydb.cursor()
        c.execute("SELECT grade FROM takes_course where studentid = %s", (username,))
        grades = c.fetchall()
        num = round(gpa_calculator(grades), 2)
        i["gpa"] = num
        c = mydb.cursor(dictionary = True)

    

    c.close()

    if basic_info == '' or basic_info == None or len(basic_info) == 0:
        msg = "No Current Requests"


    return render_template('review_grad_status.html', msg = msg ,studentinfo = basic_info)

    



@app.route("/faculty_advisor", methods = ['GET', 'POST'])
def faculty_advisor():
    if 'username' not in session:
        return redirect("/")

    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )
    
    
    c = mydb.cursor(dictionary = True)
    username = session['username']
    if request.method == 'POST':
        c.execute("Select student_id from advises_on where fid = %s", (username,))
        results = c.fetchall()
        c.close()
        return render_template('faculty_studentList.html', username = username ,results = results)



@app.route("/student_programstudy", methods = ['GET', 'POST'])
def student_programstudy():

    if 'username' not in session:
            return redirect("/")

    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )
    

    c = mydb.cursor(dictionary = True)
    if request.method == 'POST':
                student = request.form["getStudent"]
                c.execute("Select * from program_study where univ_id = %s", (student,))
                results = c.fetchall()
                if(results == [] or results == None ):
                    return render_template('/student_programstudy', msg = "No Program Study on FILE ",results = results)
                c.close()
                return render_template('/student_programstudy',msg = "", results = results)



@app.route("/info", methods = ['GET', 'POST'])
def home():

   
    if 'username' not in session:    
        return redirect("/")

    ##Connect to database here
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )

    
    c = mydb.cursor(dictionary = True)

    ##use to retrieve basic information on user
    username = session['username']
    # print("user in session:", session['username'])

    ##select statement into database and check if email and password exist there
    c.execute("Select * from users where uname = %s", (username,))
    results = c.fetchone()
    # print("results", results)

    if results['role'] == 'student':
        c.execute("Select * from users where uname = %s", (username,))
        results = c.fetchone()
        # print(results)

        if results['program'] == None:
            return redirect(url_for('applicant'))
        elif results['is_alumni'] == 'yes':
            return render_template('alumni_student.html', results = results)
        return render_template('grad_student.html', results = results)

    if results['role'] == 'system_admin':
        c.execute("SELECT * FROM users WHERE uname != %s", (session['username'],))
        users = c.fetchall()
        c.close()
        if request.method == "POST":
            user_id = (str)(request.form['edit_user'])
            return redirect('/edit_user/'+user_id)
        return render_template('admin.html', users = users)
    
    if results['role'] == 'faculty':
        return render_template('faculty_advisor.html', results = results)
        
    if results['role'] == "grad_secretary":
        # print("grad secretary:", results)
        return render_template('grad_secretary.html', results = results)

    if results['role'] == "cac":
        # print("CAC:", results)
        return render_template('chair_of_admin.html', results = results)
    
    
    # print(results['uname'])
    # print(results['role'])

    ##Based on type user, render specific type of dashboard

    c.close()
    return render_template('login.html')

@app.route("/admininfo", methods = ['GET', 'POST'])
def admininfo():
    c = mydb.cursor(dictionary = True)
    query = "%"+request.args.get("query")+"%"
    c.execute("SELECT * FROM users WHERE uname != %s AND uname LIKE %s", (session['username'], query))
    users = c.fetchall()
    c.close()
    if request.method == "POST":
        user_id = (str)(request.form['edit_user'])
        return redirect('/edit_user/'+user_id)
    return render_template('admin.html', users = users)



@app.route("/form", methods = ['GET', 'POST'])
def form():
        
    if 'username' not in session:
            return redirect("/")

    ##Connect to database here
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )

    
    c = mydb.cursor(dictionary = True, buffered = True)

    ##use to retrieve basic information on user
    username = session['username']

    c.execute("SELECT univ_id FROM program_study WHERE univ_id = %s", (session['id'],))
    forms = c.fetchall()
    if forms != []:
        return render_template('return_template.html')
        

    c.execute("Select * from program_study where univ_id = %s", (username,))
    checkinsert = c.fetchall()
    # print(checkinsert)
    if request.method == 'POST':
        
        if request.form['Button'] == "b":
            return redirect('/info')
    
    if checkinsert != []:
        return render_template('return_template.html')


    ##select statement into database and check if email and password exist there
    c.execute("Select * from users where uname = %s", (username,))
    results = c.fetchone()

    if request.method == 'POST':
        
        if request.form['Button'] == "b":
            return redirect('/info')
        
            
        ## check and insert into database
        
        ##to count how many fields are not blank at least 10 are required
        count = 10
        
        ##used to count the amount of CS courses being taken
        count_cs = 0
        
        input1dep = request.form['input1dep']
        if input1dep == "CSCI":
            count_cs+=1
        input1crn = request.form['input1crn'] 
        input2dep = request.form['input2dep']
        if input2dep == "CSCI":
            count_cs+=1
        input2crn = request.form['input2crn']
        input3dep = request.form['input3dep']
        if input3dep == "CSCI":
            count_cs+=1
        input3crn = request.form['input3crn']
        input4dep = request.form['input4dep']
        if input4dep == "CSCI":
            count_cs+=1
        input4crn = request.form['input4crn']
        input5dep = request.form['input5dep']
        if input5dep == "CSCI":
            count_cs+=1
        input5crn = request.form['input5crn']
        input6dep = request.form['input6dep']
        if input6dep == "CSCI":
            count_cs+=1
        input6crn = request.form['input6crn']
        input7dep = request.form['input7dep']
        if input7dep == "CSCI":
            count_cs+=1 
        input7crn = request.form['input7crn']
        input8dep = request.form['input8dep']
        if input8dep == "CSCI":
            count_cs+=1
        input8crn = request.form['input8crn']
        input9dep = request.form['input9dep']
        if input9dep == "CSCI":
            count_cs+=1
        input9crn = request.form['input9crn']
        input10dep = request.form['input10dep']
        input10crn = request.form['input10crn']
        input11dep = request.form['input11dep']
        input11crn = request.form['input11crn']
        if input11crn != "":
            count+=1
        input12dep = request.form['input12dep']
        input12crn = request.form['input12crn']
        # print(input12crn)
        if input12crn != "":
            count+=1

        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input1crn, input1dep,))
        input1_id = c.fetchone()
       
        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input2crn, input2dep,))
        input2_id = c.fetchone()
        
        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input3crn, input3dep,))
        input3_id = c.fetchone()
        
        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input4crn, input4dep,))
        input4_id = c.fetchone()
        
        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input5crn, input5dep,))        
        input5_id = c.fetchone()

        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input6crn, input6dep,))
        input6_id = c.fetchone()

        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input7crn, input7dep,))
        input7_id = c.fetchone()
        
        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input8crn, input8dep,))     
        input8_id = c.fetchone()
        
        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input9crn, input9dep,))
        input9_id = c.fetchone()

        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input10crn, input10dep,))
        input10_id = c.fetchone()
        # print(input10_id)

        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input11crn, input11dep,)) 
        input11_id = c.fetchone()
        ##Not used
        if input11_id == None:
            input11_id = dict()
            input11_id['courseid'] = '00'
        
        c.execute("SELECT courseid FROM course WHERE cnum = %s and dept = %s LIMIT 1", (input12crn, input12dep,))
        input12_id = c.fetchone()
        ##Not used
        if input12_id == None:
            input12_id = dict()
            input12_id['courseid'] = '00'


        ##error check form
        ##using tuples
        c = mydb.cursor(dictionary = True)
        
        c.execute("SELECT * FROM course where courseid in (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (input1_id['courseid'], input2_id['courseid'], input3_id['courseid'], input4_id['courseid'], input5_id['courseid'], input6_id['courseid'], input7_id['courseid'], input8_id['courseid'], input9_id['courseid'], input10_id['courseid'], input11_id['courseid'], input12_id['courseid']))
        
        ##list of dictionaries
        checklist = c.fetchall()
        # print(checklist)
        # print(count)

        ##error checks
        ##Check for invalid course nmbs entered
        if  checklist == [] or len(checklist) != count:
            msg = "Error, one or more invalid courses entered or multiples entered, try again"
            return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
        
        ##Check for course credits
        count_cred = 0
        for i in checklist:
            count_cred += i['credits']
        
        ##course credits required based on what program the grad student is taking
        c = mydb.cursor()
        c.execute("Select program from users where uname = %s", (username,))
        enrollcheck = c.fetchone()
        # print(enrollcheck)

        if enrollcheck[0] == "PHD":
            c.execute("SELECT mincredit FROM requirements where degree_type = %s", (enrollcheck[0],))
            minPHD = c.fetchone()
            if count_cred<minPHD[0]:
                msg = "Error, not enough credits, need at least 36 for PHD"
                return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
            
            ##parse and check at least 30 credits in CS
            ##count cs credits
            countcs_cred = 0
            for i in checklist:
                if i['dept'] == 'CSCI':
                    countcs_cred+=i['credits']
            if countcs_cred<30:
                msg = "Error, not enough CS credits, need 30 credits"
                return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
            # print("success")
            ##For insertion of each course into program study 
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input1dep, input1crn, input1_id['courseid']))
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input2dep, input2crn, input2_id['courseid']))
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input3dep, input3crn, input3_id['courseid']))            
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input4dep, input4crn, input4_id['courseid']))            
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input5dep, input5crn, input5_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input6dep, input6crn, input6_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input7dep, input7crn, input7_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input8dep, input8crn, input8_id['courseid']))
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input9dep, input9crn, input9_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input10dep, input10crn, input10_id['courseid']))

            if input11crn != "":
                c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input11dep, input11crn, input11_id['courseid']))

            if input12crn != "":
                c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input12dep, input12crn, input12_id['courseid']))
            mydb.commit()
            msg = "Success!"
            return render_template('return_template.html')
        else:
            c.execute("SELECT mincredit FROM requirements where degree_type = %s", (enrollcheck[0],))
            minMS = c.fetchone()
            if count_cred<minMS[0]:
                msg = "Error, not enough credits, need at least 30 for MS"
                return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
               
            ##Check if courses CSCI 6212 CSCI 6221 CSCI 6461 included, and check how many non CS courses
            non_cs = 0
            count_core = 0 
            c.execute("SELECT * FROM reqMScourses")
            req = c.fetchall()
            for i in checklist:
                # print(i['course_num'])
                # print(i['dept'])
                # print(req)
                ##if i['course_id'] == req[0][0] or i['course_id'] == req[1][0] or i['course_id'] == [2][0]:
                if i['courseid'] == '03' or i['courseid'] == '01' or i['courseid'] == '02':
                    count_core+=1
                if i['dept'] != 'CSCI':
                    non_cs+=1
            if count_core != 3:
                # print(count_core)
                msg = "Error, 3 core classes CSCI 6212 CSCI 6221 CSCI 6461 must be included"
                return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
            
            if non_cs > 2:
                msg = "Error, at most 2 non-CS course, try again"
                return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
            # print("success")
            ##For insertion of each course into program study 
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input1dep, input1crn, input1_id['courseid']))
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input2dep, input2crn, input2_id['courseid']))
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input3dep, input3crn, input3_id['courseid']))            
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input4dep, input4crn, input4_id['courseid']))            
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input5dep, input5crn, input5_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input6dep, input6crn, input6_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input7dep, input7crn, input7_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input8dep, input8crn, input8_id['courseid']))
            
            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input9dep, input9crn, input9_id['courseid']))

            c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input10dep, input10crn, input10_id['courseid']))

            if input11crn != "":
                c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input11dep, input11crn, input11_id['courseid']))

            if input12crn != "":
                c.execute("INSERT INTO program_study VALUES (%s, %s, %s, %s, %s, %s)", (results['uid'], results['lname'], results['fname'], input12dep, input12crn, input12_id['courseid']))
            mydb.commit()
            msg = "Success!"
            return render_template('return_template.html')



    c.close()
    msg = ''
    # print("here:",results)
    return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)



@app.route("/transcript", methods = ['GET', 'POST'])
def transcript():

    if 'username' not in session:
        return redirect("/")   

    ##Connect to database here
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )
    
    username = session['username']
    c = mydb.cursor(dictionary = True)
    c.execute("SELECT * FROM users WHERE uname = %s", (username,))
    id = c.fetchone()
    # print("id:", id)
    c = mydb.cursor()
    c.execute("SELECT grade FROM takes_course where studentid = %s", (id['uid'],))
    grades = c.fetchall()
    # print(grades)
    if grades != None:
        num = round(gpa_calculator(grades), 2)
    c = mydb.cursor(dictionary = True)
    c.execute("SELECT * FROM takes_course INNER JOIN course ON course.courseid = takes_course.courseid HAVING studentid = %s ORDER BY year_taken, semester", (id['uid'],))
    program_curr = c.fetchall()
    c.execute("SELECT program FROM users where uname = %s",(username,))
    typedegree = c.fetchone()
    # print(typedegree)
    # print(program_curr)

    msg =""
    
    if typedegree['program'] == "PHD":
        c.execute("SELECT minGPA FROM requirements where degree_type = 'PHD'")
        min = c.fetchone()
        if num<min['minGPA']:
            msg = "Minimum GPA not met seek advisor"

        # check to seee that they have taken 30 credit hours in cs
        # 36 credits total
        c.execute("SELECT * FROM takes_course INNER JOIN course ON course.courseid = takes_course.courseid HAVING studentid = %s", (id['uid'],))
        req = c.fetchall()
        # print("REQ: ", req)

        total_credits = 0
        
        for i in req:
            total_credits += i['credits']
        if total_credits < 36:
            msg = "Not enough credits to graduate"
        
        cs_credit = 0
        for i in req:
            if i['dept'] == "CSCI":
                cs_credit += i['credits']
        if cs_credit < 30:
            msg = "Not enough cs credits hours to graduate"

        

        count = 0
        for i in grades:
            for j in i:
                if j == "B-" or j == "C+" or j =="C" or j == "C-" or j == "D+" or j =="D" or j == "F":
                    count+=1
        if count>1:
            if msg != "":
                msg = msg + " and more than one grade below a B"
            else:
                msg = "More than one grade below a B"

        c = mydb.cursor(dictionary = True)
        c.execute("SELECT thesis_status FROM users where uname = %s LIMIT 1", (username,))
        statusthesis = c.fetchone()
        # print(statusthesis)
        if statusthesis['thesis_status'] != "complete":
            if msg != "":
                msg = msg + " and thesis not passed"
            else:
                msg = "Thesis not passed"
        
    else:
        # check if they have taken the core classes
        # check if their total credits is greater than 30
        c.execute("SELECT minGPA FROM requirements where degree_type = 'MS'")
        min = c.fetchone()
        if num<min['minGPA']:
            msg = "Minimum GPA not met seek advisor"
        
        c.execute("SELECT * FROM takes_course INNER JOIN course ON course.courseid = takes_course.courseid HAVING studentid = %s", (id['uid'],))
        req = c.fetchall()
        
        count_core = 0
        for i in req:
            if i['courseid'] == '03' or i['courseid'] == '01' or i['courseid'] == '02':
                count_core += 1
        if count_core != 3:
            msg = "Don't have the required classes for CS"
        
        total_credits = 0  
        for i in req:
            total_credits += i['credits']
        print(total_credits)
        if total_credits < 30:
            msg = "Not enough credits to graduate"

        count = 0
        for i in grades:
            for j in i:
                if j == "B-" or j == "C+" or j =="C" or j == "C-" or j == "D+" or j =="D" or j == "F":
                    count+=1
        if count > 2:
            if msg != "":
                msg = msg + " and more than one grade below a B"
            else:
                msg = "More than one grade below a B"

        other_classes = 0
        for i in req:
            if i['dept'] == 'ECE' or i['dept'] == 'MATH':
                other_classes += 1
        if other_classes > 2:
            msg = "Took too many classes outside of CS"


    ##If apply button was clicked
    if request.method == 'POST':
        if request.form['Button'] == "Submit for Graduation":
            msg = "Sucess, your application will be reviewed by a GS"
            status = "sent"
            print(status + " " + username)
            c.execute("UPDATE users SET grad_status = (%s) WHERE uname = (%s)", (status, username, ))
            mydb.commit()
        else:
            c.close()
            return redirect('/info')

    c.execute("Select is_alumni FROM users where uname = (%s)", (username,))
    result = c.fetchone()


    ##check requirements based on program
    c.close()
    return render_template('transcript.html', gpa = num, proglist = program_curr, err = msg, result = result)


def gpa_calculator(grades):
    points = 0
    i = 0
    grade_c = {"A":4,"A-":3.67,"B+":3.33,"B":3.0,"B-":2.67, "C+":2.33,"C":2.0,"C-":1.67,"D+":1.33,"D":1.0,"F":0}
    if grades != []:
        completedGrades = 0
        for i in grades:
            for j in i:
                if j != 'IP':
                    points += grade_c[j]
                    completedGrades = completedGrades + 1
        if completedGrades == 0:
            return 0.0
        else:
            gpa = points / completedGrades
            return gpa
    else:
        return 0.0
 
 

@app.route("/update_info", methods = ['GET', 'POST'])
def update_info():
    
    if 'username' not in session:
        return redirect("/")


    ##Connect to database here
    c = mydb.cursor(dictionary = True)


    username = session['username']
    c.execute("Select * FROM users WHERE uname =(%s)",(username,))
    result = c.fetchone()
    # print(result)

    if request.method == 'POST':
        if request.form['Button'] == "Confirm":
            msg = "Succesfully Updated"
            uname = request.form['uname']
            address = request.form['address']
            fname = request.form['fname']
            lname = request.form['lname']
            password = request.form['password']
            # print(password)
            uname = request.form['uname']
            ss_num = request.form['ss_num']
            email = request.form['email']
            username = session['username']
            c.execute("SELECT email, uname, password, ss_num FROM users")
            userinfo = c.fetchall()
            for info in userinfo:
                if info['uname'] == uname and uname != result['uname']:
                    return render_template('update_info.html', result = result, errormsg = "Username already in use")
                elif info['email'] == email and email != result['email']:
                    return render_template('update_info.html', result = result, errormsg = "Email already in use")
                elif info['password'] == password and password != result['password']:
                    return render_template('update_info.html', result = result, errormsg = "Password already in use")
                elif info['ss_num'] == ss_num and ss_num != result['ss_num']:
                    return render_template('update_info.html', result = result, errormsg = "SSN already in use")
            c.execute("UPDATE users SET uname = %s, fname = %s, lname = %s, password = %s, address = %s, ss_num = %s, email = %s where uname = (%s)", (uname, fname, lname, password, address, ss_num, email, username,))
            mydb.commit()
            session['username'] = uname
            return redirect('/info')
        else:
            c.close()
            return redirect('/info')
    return render_template('update_info.html', result = result, errormsg = "")


@app.route("/create_user", methods = ['GET', 'POST'])
def create_user():
    ##Connect to database here
    c = mydb.cursor()
    
    if 'username' not in session:
        if request.method == 'POST':
            if request.form['Button'] == "Home":
                return redirect('/')
        check = "check"
        c = mydb.cursor()
        if request.method == 'POST':
            if request.form['Button'] == "Submit":
                uname = request.form['uname']
                session['create_userID'] = uname
                password = request.form['password']
                # name = request.form['name']
                role = request.form['role']
                # print(role)
                # print(type(role))
                c.execute("SELECT * FROM users WHERE uname = %s", (uname,))
                error_checking = c.fetchall()
                if(error_checking == [] or error_checking == None):
                    session['username'] = uname
                    session['password'] = password
                    session['role'] = role
                    if role == "student" or role == 'student':
                        session['check'] = 'check'
                        return redirect('/enter_info')
                else:
                    return render_template('create_user.html', msg = "Invalid User ID", check = check)
            
        return render_template('create_user.html', msg = "", check = check)
    c = mydb.cursor()
    if request.method == 'POST':
        if request.form['Button'] == "Submit":
            uname = request.form['uname']
            session['create_userID'] = uname
            password = request.form['password']
            # name = request.form['name']
            role = request.form['role']
            c.execute("SELECT * FROM users WHERE uname = %s", (uname,))
            error_checking = c.fetchall()
            if(error_checking == [] or error_checking == None):
                session['username'] = uname
                session['password'] = password
                session['role'] = role
                # c.execute("INSERT INTO users(uname,password,role) VALUES (%s, %s, %s)", (uname,password,role,))
                # mydb.commit()
                if role == "student"or role == "faculty" or role == 'faculty' or role == "grad_secratary" or role == 'grad_secretay' or role == "systems_admin" or role == 'system_admin' or role == 'cac':
                    return redirect('/enter_info')
            else:
                return render_template('create_user.html', msg = "Invalid User ID")
        else:
            c.close()
            return redirect('/info')
    return render_template('create_user.html')

@app.route("/enter_info", methods = ['GET', 'POST'])
def enter_info():
    if 'username' not in session and 'check' not in session:
        return redirect("/")
    ##Connect to database here
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )
    c = mydb.cursor()

    if request.method == 'POST':
        if request.form['Button'] == "Submit":
            uid = session['create_userID']
            fname = request.form['fname']
            lname = request.form['lname']
            # program = request.form['program']
            address = request.form['address']
            ssn = request.form['ssn']
            email = request.form['email']
            c.execute("SELECT * from users where uid = %s ", (uid,))
            error_check = c.fetchall()
            if(error_check == [] or error_check == None):
                c.execute("INSERT INTO users(uname, fname, lname, email, password, address, ss_num, role, is_alumni) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'no')", (session['username'], fname, lname, email, session['password'], address, ssn, session['role'],))
                mydb.commit()
                session.pop('check', None)
                return redirect('/info')
            else: 
                return render_template('enter_info.html',msg = "duplicate entry")
        else:
            c.close()
            session.pop('check', None)
            return redirect('/info')
    return render_template('enter_info.html', msg = "")

@app.route("/enter_PHDinfo", methods = ['GET', 'POST'])
def enterPHD():
    if 'username' not in session:
        return redirect("/")
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )

    c = mydb.cursor()
    username = session['username']    
    msg = ''
    if request.method == 'POST':
        if request.form['Button'] == "Submit":
            text = request.form['field']
            c.execute("UPDATE users SET thesis = (%s) where uname = (%s)", (text, username))
            c.execute("UPDATE users SET thesis_status = (%s) where uname = (%s)", ("pending", username))
            mydb.commit()
            msg = 'Successfully Updated'
        else:
            return redirect('/info')



    return render_template('enterPHD.html', msg = msg)

@app.route("/view_thesis", methods = ['GET', 'POST'])
def view_thesis():
    if 'username' not in session:
        return redirect("/")
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )

    c = mydb.cursor(dictionary = True)


    if request.method == 'POST':
        if request.form['Button'] == "Back to Home":
            return redirect("/info")
        target = request.form.get('uid')
        # print(target)

        c.execute("UPDATE users SET thesis_status = (%s) where uid = (%s)", ("complete", target))
        mydb.commit()
    
    username = session['username']
    # print(username)
    c.execute("SELECT uid FROM users WHERE uname = %s", (username,))
    username = c.fetchone()
    c.execute("Select * FROM users INNER JOIN advises_on ON advises_on.student_id = users.uid WHERE (thesis_status = %s AND fid = %s)", ("pending",username['uid'],))
    allthesis = c.fetchall()
    # print(allthesis)

    return render_template('approvethesis.html', info = allthesis)

### //////////////////////////////////////////////////////////////////////////////////////////////////// ###
### This function gets basic info about the logged in user by checking the session ###
def loginInfo():
  #connect to database
  cursor = mydb.cursor(dictionary=True)

  if 'username' not in session:
    uid = ''
    fname = ''
    lname = ''
  else:
    cursor.execute("SELECT uid, fname, lname FROM users WHERE uname ='" + session['username'] + "'")
    user = cursor.fetchone()
    uid = user.get('uid')
    fname = user.get('fname')
    lname = user.get('lname')

  return (uid, fname, lname)

### Function that displays the home page and collects all items in the 'product' table ###
@app.route('/applicant', methods=['GET', 'POST'])
def applicant():
  if 'username' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    uid, fname, lname = loginInfo()

    refEmail = ''

    refExists = recLetterCheck()
    # print("refExists: ", refExists)
    if refExists:
      cursor.execute("SELECT ref_email FROM reference WHERE id=" + str(uid))
      reference = cursor.fetchone()
      refEmail = reference.get('ref_email')
    #   print("refEmail: ", refEmail)
    
    cursor.execute("SELECT app_status FROM application WHERE id = %s" , (uid,))
    form = cursor.fetchone()

    username = session['username']
    cursor.execute("Select * from users where uname = %s", (username,))
    results = cursor.fetchone()
    
    if form:
      app_status = form.get('app_status')
      formsExist = True
    else:
      formsExist = False

    if results['program'] != None:
        admitted = True
    else:
        admitted = False
      
    if formsExist and refEmail:
      return render_template('applicant.html', uid = uid, fname = fname, status = app_status, formsExist = formsExist, refEmail = refEmail, results = results, admitted = admitted)
    elif formsExist:
      return render_template('applicant.html', uid = uid, fname = fname, status = app_status, formsExist = formsExist, results = results, admitted = admitted)
    else:
      return render_template('applicant.html', fname = fname, formsExist = formsExist, results = results, admitted = admitted)

### Function for the application page ###
@app.route('/application', methods=['GET', 'POST'])
def application():
  # connect to database
  cursor = mydb.cursor(dictionary=True)
  
  if request.method == 'POST':
    #Type of degree they want to apply for
    typeDeg = request.form["choice"]

    #Previous degrees
    priorDeg1 = request.form["priorDeg1"]
    priorDeg1Major = request.form["priorDeg1Major"]
    priorDeg1Year = request.form["priorDeg1Year"]
    priorDeg1GPA = request.form["priorDeg1GPA"]
    priorDeg1Uni = request.form["priorDeg1Uni"]
    priorDeg2 = request.form["priorDeg2"]
    priorDeg2Major = request.form["priorDeg1Major"]
    priorDeg2Year = request.form["priorDeg2Year"]
    priorDeg2GPA = request.form["priorDeg2GPA"]
    priorDeg2Uni = request.form["priorDeg2Uni"]
    
    # Area of interest
    interestIn = request.form["interestIn"]
    
    #GRE information
    greVerbal = request.form["greVerbal"]
    greQuant = request.form["greQuant"]
    greYear = request.form["greYear"]
    greAdvSub = request.form["greAdvSub"]
    greAdvScore = request.form["greAdvScore"]
  
    #TOEFL information
    tflScore = request.form["tflScore"]
    tflDate = request.form["tflDate"]

    # Previous experience
    experience = request.form["experience"]
    
    # Start Date 
    adminSem = request.form["adminSem"]
    adminYear = request.form["adminYear"]
    adminDate = adminSem + ' ' + adminYear
    
    # Recommedations
    reference1Fname = request.form["reference1Fname"]
    reference1Lname = request.form["reference1Lname"]
    reference1Email = request.form["reference1Email"]
    reference1Title = request.form["reference1Title"]
    reference1Affil = request.form["reference1Affil"]

    # reference2Fname = request.form["reference2Fname"]
    # reference2Lname = request.form["reference2Lname"]
    # reference2Email = request.form["reference2Email"]
    # reference2Title = request.form["reference2Title"]
    # reference2Affil = request.form["reference2Affil"]
    
    today = date.today()
# 
    current_date = today.strftime("%d/%m/%Y")
    # print("time of application", current_date)


    cursor.execute("SELECT uid, lname, fname FROM users WHERE uname ='" + session['username'] + "'")
    user= cursor.fetchone()
    uid = user.get("uid")
    fname = user.get("fname")
    lname = user.get("lname")
    complete = 1

    try:
      cursor.execute("INSERT INTO application (id, lname, fname, app_degree, semester, area_interest, experience, complete, gre_verbal, gre_quant, gre_year, gre_adv_sub, gre_adv_score, toefl_score, toefl_year, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(uid, lname, fname, typeDeg, adminDate, interestIn, experience, complete, greVerbal, greQuant, greYear, greAdvSub, greAdvScore, tflScore, tflDate, current_date))
      cursor.execute("INSERT INTO degree (uid, degree_name, gpa, major, degree_year, university) VALUES (%s,%s,%s,%s,%s,%s)",(uid, priorDeg1, priorDeg1GPA, priorDeg1Major, priorDeg1Year, priorDeg1Uni))
      cursor.execute("INSERT INTO reference (id, ref_fname, ref_lname, ref_email, title, affiliation) VALUES (%s,%s,%s,%s,%s,%s)", (uid, reference1Fname, reference1Lname, reference1Email, reference1Title, reference1Affil))
      

      if priorDeg2 is not None:
        cursor.execute("INSERT INTO degree (uid, degree_name, gpa, major, degree_year, university) VALUES (%s,%s,%s,%s,%s,%s)",(uid, priorDeg2, priorDeg2GPA, priorDeg2Major, priorDeg2Year, priorDeg2Uni))
    
      mydb.commit()
      # print('New application!')
      msg = 'Applied Succesfully'
      return redirect(url_for('applicant'))
    except:
      mydb.rollback()
      # print("error occured")
      errmsg = 'An unexpected error occured, please try again'
      return render_template('application.html', errmsg = errmsg)
  return render_template('application.html')


@app.route('/recLetter', methods=['GET', 'POST'])
def recLetter():
  # connect to database
  cursor = mydb.cursor(dictionary=True, buffered=True)
  refEmail = request.args.get("refEmail")
#   print("refEmail in recLetter: ", refEmail)

  if request.method == 'POST':
    letter = request.form['letter']
    
    cursor.execute("SELECT ref_fname, ref_lname FROM reference WHERE ref_email ='" + refEmail + "'")
    reference = cursor.fetchone()
    uid, fname, lname = loginInfo()
    ref_fname = reference.get("ref_fname")
    ref_lname = reference.get("ref_lname")
    refName = ref_fname + ' ' + ref_lname

    cursor.execute("SELECT complete FROM application WHERE id = %s", (uid,) )
    complete = cursor.fetchone()
    total = complete.get('complete') + 1

    try:
      cursor.execute("INSERT INTO letter (id, name, message) VALUES (%s,%s,%s)", (uid, refName, letter))
      mydb.commit()
      # print('Recommendation letter recieved!')
      try:
        cursor.execute("UPDATE application SET complete=%s WHERE id = %s", (total, uid))
        mydb.commit()
      except:
        mydb.rollback()
      
      msg = "Reccomendation letter successfully submitted"
      return redirect(url_for('applicant'))
    except:
      mydb.rollback()
      # print('error occured')
      msg = "An unexpected error occured, please try again"
      return render_template('letter.html', msg = msg)
  return render_template('letter.html', refEmail = refEmail)

### Function that checks if recommendation letter needs to be filled ###
def recLetterCheck():
  #connect to database
  cursor = mydb.cursor(dictionary=True)
  
  # mySQL query to find uid of user in session
  cursor.execute("SELECT uid FROM users WHERE uname='" + session['username'] + "'")
  userID = cursor.fetchone()
  uid = userID.get("uid")

  # MySQL query to find the email of the reference
  cursor.execute("SELECT ref_email FROM reference WHERE id=" + str(uid))
  reference = cursor.fetchone()
  
  # if no reference, return False (There are no recommenders linked to this user)
  if not reference:
    return False
  # There is a reference, check if letter exists
  else:
    # MySQL query to find the message from the reference
    cursor.execute("SELECT message FROM letter WHERE id=" + str(uid))
    message = cursor.fetchone()

    # If no message, return True (There is a recommender, but a letter needs to be filled) 
    if not message:
      return True
    # There exists a letter, return False
    else:
      return False

### Function for the page the GS can see ###
@app.route('/gs', methods=['GET', 'POST'])
def gs():
  if 'username' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    loggedIn, fname, lname = loginInfo()

    try:
      cursor.execute("SELECT * FROM application ORDER BY date DESC")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False
    
    if formsExist:
      return render_template('gs.html', fname = fname, forms = forms, formsExist = formsExist )
    else:
      return render_template('gs.html', fname = fname, formsExist = formsExist )      
  redirect(url_for('logout'))

### Function for the page the GS can see ###
@app.route('/cac', methods=['GET', 'POST'])
def cac():
  if 'username' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    loggedIn, fname, lname = loginInfo()

    session['fname'] = fname

    try:
      cursor.execute("SELECT * FROM application ORDER BY date DESC")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False

    if formsExist:
      return render_template('cac.html', fname = fname, forms = forms, formsExist = formsExist )
    else:
      return render_template('cac.html', fname = fname, formsExist = formsExist )      
  redirect(url_for('logout'))



### Function for the page the reviewer can see ###
@app.route('/reviewer', methods=['GET', 'POST'])
def reviewer():
  if 'username' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    # fname to display
    cursor.execute("SELECT fname FROM users WHERE uname=%s", (session['username'],) )
    fname = cursor.fetchone()
    
    session['fname'] = fname.get('fname')

    try:
      # complete = 3 means: recieved application, recieved rec letter, and 
      # recieved transcript
      cursor.execute("SELECT * FROM application WHERE complete = '3'")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False

    if formsExist:
      return render_template('reviewer.html', name = fname.get('fname'), forms = forms, formsExist = formsExist )
    else:
      return render_template('reviewer.html', name = fname.get('fname'), formsExist = formsExist )      
  else:
    redirect(url_for('logout'))


@app.route('/review_application/<id>', methods=['GET', 'POST'])
def review(id):
  if 'username' in session:

    cursor = mydb.cursor(dictionary=True)
    
    # get role
    cursor.execute("SELECT role FROM users WHERE uname ='" + session['username'] + "'")
    role = cursor.fetchone()

    # get all info from took
    # print("ID of applicant that GS is reviewing:", id)
    cursor.execute("SELECT * FROM application WHERE id = '" + id +"'")
    application = cursor.fetchall()
    # print("Application of this applicant:", application)


    for i in application:
        completed = i.get('complete')
        status = i.get('app_status')
        admitted = False
        appcompleted = False
        if completed >= 3:
            appcompleted = True 
        if status == 'admit':
            admitted = True
    # print("complete variable:", completed)
    
    # print("admitted variable", admitted)
    
    # get all from degree
    cursor.execute("SELECT * FROM degree WHERE uid = '" + id +"'")
    degree = cursor.fetchall()
    
    if role.get('role') == 'grad_secretary':                                     
      return render_template('review_gs.html', application = application, 
                           degree = degree, role = role, appcompleted = appcompleted, admitted = admitted)
    if role.get('role') == 'cac':                                     
      return render_template('review_cac.html', application = application, 
                           degree = degree, role = role, appcompleted = appcompleted, admitted = admitted)

    return render_template('review.html', application = application, 
                           degree = degree, role = role, appcompleted = appcompleted, admitted = admitted)
  return redirect(url_for('logout'))
    




@app.route('/submit_review/<id>', methods=['GET', 'POST'])
def submit_review(id):
  if 'username' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname, lname = loginInfo()

    # # get role
    cursor.execute("SELECT role FROM users WHERE uname ='" + session['username'] + "'")
    role = cursor.fetchone()   

    try:
      cursor.execute("SELECT * FROM application")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False

    try:
      cursor.execute("SELECT * FROM application WHERE complete ='3'")
      rev_forms = cursor.fetchall()
      rev = True
    except:
      rev = False

    try:
      # Get form data
      rating = request.form["rating"]
      generic = request.form["generic"]
      credible = request.form["credible"]
      where_from = request.form["from"]
      gas_rating = request.form["gas_rating"]
      def_course = request.form["def_course"]
      reject = request.form["reject"]
      gas_comment = request.form["gas_comment"]
      advisor = request.form["advisor"]
      
      cursor.execute("SELECT complete FROM application WHERE id = %s", (id,) )
      complete = cursor.fetchone()
      total = complete.get('complete') + 1
      
      
      cursor.execute("INSERT INTO letter_review (id, rating, generic, credible, university) VALUES (%s,%s,%s,%s,%s)", ( id, rating, generic, credible, where_from))      
      cursor.execute("INSERT INTO gas_rating (id, review_rating, deficiency_course, reason_reject, gas_comment, advisor) VALUES (%s,%s,%s,%s,%s,%s)", ( id, gas_rating, def_course, reject, gas_comment, advisor))      
      cursor.execute("UPDATE application SET complete=%s WHERE id = %s", (total, id))
      mess = 'Sucessfully Added Review.'
      # return render_template('review.html', id, mess = mess)
      # return redirect(url_for('review'), id = id, mes = mess)
      fname = session['fname']
      mydb.commit()

      if role.get('role') == 'cac':                                     
        return render_template('cac.html', mess = mess, name = fname, forms = forms, formsExist = formsExist)

      return render_template('reviewer.html', mess = mess, name = fname, forms = rev_forms, formsExist = rev)
    except:
      mydb.rollback()
      mess = 'Error With Adding Review. Please Try again.'
      # return render_template('review.html', mess = mess)
      if role.get('role') == 'cac':                                     
        return render_template('cac.html', mess = mess, name = fname, forms = forms, formsExist = formsExist)
      return render_template('reviewer.html', mess = mess, name = fname, forms = rev_forms, formsExist = rev)

  redirect(url_for('logout'))
  
@app.route('/update_application_transcript/<id>', methods=['GET', 'POST'])
def update_application_transcript(id):
  if 'username' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname, lname = loginInfo()

    try:
      cursor.execute("SELECT * FROM application")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False
  

    transcript_status = request.form["transcript_status"]
    

  if transcript_status == "received":    
      cursor.execute("SELECT complete FROM application WHERE id = %s", (id,) )
      complete = cursor.fetchone()
      total = complete.get('complete') + 1
      cursor.execute("UPDATE application SET complete=%s WHERE id = %s", (total, id))

      mydb.commit()  
     
      mess = 'Sucessfully Marked Transcript As Received, Do NOT Mark as Received Again'
      return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
  else:
      mydb.rollback()
      
      mess = 'Transcripts not yet Received'
      return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)


@app.route('/update_application_admission/<id>', methods=['GET', 'POST'])
def update_application_CAC(id):
  if 'username' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname, lname = loginInfo()


   
    try:
      cursor.execute("SELECT * FROM application")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False
  

    admission_status = request.form["admission_status"]
    # print(admission_status)
    

  if admission_status == "admit":    
      admit_final = "admit"

      cursor.execute("SELECT app_degree FROM application WHERE id = %s", (id,))
      deg = cursor.fetchone()
      typeDeg = deg.get('app_degree')
    #   print("typeDeg of this student: ", typeDeg)

      try:
        cursor.execute("UPDATE users SET program = %s WHERE uid = %s", (typeDeg, id))
        cursor.execute("UPDATE application SET app_status=%s WHERE id = %s", (admit_final, id))
        mydb.commit()  
        mess = 'Sucessfully Marked Application as an Admit Application'
        return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
      except:
        mydb.rollback()
        mess = 'An unexpected error occured, please try again'
        return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
  elif admission_status == "deny":
      admit_final = "deny"

      try:
        cursor.execute("UPDATE application SET app_status=%s WHERE id = %s", (admit_final, id))
        mydb.commit()  
        mess = 'Sucessfully Marked Application as a Deny Application'
        return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
      except:
        mydb.rollback()
        mess = 'An unexpected error occured, please try again'
        return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
  else:
      mydb.rollback()
      
      mess = 'Did not Mark Application as Admit or Deny'
      return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)


@app.route('/update_application_admission_cac/<id>', methods=['GET', 'POST'])
def submit_review_cac(id):
 if 'username' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname, lname = loginInfo()

    try:
      cursor.execute("SELECT * FROM application")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False
  
    admission_status = request.form["admission_status"]
    # print(admission_status)
    

    if admission_status == "admit":    
      admit_final = "admit"
      cursor.execute("UPDATE application SET app_status=%s WHERE id = %s", (admit_final, id))
      mydb.commit()  
     
      mess = 'Sucessfully Marked Application as an Admit Application'
      return render_template('cac.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
    elif admission_status == "deny":
      admit_final = "deny"
      cursor.execute("UPDATE application SET app_status=%s WHERE id = %s", (admit_final, id))
      mydb.commit()  
     
      mess = 'Sucessfully Marked Application as a Deny Application'
      return render_template('cac.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
    else:
      mydb.rollback()
      
      mess = 'Did not Mark Application as Admit or Deny'
      return render_template('cac.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)

### ////////////////////////////////////////////////////////////////////////////////////// ###

@app.route('/register')
def register():
    # This makes the assumption that the courses in 'courses_offered'
    # are for the semester a student can currently register for.

    # set up cursor/DB connection
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute(
        "SELECT * FROM course_offered JOIN course ON course.courseid = course_offered.courseid")
    courses = cursor.fetchall()
    # show courses that are being offered
    return render_template("register.html", courses=courses)

@app.route('/register/<cid>', methods=['GET', 'POST'])
def registercid(cid):
    # this method adds a given course to a student's "cart", stored in a session variable.
    # these courses are only added to their enrollment once they click "Complete Registration"
    if 'username' not in session:
        return render_template("register.html", err=1)
    if request.method == "POST":
        # you can add any course to your cart, validation (overlappting times, proper prerequsities)
        # is once "complete registration" is clicked
        if 'cart' not in session:
            session['cart'] = list()
            cart = [cid]
            session['cart'] = cart
            # print(session['cart'])
        else:
            cart = session['cart']
            cart.append(cid)
            session['cart'] = cart
            # print(session['cart'])
    return redirect('/register')

@app.route('/remove/<cid>', methods=['GET', 'POST'])
def removecid(cid):
    # this method removes a course from the "cart"
    # you can only remove a course once it is in your cart, this is based in the HTML
    if 'username' not in session:
        return render_template("register.html", err=1)
    if request.method == "POST":
        if 'cart' in session:
            cart = session['cart']
            cart.remove(cid)
            session['cart'] = cart
    return redirect('/register')

@app.route("/admin_student_facultyListsearch", methods = ['GET','POST'])
def admin_student_facultyListsearch():
    if 'username' not in session:
        return redirect("/")

    default_value = 0



    # mydb = mysql.connector.connect(
    # host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    # user = "admin",
    # password = "iGoByAdham$4*8",
    # database = "AdvisingSystem_ADS_3"  
    # )
    c = mydb.cursor(dictionary = True)
    ##use to retrieve basic information on user

    query = "%"+request.args.get("query")+"%"
    c.execute("Select * from advises_on WHERE (fid LIKE %s OR student_id LIKE %s)", (query, query))
    results = c.fetchall()

    username = session['username']

    if request.method == 'POST':


        if request.form.get('Button', default_value) == "Back to Home":
            return redirect('/info')

        data = request.form.get ("Delete" , default_value)
        if data == "Delete":
            student = request.form.get('student_id', default_value)
            faculty = request.form.get('faculty_id',default_value)
            # print(student)
            c.execute("DELETE FROM advises_on WHERE fid = %s AND student_id = %s", (faculty, student,))
            mydb.commit()
            c.execute("Select * from advises_on")
            results = c.fetchall()
            c.close()

            return render_template('admin_student_facultyList.html', username = username, results = results)
        return render_template('admin_student_facultyList.html', username = username, results = results)

    return render_template('admin_student_facultyList.html', username = username, results = results)

@app.route('/submit')
def submit():
    # this method is called when the student clicks on "complete registration"
    # checks for validity, and if all courses can be registered for, enrolls a student in the
    # courses they have selected for their cart
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM course_offered JOIN course ON course.courseid = course_offered.courseid")
    courses = cursor.fetchall()
    if 'cart' not in session:
        return render_template("register.html", courses=courses, err=4)
    else:
        cart = list()
        for course in session['cart']:
            cursor.execute("SELECT * FROM course_offered JOIN course ON course.courseid = course_offered.courseid HAVING course.courseid = %s", (course,))
            cart.append(cursor.fetchone())
        # check for the same time slot
        # fix logic here
        for item in cart:
            for other_item in cart:
                if item['courseid'] != other_item['courseid'] and item['day'] == other_item['day']:
                    if (item['end_time'] >= other_item['start_time'] and item['end_time'] <= other_item['end_time']) or (item['start_time'] <= other_item['end_time'] and item['end_time'] >= other_item['end_time']):
                        session.pop('cart')
                        return render_template("register.html", courses=courses, err=3, course1 = item['title'], course2 = other_item['title'])
        cursor.execute("SELECT * FROM constants")
        constants = cursor.fetchone()
        # print(constants)
        cursor.execute("SELECT * FROM takes_course JOIN course_offered ON takes_course.courseid = course_offered.courseid WHERE studentid = %s AND semester = %s AND year_taken = %s AND grade = 'IP'", (session['id'], constants['cur_sem'], constants['cur_year']))
        in_progress = cursor.fetchall()
        # print(in_progress)
        for item in cart:
            for other_item in in_progress:
                if item['courseid'] != other_item['courseid'] and item['day'] == other_item['day']:
                    if (item['end_time'] >= other_item['start_time'] and item['end_time'] <= other_item['end_time']) or (item['start_time'] <= other_item['end_time'] and item['end_time'] >= other_item['end_time']):
                        session.pop('cart')
                        cursor.execute("SELECT title FROM course WHERE courseid = %s", (other_item['courseid'],))
                        # print("here")
                        conflictedcourse = cursor.fetchone()
                        # print("here")
                        # print(conflictedcourse)
                        return render_template("register.html", courses=courses, err=3.5, course1 = item['title'], course2 = conflictedcourse['title'])

        # another error check: make sure they haven't already taken the course!!

        cursor.execute("SELECT * FROM takes_course WHERE studentid = %s", (session['id'],))
        taken = cursor.fetchall()
        for item in cart:
            for other_item in taken:
                if item['courseid'] == other_item['courseid']:
                    session.pop('cart')
                    return render_template("register.html", courses=courses, err=5, course1 = item['title'])

        cursor.execute("SELECT * FROM constants")
        constants = cursor.fetchone()
        # print(constants)
        for course in session['cart']:
            # ensure prerequisites have already been taken
            cursor.execute("SELECT * FROM prereq_of WHERE courseid LIKE %s", (course,))
            prereqs = cursor.fetchall()
            cursor.execute("SELECT * FROM takes_course WHERE studentid LIKE %s", (session['id'],))
            taken = cursor.fetchall()
            taken_list = list()
            for t in taken:
                taken_list.append(t['courseid'])
            for pr in prereqs:
                if pr['pr_cid'] not in taken_list:
                    session.pop('cart')
                    cursor.execute("SELECT * FROM course_offered JOIN course ON course.courseid = course_offered.courseid")
                    courses = cursor.fetchall()
                    cursor.execute("SELECT title FROM course WHERE courseid = %s", (pr['courseid'],))
                    prtitle = cursor.fetchone()['title']
                    return render_template("register.html", courses=courses, err=2, prtitle=prtitle)

            cursor.execute("INSERT INTO takes_course VALUES (%s, %s, %s, %s, %s)", (session['id'], course, constants['cur_sem'], constants['cur_year'], 'IP'))
            mydb.commit()
        cursor.close()
        session.pop('cart')
    return redirect('/info')

@app.route("/transcriptsearch", methods = ['GET', 'POST'])
def transcriptsearch():

    if 'username' not in session:
        return redirect("/")   

    ##Connect to database here
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )

    username = session['username']
    c = mydb.cursor(dictionary = True)
    c.execute("SELECT * FROM users WHERE uname = %s", (username,))
    id = c.fetchone()
    print("id:", id)
    c = mydb.cursor()
    c.execute("SELECT grade FROM takes_course where studentid = %s", (id['uid'],))
    grades = c.fetchall()
    # print(grades)
    if grades != None:
        num = round(gpa_calculator(grades), 2)
    c = mydb.cursor(dictionary = True)
    query = "%"+request.args.get("query")+"%"
    c.execute("SELECT * FROM takes_course INNER JOIN course ON course.courseid = takes_course.courseid WHERE course.courseid LIKE %s HAVING studentid = %s ORDER BY year_taken, semester", (query, id['uid']))
    program_curr = c.fetchall()

    c.execute("SELECT program FROM users where uname = %s",(username,))
    typedegree = c.fetchone()
    # print(typedegree)
    # print(program_curr)

    msg =""

    if typedegree['program'] == "PHD":
        c.execute("SELECT minGPA FROM requirements where degree_type = 'PHD'")
        min = c.fetchone()
        if num<min['minGPA']:
            msg = "Minimum GPA not met seek advisor"

        # check to seee that they have taken 30 credit hours in cs
        # 36 credits total
        c.execute("SELECT * FROM takes_course INNER JOIN course ON course.courseid = takes_course.courseid HAVING studentid = %s", (id['uid'],))
        req = c.fetchall()
        print("REQ: ", req)

        total_credits = 0

        for i in req:
            total_credits += i['credits']
        if total_credits < 36:
            msg = "Not enough credits to graduate"

        cs_credit = 0
        for i in req:
            if i['dept'] == "CSCI":
                cs_credit += i['credits']
        if cs_credit < 30:
            msg = "Not enough cs credits hours to graduate"



        count = 0
        for i in grades:
            for j in i:
                if j == "B-" or j == "C+" or j =="C" or j == "C-" or j == "D+" or j =="D" or j == "F":
                    count+=1
        if count>1:
            if msg != "":
                msg = msg + " and more than one grade below a B"
            else:
                msg = "More than one grade below a B"

        c = mydb.cursor(dictionary = True)
        c.execute("SELECT thesis_status FROM users where uname = %s LIMIT 1", (username,))
        statusthesis = c.fetchone()
        # print(statusthesis)
        if statusthesis['thesis_status'] != "complete":
            if msg != "":
                msg = msg + " and thesis not passed"
            else:
                msg = "Thesis not passed"

    else:
        # check if they have taken the core classes
        # check if their total credits is greater than 30
        c.execute("SELECT minGPA FROM requirements where degree_type = 'MS'")
        min = c.fetchone()
        if num<min['minGPA']:
            msg = "Minimum GPA not met seek advisor"

        c.execute("SELECT * FROM takes_course INNER JOIN course ON course.courseid = takes_course.courseid HAVING studentid = %s", (id['uid'],))
        req = c.fetchall()

        count_core = 0
        for i in req:
            if i['courseid'] != '03' or i['courseid'] != '01' or i['courseid'] != '02':
                count_core += 1
        if count_core != 3:
            msg = "Don't have the required classes for CS"

        total_credits = 0  
        for i in req:
            total_credits += i['credits']
        if total_credits < 30:
            msg = "Not enough credits to graduate"

        count = 0
        for i in grades:
            for j in i:
                if j == "B-" or j == "C+" or j =="C" or j == "C-" or j == "D+" or j =="D" or j == "F":
                    count+=1
        if count > 2:
            if msg != "":
                msg = msg + " and more than one grade below a B"
            else:
                msg = "More than one grade below a B"

        other_classes = 0
        for i in req:
            if i['dept'] == 'ECE' or i['dept'] == 'MATH':
                other_classes += 1
        if other_classes > 2:
            msg = "Took too many classes outside of CS"


    ##If apply button was clicked
    if request.method == 'POST':
        if request.form['Button'] == "Submit for Graduation":
            msg = "Sucess, your application will be reviewed by a GS"
            status = "sent"

            c.execute("UPDATE users SET grad_status = (%s) WHERE uid = (%s)", (status, username, ))
            mydb.commit()
        else:
            c.close()
            return redirect('/info')


    ##check requirements based on program
    c.close()
    return render_template('transcript.html', gpa = num, proglist = program_curr, err = msg)

@app.route('/enrollment')
def enrollment():
    # shows courses that a student is currently enrolled in
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM constants")
    constants = cursor.fetchone()
    cursor.execute("SELECT courseid FROM takes_course WHERE studentid LIKE %s AND semester LIKE %s AND year_taken LIKE %s",(session['id'], constants['cur_sem'], constants['cur_year']))
    courses = cursor.fetchall()
    enrollment = list()
    for course in courses:
        cursor.execute("SELECT * FROM course JOIN takes_course ON course.courseid = takes_course.courseid HAVING course.courseid LIKE %s AND takes_course.studentid = %s", (course['courseid'], session['id']))
        enrollment.append(cursor.fetchone())
    cursor.close()
    return render_template("enrollment.html", year=constants['cur_year'], semester=constants['cur_sem'], courses=enrollment)

@app.route('/drop/<cid>', methods=['GET', 'POST'])
def dropcid(cid):
    # this method drops a course once it has been registered for
    # accessible via the enrollment page
    if 'username' not in session:
        return render_template("register.html", err=1)
    if request.method == "POST":
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(
            "DELETE FROM takes_course WHERE courseid = %s AND studentid = %s", (cid, session['id']))
        mydb.commit()

    return redirect('/enrollment')

grades = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "F": 0.0
}

@app.route('/gssearch', methods=['GET', 'POST'])
def gssearch():
  if 'username' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    loggedIn, fname, lname = loginInfo()

    try:
      query = "%"+request.args.get("query")+"%"
      cursor.execute("SELECT * FROM application WHERE (fname LIKE %s OR lname LIKE %s) ORDER BY date DESC", (query, query))
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False

    if formsExist:
      return render_template('gs.html', fname = fname, forms = forms, formsExist = formsExist )
    else:
      return render_template('gs.html', fname = fname, formsExist = formsExist )      
  redirect(url_for('logout'))

@app.route('/cacsearch', methods=['GET', 'POST'])
def cacsearch():
  if 'username' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    loggedIn, fname, lname = loginInfo()

    session['fname'] = fname

    try:
      query = "%"+request.args.get("query")+"%"
      cursor.execute("SELECT * FROM application WHERE (fname LIKE %s OR lname LIKE %s) ORDER BY date DESC", (query, query))
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False

    if formsExist:
      return render_template('cac.html', fname = fname, forms = forms, formsExist = formsExist )
    else:
      return render_template('cac.html', fname = fname, formsExist = formsExist )      
  redirect(url_for('logout'))

@app.route('/enrollmentsearch')
def enrollmentsearch():
    # shows courses that a student is currently enrolled in
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM constants")
    constants = cursor.fetchone()
    cursor.execute("SELECT courseid FROM takes_course WHERE studentid LIKE %s AND semester LIKE %s AND year_taken LIKE %s",(session['id'], constants['cur_sem'], constants['cur_year']))
    courses = cursor.fetchall()
    enrollment = list()
    for course in courses:
        query = request.args.get("query")
        cursor.execute("SELECT * FROM course JOIN takes_course ON course.courseid = takes_course.courseid HAVING course.courseid LIKE %s AND takes_course.studentid = %s", (course['courseid'], session['id']))
        course = cursor.fetchone()
        print(course['title'])
        if (query in course['title'].lower()):
            enrollment.append(course)

    cursor.close()
    return render_template("enrollment.html", year=constants['cur_year'], semester=constants['cur_sem'], courses=enrollment)

@app.route('/registersearch')
def registersearch():
    # This makes the assumption that the courses in 'courses_offered'
    # are for the semester a student can currently register for.

    # set up cursor/DB connection
    cursor = mydb.cursor(dictionary=True, buffered=True)
    query = "%"+request.args.get("query")+"%"
    cursor.execute(
        "SELECT * FROM course_offered JOIN course ON course.courseid = course_offered.courseid WHERE course.title LIKE %s", (query,))
    courses = cursor.fetchall()
    # show courses that are being offered
    return render_template("register.html", courses=courses)

@app.route('/grade_entry', methods=['GET', 'POST'])
def grade_entry():
    cursor = mydb.cursor(dictionary=True, buffered=True)
    if 'facultytype' not in session:
      return redirect('/')
    if session['facultytype'] == 'faculty':
        print("accessed1")
        cursor.execute("SELECT course.title FROM teaches INNER JOIN course ON teaches.courseid = course.courseid WHERE teaches.facultyid = %s AND teaches.semester = 'SPRING' AND teaches.year = '2022'", (session['id'],))
        coursesteachingfetch = cursor.fetchall()
        coursesteaching = list()
        for course in coursesteachingfetch:
            coursesteaching.append(course['title'])
    elif session['facultytype'] == 'grad_secretary' or 'cac':
        cursor.execute("SELECT course.title FROM course INNER JOIN course_offered ON course.courseid = course_offered.courseid")
        coursesteachingfetch = cursor.fetchall()
        coursesteaching = list()
        for course in coursesteachingfetch:
            coursesteaching.append(course['title'])
    courseselected = request.args.get('class')
    cursor.execute("SELECT users.* FROM users INNER JOIN takes_course ON users.uid = takes_course.studentid INNER JOIN course ON takes_course.courseid = course.courseid WHERE course.title = %s AND users.is_alumni = 'no'", (courseselected,))
    studentsfetch = cursor.fetchall()
    print(studentsfetch)
    students = list()
    for student in studentsfetch:
        if session['facultytype'] == 'faculty':
            cursor.execute("SELECT takes_course.grade FROM takes_course INNER JOIN course ON takes_course.courseid = course.courseid WHERE takes_course.studentid = %s AND course.title = %s",(student['uid'], courseselected))
            gradefetch = cursor.fetchone()['grade']
            if gradefetch == 'IP':
                studentdict = {'studentid': student['uid'], 'fname': student['fname'], 'lname': student['lname'], 'currentgrade': "IP"}
                students.append(studentdict)
        elif session['facultytype'] == 'grad_secretary' or 'cac':
            print("accessed")
            cursor.execute("SELECT takes_course.grade FROM takes_course INNER JOIN course ON takes_course.courseid = course.courseid WHERE takes_course.studentid = %s AND course.title = %s",(student['uid'], courseselected))
            gradefetch = cursor.fetchone()['grade']
            studentdict = {'studentid': student['uid'], 'fname': student['fname'], 'lname': student['lname'], 'currentgrade': gradefetch}
            # print(studentdict)
            students.append(studentdict)
    studentselected = request.args.get('student')
    gradeselected = request.args.get('grade')
    if courseselected != None and studentselected != None and gradeselected != None:
        # print("Course: " + courseselected + " Student: " + studentselected + " Grade: " + gradeselected)
        allinfo = request.args.to_dict(flat=False)
        # print(allinfo)
        for i in range(len(allinfo['student'])):
            cur_student = allinfo['student'][i]
            cur_grade = allinfo['grade'][i]
            print(courseselected)
            print(cur_student)
            print(cur_grade)
            cursor.execute("UPDATE takes_course INNER JOIN course ON takes_course.courseid = course.courseid SET takes_course.grade = %s WHERE takes_course.studentid = %s AND course.title = %s",(cur_grade, cur_student, courseselected))
        mydb.commit()
        return redirect(request.referrer)
    return render_template("grade_entry.html", courses=coursesteaching, courseselected=courseselected, students=students, studentselected=studentselected, grades=grades, gradeselected=gradeselected)

@app.route('/coursecatalog')
def coursecatalog():
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM course_offered JOIN course ON course.courseid = course_offered.courseid")
    courses = cursor.fetchall()
    return render_template("catalog.html", courses=courses)

@app.route('/coursecatalogsearch')
def coursecatalogsearch():
    cursor = mydb.cursor(dictionary=True, buffered=True)
    query = "%"+request.args.get("query")+"%"
    # print(query)
    cursor.execute("SELECT * FROM course_offered JOIN course ON course.courseid = course_offered.courseid WHERE course.title LIKE %s", (query,))
    courses = cursor.fetchall()
    return render_template("catalog.html", courses=courses)

@app.route('/chyear')
def chyear():
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM constants")
    yearsem = cursor.fetchone()
    cur_year = yearsem['cur_year']
    cur_sem = yearsem['cur_sem']
    return render_template("administrate.html", cur_year = cur_year, cur_sem = cur_sem)


@app.route('/setsem', methods=['GET', 'POST'])
def setsem():
    if request.method == "POST":
        year = request.form['year']
        sem = request.form['sem']
        cursor = mydb.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM constants")
        cur = cursor.fetchone()
        cursor.execute("UPDATE constants SET cur_year = %s, cur_sem = %s WHERE cur_year = %s", (year, sem, cur['cur_year']))
        mydb.commit()
        cursor.execute("SELECT * FROM constants")
        cur = cursor.fetchone()
        cur_year = cur['cur_year']
        cur_sem = cur['cur_sem']
        return render_template("administrate.html", cur_year = cur_year, cur_sem=cur_sem, success=1)

@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM users WHERE uid = %s", (user_id,))
    user_info = cursor.fetchone()
    if request.method == 'POST':
        if request.form['edit'] == "Update User":
            cursor.execute("SELECT email, uname, password, ss_num FROM users WHERE uid != %s", (user_id,))
            userinfo = cursor.fetchall()
            # print(userinfo)
            username = request.form['uname']
            # print(username)
            firstname = request.form['fname']
            # print(firstname)
            lastname = request.form['lname']
            # print(lastname)
            email = request.form['email']
            # print(email)
            password = request.form['password']
            # print(password)
            address = request.form['address']
            # print(address)
            ssn = request.form['ssn']
            # print(ssn)
            for info in userinfo:
                if info['uname'] == username:
                    return render_template("edit_user.html", user = user_info, errormsg = "Username already in use")
                elif info['email'] == email:
                    return render_template("edit_user.html", user = user_info, errormsg = "Email already in use")
                elif info['password'] == password:
                    return render_template("edit_user.html", user = user_info, errormsg = "Password already in use")
                elif info['ss_num'] == ssn:
                    return render_template("edit_user.html", user = user_info, errormsg = "SSN already in use")
            if user_info['role'] == "student" and user_info['program'] != None:
                program = request.form['program']
                # print(program)
                grad_status = request.form['grad_status']
                # print(grad_status)
                is_alumni = request.form['is_alumni']
                # print(is_alumni)
                cursor.execute("UPDATE users SET uname = %s, fname = %s, lname = %s, email = %s, password = %s, address = %s, ss_num = %s, program = %s, grad_status = %s, is_alumni = %s WHERE uid = %s", (username, firstname, lastname, email, password, address, ssn, program, grad_status, is_alumni, user_id))
            else:
                cursor.execute("UPDATE users SET uname = %s, fname = %s, lname = %s, email = %s, password = %s, address = %s, ss_num = %s WHERE uid = %s", (username, firstname, lastname, email, password, address, ssn, user_id))
        elif request.form['edit'] == "Delete User":
            cursor.execute("DELETE FROM teaches WHERE facultyid = %s", (user_id,))
            cursor.execute("DELETE FROM takes_course WHERE studentid = %s", (user_id,))
            cursor.execute("DELETE FROM reference WHERE id = %s", (user_id,))
            cursor.execute("DELETE FROM program_study WHERE univ_id = %s", (user_id,))
            cursor.execute("DELETE FROM letter_review WHERE id = %s", (user_id,))
            cursor.execute("DELETE FROM letter WHERE id = %s", (user_id,))
            cursor.execute("DELETE FROM gas_rating WHERE id = %s", (user_id,))
            cursor.execute("DELETE FROM degree WHERE uid = %s", (user_id,))
            cursor.execute("DELETE FROM application WHERE id = %s", (user_id,))
            cursor.execute("DELETE FROM advises_on WHERE fid = %s", (user_id,))
            cursor.execute("DELETE FROM advises_on WHERE student_id = %s", (user_id,))
            mydb.commit()
            cursor.execute("DELETE FROM users WHERE uid = %s", (user_id,))
        mydb.commit()
        return redirect('/info')
    return render_template("edit_user.html", user = user_info, errormsg = "")

@app.route("/reset", methods = ['GET', 'POST'])
def reset():
    cursor = mydb.cursor(dictionary=True, buffered=True)
    cursor.execute("DELETE FROM advises_on")
    cursor.execute("DELETE FROM application")
    cursor.execute("DELETE FROM constants")
    cursor.execute("DELETE FROM degree")
    cursor.execute("DELETE FROM gas_rating")
    cursor.execute("DELETE FROM letter")
    cursor.execute("DELETE FROM letter_review")
    cursor.execute("DELETE FROM program_study")
    cursor.execute("DELETE FROM reference")
    cursor.execute("DELETE FROM takes_course")
    cursor.execute("DELETE FROM teaches")
    cursor.execute("DELETE FROM users")

    cursor.execute("INSERT INTO users VALUES ('11111125', 'bnarahari', 'Bhagi', 'Narahari', 'bnarahari@gwu.edu', 'narahari', '123 narahari lane', '123456789', 'faculty', NULL, NULL, NULL, NULL, NULL)")
    cursor.execute("INSERT INTO users VALUES ('11111155', 'choi', 'Hyeong', 'Choi', 'choi@gwu.edu', 'choipass', '123 choi lane', '332432154', 'faculty', NULL, NULL, NULL, NULL, NULL)")
    cursor.execute("INSERT INTO users VALUES ('11111166', 'gabe', 'Gabriel', 'Parmer', 'parmer@gwu.edu', 'parmerpass', '123 parmer lane', '386432154', 'faculty', NULL, NULL, NULL, NULL, NULL)")
    
    cursor.execute("INSERT INTO users VALUES ('22222235', 'gradsecretary', 'Grad', 'Secretary', 'gradsecretary@gwu.edu', 'gspass', '456 gradsec ave', '987654321', 'grad_secretary', NULL, NULL, NULL, NULL, NULL)")
    cursor.execute("INSERT INTO users VALUES ('33333345', 'systemsadmin', 'Systems', 'Admin', 'systemsadmin@gwu.edu', 'sapass', '789 systems road', '457893847', 'system_admin', NULL, NULL, NULL, NULL, NULL)")
    cursor.execute("INSERT INTO users VALUES ('33333340', 'cac', 'Chair of Admissions', 'Committee', 'cac@gwu.edu', 'cacpass', '789 cac road', '473291673', 'cac', NULL, NULL, NULL, NULL, NULL)")

    cursor.execute("INSERT INTO users VALUES ('44444455', 'pravinkhanal', 'Pravin', 'Khanal', 'pkhanal@gwu.edu', 'khanal', '3456 nepal street', '865444687', 'student', 'PHD', 'no', NULL, 'no', NULL)")
    cursor.execute("INSERT INTO users VALUES ('55555565', 'joshrizika', 'Joshua', 'Rizika', 'joshrizika@gwu.edu', 'rizika', '332 josh street', '953659532', 'student', 'MS', 'no', NULL, 'no', NULL)")
    cursor.execute("INSERT INTO users VALUES ('66666668', 'abdullahalm', 'Abdullah', 'Almaayoof', 'abdullah@gwu.edu', 'almaayoof', '986 aa lane', '696726849', 'student', 'PHD', 'done', NULL, 'yes', NULL)")
    cursor.execute("INSERT INTO users VALUES ('12312312', 'jlennon', 'John', 'Lennon', 'jlennon@gwu.edu', 'johnpass', '123 main dr', '111111111', 'student', 'NULL', 'no', NULL, 'no', NULL)")
    cursor.execute("INSERT INTO users VALUES ('66666666', 'ringo', 'Ringo', 'Starr', 'ringo@gwu.edu', 'ringopass', '231 ringo blvd', '222111111', 'student', 'NULL', 'NULL', NULL, 'NULL', NULL)")
    cursor.execute("INSERT INTO users VALUES ('88888888', 'billie', 'Billie', 'Holiday', 'billie@gwu.edu', 'billiepass', '654 billie ct', '236647687', 'student', 'MS', 'NULL', NULL, 'NULL', NULL)")
    cursor.execute("INSERT INTO users VALUES ('99999999', 'diana', 'Diana', 'Krall', 'diana@gwu.edu', 'dianapass', '744 diana st', '342165785', 'student', 'MS', 'NULL', NULL, 'NULL', NULL)")
    cursor.execute("INSERT INTO users VALUES ('55555555', 'paul', 'Paul', 'McCartney', 'paul@gwu.edu', 'paulpass', '744 paul st', '384621765', 'student', 'MS', 'NULL', NULL, 'NULL', NULL)")
    cursor.execute("INSERT INTO users VALUES ('66666667', 'george', 'George', 'Harrison', 'george@gwu.edu', 'georgepass', '744 george st', '384561765', 'student', 'MS', 'NULL', NULL, 'NULL', NULL)")
    cursor.execute("INSERT INTO users VALUES ('66666669', 'jett', 'Jet', 'Jacob', 'jet@gwu.edu', 'jetpass', '744 jet st', '384561705', 'student', 'PHD', 'NULL', NULL, 'NULL', NULL)")
    cursor.execute("INSERT INTO users VALUES ('77777777', 'clapton', 'Eric', 'Clapton', 'eric@gwu.edu', 'ericpass', '744 eric st', '384591705', 'student', 'MS', 'done', NULL, 'yes', NULL)")
    
    cursor.execute("INSERT INTO constants VALUES ('2022', 'SPRING')")

    cursor.execute("INSERT INTO takes_course VALUES ('44444455','02', 'SPRING', '2022', 'IP')")
    cursor.execute("INSERT INTO takes_course VALUES ('44444455','03', 'SPRING', '2022', 'IP')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555565','02', 'SPRING', '2022', 'IP')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555565','03', 'SPRING', '2022', 'IP')")
    cursor.execute("INSERT INTO takes_course VALUES ('88888888','02', 'SPRING', '2022', 'IP')")
    cursor.execute("INSERT INTO takes_course VALUES ('88888888','03', 'SPRING', '2022', 'IP')")

    cursor.execute("INSERT INTO takes_course VALUES ('55555555','01', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','03', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','02', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','05', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','06', 'SPRING', '2022', 'A')")

    cursor.execute("INSERT INTO takes_course VALUES ('55555555','07', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','09', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','13', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','14', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('55555555','08', 'SPRING', '2022', 'B')")


    cursor.execute("INSERT INTO takes_course VALUES ('66666667','20', 'SPRING', '2022', 'C')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','01', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','02', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','03', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','05', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','06', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','07', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','08', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','14', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666667','15', 'SPRING', '2022', 'B')")
    


    cursor.execute("INSERT INTO takes_course VALUES ('66666669','04', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','01', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','02', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','03', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','05', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','06', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','07', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','08', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','09', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','10', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','15', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('66666669','11', 'SPRING', '2022', 'A')")

    cursor.execute("INSERT INTO takes_course VALUES ('77777777','01', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','03', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','02', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','05', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','06', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','08', 'SPRING', '2022', 'B')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','14', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','15', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','16', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','10', 'SPRING', '2022', 'A')")
    cursor.execute("INSERT INTO takes_course VALUES ('77777777','15', 'SPRING', '2022', 'A')")


    cursor.execute("INSERT INTO teaches VALUES ('11111125', '02', 'SPRING', '2022')")
    cursor.execute("INSERT INTO teaches VALUES ('11111155', '03', 'SPRING', '2022')")

    cursor.execute("INSERT INTO advises_on VALUES ('11111125', 'CSCI', '44444455')")
    cursor.execute("INSERT INTO advises_on VALUES ('11111125', 'CSCI', '55555555')")
    cursor.execute("INSERT INTO advises_on VALUES ('11111166', 'CSCI', '66666669')")
    cursor.execute("INSERT INTO advises_on VALUES ('11111166', 'CSCI', '66666667')")


    cursor.execute("INSERT INTO application VALUES ('44444455','Khanal','Pravin','PHD','Fall 2020','Computer Science','Worked at Microsoft','3','220','200','2020','Mathematics','200','150','2019', '5', DEFAULT, '05/04/2022')")
    cursor.execute("INSERT INTO application VALUES ('12312312','Lennon','John','MS','Fall 2023','Computer Science','Worked at Apple','3','123','123','2020','Physics','200','150','2019', '5', DEFAULT, '07/04/2022')")
    cursor.execute("INSERT INTO application VALUES ('66666667','Harrison','George','MS','Fall 2020','Computer Science','Worked at Apple','3','123','123','2020','Physics','200','150','2019', '5', 'admit', '07/04/2021')")
    cursor.execute("INSERT INTO application VALUES ('88888888','Holiday','Billie','MS','Fall 2020','Computer Science','Worked at Amazon','3','123','123','2020','Physics','200','150','2019', '5', 'admit', '07/04/2020')")
    cursor.execute("INSERT INTO application VALUES ('99999999','Krall','Diana','MS','Fall 2020','Computer Science','Worked at Tesla','3','123','123','2020','Physics','200','150','2019', '5', 'admit', '07/01/2021')")
    cursor.execute("INSERT INTO application VALUES ('55555555','Paul','McCartney','MS','Fall 2020','Computer Science','Worked at Google','3','123','123','2020','Physics','200','150','2019', '5', 'admit', '07/01/2020')")
    cursor.execute("INSERT INTO application VALUES ('66666669','Jet','Jacob','PHD','Fall 2020','Computer Science','CEO of Google','3','123','123','2020','Physics','200','150','2019', '5', 'admit', '07/05/2020')")
   
    cursor.execute("INSERT INTO degree VALUES ('44444455','BS','4.0','Computer Science','2020','University of Maryland')")
    cursor.execute("INSERT INTO degree VALUES ('12312312','BS','3.9','Computer Science','2019','George Washington University')")


    cursor.execute("INSERT INTO reference VALUES ('44444455','George','Martin','martingeorge@email.com','Professor','EMI')")
    cursor.execute("INSERT INTO reference VALUES ('12312312','Tim','Wood','timwood@gwu.edu','Professor','GW')")
    
    cursor.execute("INSERT INTO letter VALUES ('44444455','George Martin','Very good student. Please admit.')")
    cursor.execute("INSERT INTO letter VALUES ('12312312','Tim Wood','John is a great student')")

    mydb.commit()
    
    return redirect("/")

### //////////////////////////////////////////////////////////////////////////////////////// ###
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
