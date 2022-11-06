from turtle import update
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
    
    ##Connect to database here
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )
    c = mydb.cursor(dictionary = True)
    
    if "username" in session:
        return redirect('/info')
        
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        print(username)
        print(password)

        ##select statement into database and check if email and password exist there
        c.execute("Select * from users where uname = %s and password = %s", (username, password,))
        results = c.fetchone()
        c.close()

        ##check to see if user input is in database
        print(results)
        if results == None:
            msg = "Not found, try again"
            return render_template('login.html', error = msg)
        else:
            session['username'] = username
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

    print (results)
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
            print("stuff")
            student = request.form.get('student_id', default_value)
            faculty = request.form.get('faculty_id',default_value)
            print(student)
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
    c = mydb.cursor(dictionary = True)
    ##use to retrieve basic information on user
    username = session['username']
    print(username)

    ##COULD DO IF STATEMENT FOR SYS ADMIN THAT ALLOWS THEM VIEW ALL
    ##Check TYPE USER
    c.execute("Select * from users where uname = %s LIMIT 1", (username,))
    results = 0
    syscheck = c.fetchone()


    if syscheck['role'] == 'system_admin' or syscheck['role'] == 'grad_secretary':
        c.execute("Select * from users")
        results = c.fetchall()
        print(results)
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
            print(student)
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
            print(student)
            c.execute("Select fname from users where uid = %s", (student,))
            student_name = c.fetchone()
            c.execute("Select * from program_study where univ_id = %s", (student,))
            results = c.fetchall()
            if (results == [] or results == None):
                return render_template('student_programstudy.html',msg = "No Program Study Found", username = student_name['fname'],results = results)
            c.close()
            return render_template('student_programstudy.html', msg = "", username = student_name['fname'],results = results)

    print (results)
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
            print("stuff")
            student = request.form.get('student_id', default_value)
            faculty = request.form.get('faculty_id',default_value)
            print(student)
            c.execute("DELETE FROM advises_on WHERE fid = %s AND student_id = %s", (faculty, student,))
            mydb.commit()
            c.execute("Select * from advises_on")
            results = c.fetchall()
            # c.close()

            return render_template('assign_faculty_student.html', results = results)
        

        faculty = request.form["faculty"]
        student = request.form["student"]
        print ("faculty:", faculty)
        print ("student:", student)
        c.execute( "Select * From users Where uid = %s",(student,))
        student_check = c.fetchall()
        print("student_check:", student_check)
        if (student_check == [] or student_check == None):
            return render_template('assign_faculty_student.html', results = results,msg = "Invalid Insertion no student exists")
        


        c.execute("Select role From users where uid = %s", (faculty,))
        faculty_verify = c.fetchone()
        print(faculty_verify)
        if (faculty_verify == [] or faculty_verify == None  or faculty_verify['role'] != "faculty"):
            return render_template('assign_faculty_student.html',results = results, msg = "Invalid Insertion no Faculty exist")
        
        c.execute("Select dname From advises_on WHERE fid = %s",(faculty,))
        department = c.fetchone()
        if (department == [] or department == None ):
            department = request.form["department"]
            if(department == ""):
                return render_template('assign_faculty_student.html',results = results, msg = "Enter a Department Name")
           

        print("Student ID: ", student)
        c.execute("Select * From advises_on WHERE student_id = %s", (student,))
        error_check = c.fetchall()
        print("check:", error_check)
        if(error_check == [] or error_check == None):
            print(department)
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

        c.execute("UPDATE users SET is_alumni = 'yes' WHERE uid = %s", (target,))
        c.execute("UPDATE users SET grad_status = 'none' WHERE uid = %s", (target,))
        mydb.commit()

    
    ##First get applicable
    c.execute("SELECT uid, lname, fname, program FROM users where grad_status = 'sent' ORDER BY uid ASC")

    basic_info = c.fetchall()
    print(basic_info)
    num_students = len(basic_info)
    for i in basic_info:
        username = i['uid'] 
        c.execute("SELECT * FROM takes_course where studentid = %s", (username,))
        program_curr = c.fetchall()
        i["program_study"] = program_curr
        print(i["program_study"])

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
    print("user in session:", session['username'])

    ##select statement into database and check if email and password exist there
    c.execute("Select * from users where uname = %s", (username,))
    results = c.fetchone()
    print("results", results)

    if results['role'] == 'student':
        c.execute("Select * from users where uname = %s", (username,))
        results = c.fetchone()
        # print(results)
        if results['is_alumni'] == 'yes':
            return render_template('alumni_student.html', results = results)
        return render_template('grad_student.html', results = results)

    if results['role'] == 'system_admin':
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        c.close()
        return render_template('admin.html', users = users)
    
    if results['role'] == 'faculty':
        return render_template('faculty_advisor.html', results = results)
        
    if results['role'] == "grad_secretary":
        print("grad secretary:", results)
        return render_template('grad_secretary.html', results = results)
    
    
    # print(results['uname'])
    # print(results['role'])

    ##Based on type user, render specific type of dashboard

    c.close()
    return render_template('login.html')


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

    
    c = mydb.cursor(dictionary = True)

    ##use to retrieve basic information on user
    username = session['username']

    c.execute("Select * from program_study where univ_id = %s", (username,))
    checkinsert = c.fetchall()
    print(checkinsert)
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
        print(input12crn)
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
        print(input10_id)

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
        print(checklist)
        print(count)

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
        print(enrollcheck)

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
            print("success")
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
                print(i['course_num'])
                print(i['dept'])
                print(req)
                ##if i['course_id'] == req[0][0] or i['course_id'] == req[1][0] or i['course_id'] == [2][0]:
                if i['courseid'] == '03' or i['courseid'] == '01' or i['courseid'] == '02':
                    count_core+=1
                if i['dept'] != 'CSCI':
                    non_cs+=1
            if count_core != 3:
                print(count_core)
                msg = "Error, 3 core classes CSCI 6212 CSCI 6221 CSCI 6461 must be included"
                return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
            
            if non_cs > 2:
                msg = "Error, at most 2 non-CS course, try again"
                return render_template('form.html', id = results['uid'], name = results['fname'] + " " + results['lname'], error = msg)
            print("success")
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
    print("here:",results)
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
    print("id:", id)
    c = mydb.cursor()
    c.execute("SELECT grade FROM takes_course where studentid = %s", (id['uid'],))
    grades = c.fetchall()
    print("grades:", grades )
    # print(grades)
    num = round(gpa_calculator(grades), 2)
    c = mydb.cursor(dictionary = True)
    c.execute("SELECT * FROM takes_course INNER JOIN course ON course.courseid = takes_course.courseid HAVING studentid = %s ORDER BY year_taken, semester", (id['uid'],))
    program_curr = c.fetchall()
    c.execute("SELECT program FROM users where uname = %s",(username,))
    typedegree = c.fetchone()
    print(typedegree)
    print(program_curr)

    msg =""
    
    if typedegree['program'] == "PHD":
        c.execute("SELECT minGPA FROM requirements where degree_type = 'PHD'")
        min = c.fetchone()
        if num<min['minGPA']:
            msg = "Minimum GPA not met seek advisor"
    
        count = 0
        for i in grades:
            for j in i:
                if j == "B-" or j == "C+" or j =="C" or j == "C-" or j == "D+" or j =="D" or j == "F" or j == "IP":
                    count+=1
        if count>1:
            if msg != "":
                msg = msg + " and more than one grade below a B"
            else:
                msg = "More than one grade below a B"

        c = mydb.cursor(dictionary = True)
        c.execute("SELECT thesis_status FROM users where uname = %s LIMIT 1", (username,))
        statusthesis = c.fetchone()
        print(statusthesis)
        if statusthesis['thesis_status'] != "complete":
            if msg != "":
                msg = msg + " and thesis not passed"
            else:
                msg = "Thesis not passed"
        
    else:
        c.execute("SELECT minGPA FROM requirements where degree_type = 'MS'")
        min = c.fetchone()
        if num<min['minGPA']:
            msg = "Minimum GPA not met seek advisor"
        


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


def gpa_calculator(grades):
    points = 0
    i = 0
    grade_c = {"A":4,"A-":3.67,"B+":3.33,"B":3.0,"B-":2.67, "C+":2.33,"C":2.0,"C-":1.67,"D+":1.33,"D":1.0,"F":0}
    if grades != []:
        for i in grades:
            for j in i:
                if j != "IP":
                    points += grade_c[j]
        gpa = points / len(grades)
        return gpa
    else:
        return 0.0
 
 

@app.route("/update_info", methods = ['GET', 'POST'])
def update_info():
    
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


    username = session['username']
    c.execute("Select * FROM users WHERE uname =(%s)",(username,))
    result = c.fetchone()
    print(result)

    if request.method == 'POST':
        if request.form['Button'] == "Confirm":
            msg = "Succesfully Updated"
            address = request.form['address']
            # phonenmbr = request.form['phonenmbr']
            email = request.form['email']
            username = session['username']
            c.execute("UPDATE users SET address = (%s) where uname = (%s)", (address, username,))
            # c.execute("UPDATE users SET phonenmbr = (%s) where uid = (%s)", (phonenmbr, username,))
            c.execute("UPDATE users SET email = (%s) where uname = (%s)", (email, username,))
            mydb.commit()
            return redirect('/info')
        else:
            c.close()
            return redirect('/info')
    return render_template('update_info.html', result = result)


@app.route("/create_user", methods = ['GET', 'POST'])
def create_user():
    ##Connect to database here
    # mydb = mysql.connector.connect(
    #     host = "ads-3.catiyzmpqdxa.us-east-1.rds.amazonaws.com",
    #     user = "admin",
    #     password = "iGoByAdham$4*8",
    #     database = "AdvisingSystem_ADS_3"
    # )
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
                print(role)
                print(type(role))
                c.execute("SELECT * FROM users WHERE uname = %s", (uname,))
                error_checking = c.fetchall()
                if(error_checking == [] or error_checking == None):
                    session['uname'] = uname
                    session['password'] = password
                    session['role'] = role
                    print("hi")
                    if role == "student" or role == 'student':
                        session['check'] = 'check'
                        return redirect('/enter_info')
                else:
                    return render_template('create_user.html', msg = "Invalid User ID")
            
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
                session['uname'] = uname
                session['password'] = password
                session['role'] = role
                # c.execute("INSERT INTO users(uname,password,role) VALUES (%s, %s, %s)", (uname,password,role,))
                # mydb.commit()
                if role == "student"or role == "faculty" or role == 'faculty' or role == "grad_secratary" or role == 'grad_secretay' or role == "systems_admin" or role == 'system_admin':
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
                c.execute("INSERT INTO users(uname, fname, lname, email, password, address, ss_num, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (session['uname'], fname, lname, email, session['password'], address, ssn, session['role'],))
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
        print(target)

        c.execute("UPDATE users SET thesis_status = (%s) where uid = (%s)", ("complete", target))
        mydb.commit()
    
    username = session['username']
    print(username)
    c.execute("SELECT uid FROM users WHERE uname = %s", (username,))
    username = c.fetchone()
    c.execute("Select * FROM users INNER JOIN advises_on ON advises_on.student_id = users.uid WHERE (thesis_status = %s AND fid = %s)", ("pending",username['uid'],))
    allthesis = c.fetchall()
    print(allthesis)

    return render_template('approvethesis.html', info = allthesis)

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")






