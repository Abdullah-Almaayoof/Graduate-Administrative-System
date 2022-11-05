from audioop import add
from queue import Empty
import mysql.connector, random
from flask import Flask, session, render_template, request, redirect, url_for

app = Flask('app')
app.secret_key = "password123"

mydb = mysql.connector.connect(
    host="gib.c8rnuhqze26n.us-east-1.rds.amazonaws.com",
    user="admin",
    password= "M5jp2GbGDqEW",
    database="university" 
)


### Function that checks if user logged is logged in or not, and directing the user to 
# the appropiate page ###
@app.route('/')
def loginForm():
  if 'uname' in session:

    #connect to database
    cursor = mydb.cursor(dictionary=True)

    # mySQL query to find the role of the user
    cursor.execute("SELECT role FROM users WHERE uname ='" + session['uname'] + "'")
    role = cursor.fetchone()
    cursor.reset()

    # Depending on role, redirect to appropriate function
    if role.get('role') == 'student':                                     
      return redirect(url_for('applicant'))
    elif role.get('role') == 'faculty':
      return redirect(url_for('reviewer'))
    elif role.get('role') == 'grad_secretary':
      return redirect(url_for('gs'))
    elif role.get('role') == 'cac':
      return redirect(url_for('cac'))
    elif role.get('role') == 'system_admin':
      return redirect(url_for('sysadmin'))
  # No user in session, redirect to login.html
  else:
    return render_template('login.html')
      

### This function gets basic info about the logged in user by checking the session ###
def loginInfo():
  #connect to database
  cursor = mydb.cursor(dictionary=True)

  if 'uname' not in session:
    uid = ''
    fname = ''
  else:
    cursor.execute("SELECT uid, fname FROM users WHERE uname ='" + session['uname'] + "'")
    user = cursor.fetchone()
    uid = user.get('uid')
    fname = user.get('fname')

  return (uid, fname)


### Function that validates login credentials with database ###
def validLogin(uname, password):
  #connect to database
  cursor = mydb.cursor()

  cursor.execute('SELECT uname, password FROM users')
  data = cursor.fetchall()
  cursor.reset()

  for i in data:
    if i[0] == uname.strip() and i[1] == password:
      return True
  return False


### Function that logs a user in by setting a session with the user's username. It also checks if 
# credentials are correct by calling function 'validLogin' with the username and password passed in ###
@app.route('/login', methods=['GET', 'POST'])
def login():
  cursor = mydb.cursor(dictionary=True)

  # Collect login credentials
  if request.method == 'POST':
    uname = request.form["email"]
    password = request.form["pass"]

    # If login is valid, create session, find the role of the user, and redirect them accordinlgy
    if validLogin(uname, password):
      session['uname'] = uname.strip()

      cursor.execute("SELECT role FROM users WHERE uname ='" + session['uname'] + "'")
      role = cursor.fetchone()
      cursor.reset()

      if role.get('role') == 'student':
        return redirect(url_for('applicant'))
      elif role.get('role') == 'faculty':
        return redirect(url_for('reviewer'))
      elif role.get('role') == 'grad_secretary':
        return redirect(url_for('gs'))
      elif role.get('role') == 'cac':
        return redirect(url_for('cac'))
      elif role.get('role') == 'system_admin':
        return redirect(url_for('sysadmin'))
    # Login is invalid, return to login.html
    else:
      errmsg = 'Invalid email/password, please try again'
      return render_template('login.html', msg = errmsg)

  return render_template('login.html')


### Function that enables a user to register and enter new data into the table 'applicants' ###
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  #connect to database
  cursor = mydb.cursor(dictionary=True)
  
  # Collect registration information
  if request.method == 'POST':
    firstName = request.form["fname"]
    lastName = request.form["lname"]
    uname = request.form["uname"]
    email = request.form["email"]
    password = request.form["pass"]
    password2 = request.form["pass2"]
    ssn = request.form["ssn"]
    address = request.form["address"]

    # Confirm both passwords match
    if password != password2:
      errmsg = "Please re-enter password"
      return render_template('signup.html', errmsg = errmsg)
    else:
      try:
        # MySQL query to insert new user into the user table
        cursor.execute("INSERT INTO users (uname, fname, lname, email, password, address, ss_num, role) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(uname, firstName, lastName, email, password, address, ssn, "student"))
        mydb.commit()
        # print('New registered applicant!')
        msg = 'Registered Succesfully'
        return render_template('login.html', msg = msg)
      except:
        mydb.rollback()
        # print("error occured")
        errmsg = 'An expected error occured, please try again'
    return render_template('signup.html', errmsg = errmsg)
  return render_template('signup.html')

### Function that pops the session when user logs out ###
@app.route('/logout')
def logout():
  session.pop('uname', None)
  return render_template("login.html")


### Function that displays the home page and collects all items in the 'product' table ###
@app.route('/applicant', methods=['GET', 'POST'])
def applicant():
  if 'uname' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    uid, fname = loginInfo()

    refEmail = ''

    refExists = recLetterCheck()

    if refExists:
      cursor.execute("SELECT ref_email FROM reference WHERE id=" + str(uid))
      reference = cursor.fetchone()
      refEmail = reference.get('ref_email')
    
    cursor.execute("SELECT app_status FROM application WHERE id =" + str(uid))
    form = cursor.fetchone()
    
    if form:
      app_status = form.get('app_status')
      formsExist = True
    else:
      formsExist = False

      
    if formsExist and refEmail:
      return render_template('applicant.html', uid = uid, fname = fname, status = app_status, formsExist = formsExist, refEmail = refEmail)
    elif formsExist:
      return render_template('applicant.html', uid = uid, fname = fname, status = app_status, formsExist = formsExist)
    else:
      return render_template('applicant.html', fname = fname, formsExist = formsExist)

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
    

    cursor.execute("SELECT uid, lname, fname FROM users WHERE uname ='" + session['uname'] + "'")
    user= cursor.fetchone()
    uid = user.get("uid")
    fname = user.get("fname")
    lname = user.get("lname")
    complete = 1

    try:
      cursor.execute("INSERT INTO application (id, lname, fname, app_degree, semester, area_interest, experience, complete, gre_verbal, gre_quant, gre_year, gre_adv_sub, gre_adv_score, toefl_score, toefl_year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(uid, lname, fname, typeDeg, adminDate, interestIn, experience, complete, greVerbal, greQuant, greYear, greAdvSub, greAdvScore, tflScore, tflDate))
      cursor.execute("INSERT INTO degree (uid, degree_name, gpa, major, degree_year, university) VALUES (%s,%s,%s,%s,%s,%s)",(uid, priorDeg1, priorDeg1GPA, priorDeg1Major, priorDeg1Year, priorDeg1Uni))
      cursor.execute("INSERT INTO reference (id, ref_fname, ref_lname, ref_email, title, affiliation) VALUES (%s,%s,%s,%s,%s,%s)", (uid, reference1Fname, reference1Lname, reference1Email, reference1Title, reference1Affil))
      
      # Maybe update after student is admitted?
      # cursor.execute("UPDATE users SET program = %s WHERE uid = %s", (typeDeg, uid))
      if priorDeg2 and priorDeg2.strip():
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
  cursor = mydb.cursor(dictionary=True)
  refEmail = request.args.get("refEmail")

  if request.method == 'POST':
    letter = request.form['letter']
    
    cursor.execute("SELECT id, ref_fname, ref_lname FROM reference WHERE ref_email ='" + refEmail + "'")
    reference = cursor.fetchone()
    uid = reference.get("id")
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
  cursor.execute("SELECT uid FROM users WHERE uname='" + session['uname'] + "'")
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
  if 'uname' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    loggedIn, fname = loginInfo()

    try:
      cursor.execute("SELECT * FROM application")
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
  if 'uname' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    loggedIn, fname = loginInfo()

    session['fname'] = fname

    try:
      cursor.execute("SELECT * FROM application")
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
  if 'uname' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    # fname to display
    cursor.execute("SELECT fname FROM users WHERE uname=%s", (session['uname'],) )
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
  if 'uname' in session:
    cursor = mydb.cursor(dictionary=True)
    
    # get role
    cursor.execute("SELECT role FROM users WHERE uname ='" + session['uname'] + "'")
    role = cursor.fetchone()

    # get all info from took
    cursor.execute("SELECT * FROM application WHERE id = '" + id +"'")
    application = cursor.fetchall()
    
    # get all from degree
    cursor.execute("SELECT * FROM degree WHERE uid = '" + id +"'")
    degree = cursor.fetchall()
    
    if role.get('role') == 'grad_secretary':                                     
      return render_template('review_gs.html', application = application, 
                           degree = degree, role = role)
    if role.get('role') == 'cac':                                     
      return render_template('review_cac.html', application = application, 
                           degree = degree, role = role)

    return render_template('review.html', application = application, 
                           degree = degree, role = role)
  return redirect(url_for('logout'))
    




@app.route('/submit_review/<id>', methods=['GET', 'POST'])
def submit_review(id):
  if 'uname' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname = loginInfo()

    # # get role
    cursor.execute("SELECT role FROM users WHERE uname ='" + session['uname'] + "'")
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
  if 'uname' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname = loginInfo()


   
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
      if complete == '3':
        mess = 'Transcript was already marked as complete'
        return render_template('gs.html', fname = fname, mess = mess, forms = forms, formsExist = formsExist)
      else:
        total = complete.get('complete') + 1;
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
  if 'uname' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname = loginInfo()


   
    try:
      cursor.execute("SELECT * FROM application")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False
  

    admission_status = request.form["admission_status"]
    print(admission_status)
    

  if admission_status == "admit":    
      admit_final = "admit"

      try:
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


def getAvg(id):
  cursor = mydb.cursor(dictionary=True)
  cursor.execute("SELECT avg_rating FROM gas_rating WHERE id=%s", (id,) )
  rating = cursor.fetchall()
  total = 0
  num = 0
  for value in rating:
    num += value.get("review_rating")
    total += 1
  return (num/total)


def location(data):
    loc = []
    i = 0
    while i < len(data):
        cur = []
        for j in range(5):
            if i >= len(data):
                break
            cur.append(data[i])
            i += 1
        loc.append(cur)
    return loc


@app.route('/update_application_admission_cac/<id>', methods=['GET', 'POST'])
def submit_review_cac(id):
 if 'uname' in session:
    cursor = mydb.cursor(dictionary=True)
    loggedIn, fname = loginInfo()

    try:
      cursor.execute("SELECT * FROM application")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False
  
    admission_status = request.form["admission_status"]
    print(admission_status)
    

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


### Function for the page the Sysadmin can see ###
@app.route('/sysadmin', methods=['GET', 'POST'])
def sysadmin():
  if 'uname' in session:
    #connect to database
    cursor = mydb.cursor(dictionary=True)

    loggedIn, fname = loginInfo()

    try:
      cursor.execute("SELECT * FROM users")
      forms = cursor.fetchall()
      formsExist = True
    except:
      formsExist = False

    if formsExist:
      return render_template('sysadmin.html', fname = fname, forms = forms, formsExist = formsExist )
    else:
      return render_template('sysadmin.html', fname = fname, formsExist = formsExist )      
  redirect(url_for('logout'))








### Function for the adduser functionality for sysadmin ###
@app.route('/sysadmin_adduser', methods=['GET', 'POST'])
def sysadmin_adduser():
    #connect to database
  cursor = mydb.cursor(dictionary=True)

  if request.method == 'POST':
    firstName = request.form["fname"]
    lastName = request.form["lname"]
    uname = request.form["email"]
    password = request.form["pass"]
    ssn = request.form["ssn"]
    address = request.form["address"]
    role = request.form["role"]
    
   

    try:
        cursor.execute("INSERT INTO users (uname, fname, lname, password, address, ss_num, role) VALUES (%s,%s,%s,%s,%s,%s,%s)",(uname, firstName, lastName, password, address, ssn, role))
        mydb.commit()

        # cursor.execute("SELECT * FROM user")
        # forms = cursor.fetchall()
        # formsExist = True
       
        mess = 'New User Added Successfully'
        return redirect(url_for('sysadmin'))
    except:
        mydb.rollback()
        
        errmsg = 'An error occured, please try again'
    return render_template('sysadmin_adduser.html', errmsg = errmsg)
  return render_template('sysadmin_adduser.html')
  






@app.route('/reset', methods=['GET', 'POST'])
def reset():
  # delete
  cursor = mydb.cursor(dictionary=True)
  cursor.execute("DELETE FROM application")
  cursor.execute("DELETE FROM degree")
  cursor.execute("DELETE FROM gas_rating")
  cursor.execute("DELETE FROM letter_review")
  cursor.execute("DELETE FROM letter")
  cursor.execute("DELETE FROM reference")
  cursor.execute("DELETE FROM user")
  
  # insert
  # cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Coltrane','John','1111111','coltranejohn@email.com','pass','111-22-3333','applicant') ")
  # cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Davis','Miles','22222222','davismiles@email.com','pass','222-22-3333','applicant') ")
  # cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Monk','Thelonious','33333333','monkthelonious@email.com','pass','333-22-3333','applicant') ")
  # cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Getz','Stan','4444444','getzstan@email.com','pass','444-22-3333','applicant') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Lennon','John','55555555','lennonjohn@email.com','pass','111-11-1111','applicant') ")
  cursor.execute("INSERT INTO application (id,lname,fname,app_degree,semester,area_interest,experience,gre_verbal,gre_quant,gre_year,gre_adv_sub,gre_adv_score,toefl_score,toefl_year,complete) values ('55555555','Lennon','John','MS','Fall 2020','Computer Science','Worked at Microsoft','220','200','2020','200','200','150','2019','3') ")
  cursor.execute("INSERT INTO degree (uid,degree_name,gpa,major,degree_year,university) VALUES ('55555555','BS','4.0','Computer Science','2020','University of Maryland') ")
  cursor.execute("INSERT INTO reference (id,ref_fname,ref_lname,ref_email,title,affiliation) VALUES ('55555555','George','Martin','martingeorge@email.com','Professor','EMI') ")
  cursor.execute("INSERT INTO letter (id,name,message) VALUES ('55555555','George Martin','Very good student. Please admit.') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Starr','Ringo','66666666','starrringo@email.com','pass','222-11-1111','applicant') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('gs_lname', 'gs_fname', '10000000', 'gs', 'pass', '100-00-000', 'gs') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('cac_lname', 'cac_fname', '10000001', 'cac', 'pass', '100-00-001', 'cac') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Lastname', 'Narahari', '10000002', 'narahari', 'pass', '100-00-0002', 'reviewer') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Wood', 'Tim', '10000003', 'tim', 'pass', '100-00-0003', 'reviewer') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('Lastname', 'Heller', '10000004', 'heller', 'pass', '100-00-0004', 'reviewer') ")
  cursor.execute("INSERT INTO user (lname,fname,uid,email,password,ss_num,role) VALUES ('sys_lname', 'sys_fname', '00000000', 'sysadmin', 'pass', '000-00-000', 'sysadmin')" )
  mydb.commit()  
  return redirect(url_for("loginForm"))
        


  
  


app.run(host='0.0.0.0', port=8080)