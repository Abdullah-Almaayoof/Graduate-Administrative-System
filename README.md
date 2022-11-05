# Graduate Administrative System

## Application Processing System

The APPS system provides an online application and admission review system for students seeking admission to the graduate programs (Masters and PhD degrees). 
A graduate applicant goes to a website and enters their information (needed to apply for admission) into the database. Applicants can check their application status online – the status is one of three (i) application incomplete (ii) application complete and under review and (iii) decision (admit or reject). 
The graduate admissions committee reviews applications and makes a decision -- Admit, Admit with Aid, or Reject. We want this review process to be automated, wherein the faculty reviewer can enter their scores into a review form

You will eventually deploy your system on our production server using MySQL and Python Flask. Remember that you will need to integrate your application with other modules in Phase 2 – so be careful about what other software you use.

User Interface Design: For the final project we will evaluate your user interface more stringently. In Phase 1 the emphasis is correctness but we expect good user interface design methods applied to your project (such as user friendly system, input form validation, etc.). 

Description of the APPS System

The APPS component provides an online application and admissions review system. The application review process requires (potentially) multiple reviewers to enter data to reach a decision. The system changes the status of an applicant to a final status of admit or reject. The final decision (of admit, admit with aid or reject) is made by one of two users (the Graduate Secretary -- GS or Chair of Admissions Committee -- CAC), and the final decision must be stored in the system. A prospective graduate student, henceforth referred to as a ‘graduate applicant’, visits the URL for the admissions/applications component. They are presented with an online application form which they proceed to fill out if they are applying to the graduate program. Once the application is complete their application is evaluated by a faculty committee and a final decision is made.

APPS Workflow:  You must implement the workflow described below. For specific data needed for this application, refer to the information below as well as your analysis of what other data may be required. 
A graduate applicant visits a specific URL and enters data (into a form) to apply for admission. When they have completed filling in all the information they submit their application.
o	The system must let them create an account/password so they can log into the system to enter their application and later to check their admission status.
o	They fill out their personal information and their academic information:
	Personal information includes address and their social security number
	Once an applicant enters their information, they will be assigned a unique student number – an eight digit number we will refer to as UID (University ID number).
•	 For Phase 1, assume the transcript is mailed (US mail) by the applicant. When these are received the GS logs into the system and manually updates the status to indicate that they have been received. 
•	The recommendation letters are submitted through an online submission – an applicant specifies the name and email of the letter writer, the system sends an email requesting the letter, and the letter writer goes to the link specified in the email and submits/writes their letter. The system should be able to determine when the letter has been submitted. For Phase 1, we only require one letter to be requested and submitted; future extensions will require three letters.
o	Note: In your implementation you do not need to actually send an email (since we don’t want to add the difficulty of setting up mail servers, avoiding spam filters, etc). Instead, your application should display the email message that it would have sent on the screen. Of course this is not how a real system would work, because normally the link that a letter writer uses to submit a review must be kept private from the applicant!
•	The application is considered to be complete when all required information has been entered by the applicant, and the transcripts and recommendation letters have been received. (Note that in Phase 1 we only require one letter.)
•	An applicant can check on the status – the different application status are specified elsewhere in this document.
•	Once an application is complete, it is ready for review for admission. The application is reviewed by a faculty admissions committee. Typically, the committee consists of 2-3 faculty. 
•	The faculty committee will be given a list of completed (but decision pending) applications. This can be in the form of a list of student numbers but we would like search features and some automation.  While this process seems okay, note that this again requires manual intervention.
o	 You should think of automating this process – for example, when a reviewer logs in they can be presented with a list of pending applications which have not been reviewed (for fairness you can sort them by date received; for simplicity you can sort them by student number or name). They can click on an entry in the list to bring up the review form for that applicant.
•	Normally several reviewers can evaluate an applicant. In phase 1, you can assume that each application is reviewed by a single reviewer. The review process starts when the reviewer brings up a student’s review form. (To add bells and whistles to your system you can consider multiple reviewers; eventually you have to build this functionality.)
o	Given a student number (UID), the system must generate the Review form – the data for the form is taken from the database based on what the applicant has entered. In practice, the reviewer also looks at the student folder at the detailed transcript, letters, etc. – in Phase 1, for simplicity and a lower score (2% penalty) on the project, you can assume that they only look at the online review form but are not able to look at the student's application!
•	 A reviewer completes his or her review by filling out the various fields in the review form, and making a recommendation. The recommendation can be one of four options and represents a ranking: (1) reject, (2) borderline (to mean they are not certain),  (3) admit without aid, and (4) admit with aid. The four numbers 1 through 4 in a sense correspond to a ranking of the applicant. If a number of reviewers were to review this applicant, one can calculate an average ranking. The reviewer can also add their comments (to make it simple assume that they can write about 40 characters in their comments) and recommend an advisor (again, you can simplify by assuming that this has to be one of the faculty in the department). When the review is complete the application is said to have been “reviewed” – but a final decision has NOT been made.
o	To get an idea of the review process and data see the sample review form data and sample reviews in the Appendix to this document.
•	 A final decision (of admit with aid, admit, or reject) is made by the committee and only the CAC (or GS) can enter this decision into the system (which should only display admit or reject to the application).  When a final decision has been made, the status of the applicant is updated and the application review process is now complete. The GS should also have authorization to enter the final decision into the system; this is a useful feature for cases when the CAC is not available.

Additional Information/Comments: There are two types of information that applicants need to fill out:
•	Personal Information: Such as name, address, social security number and other contact information considered relevant.
•	Academic Information: this includes details about their academic background.
o	Degree sought: they specify which degree program they are applying for. For this project, we assume two programs: (1) Masters (MS) program, and (2) Doctoral (PhD.) program.
o	 Prior degrees. To simplify matters we will only keep track of a maximum of 2 degrees – their Bachelors degree and their Masters degree (if applicable). The degree information should also specify the year they got their degrees, their GPA in that degree, the University/College that they received their degrees from.
o	GRE scores. They should enter their total GRE score and their scores in the two categories: Verbal, and Quantitative. GRE subject scores may also be entered if applicable. Note that GRE scores are required of Doctoral applicants but not required for students applying for the Masters program (although Masters applicants can submit GRE scores if they prefer) – thus you may not want to have this field as required for all applicants.
o	Prior Work experience: an applicant can specify in a sentence or two their past work experience.
o	Admission Date they seek: they specify which semester and year they are applying for. 
o	Transcripts -- an applicant must have their transcript sent directly to GW. This assumes that the transcript will be mailed and the receipt will be noted in the system by the GS (i.e., the GS will go into this field and update it to record that the transcript has been received.
o	Recommendation Letters -- an applicant must specify the references who will write the recommendation letters. The information supplied should be the name of the letter writer, their email address, and their title and affiliation. (So as not to generate spam, you must enter only your email address when you are testing your application  when you implement online submissions.)
o	After filling in all the information they submit their application and are henceforth an applicant entity in the system.

The academic information about the applicant is retrieved from the applicant’s entries in the on-line application process and the final status  is decided in the admission process. However, the admission review process itself creates new information –this information is created during the review process (see the sample review form). 

Note: note that some of the information that has to be entered is a selection from a menu. For example,  an applicant cannot enter "autumn 2010" in the application date -- rather their choices are limited to "Spring" or "Fall" in future semesters (up to 2 –since you cannot apply more than a year in advance of current time.

Checking on Application Status:  A graduate applicant can check on the status of their application by visiting a specific URL.
•	 They can login to the system to check their status. The system should retrieve their status – the status can be:
o	Application Incomplete – <field> materials missing
o	Application Complete and Under Review/No Decision Yet
o	Congratulations you have been admitted. The formal letter of acceptance will be mailed
o	Your application for admission has been denied
•	 Note that the status of the application is updated by the CAC (Chair of Admissions Committee) or the graduate secretary (GS). 
•	Every applicant after the admissions review will end up as an admitted applicant or a rejected applicant.

Note on planning for scalability (i.e, for future enhancements and features) and Important relevant information:  In Phase 2, you will also need to implement a number of queries/reports (specified at a later time). Keep this in mind during your table designs. Further, for the final system, there are different types of common users each with specific functionality (and authorization) that must be satisfied by the system at each phase even though some of the queries will be implemented in Phase 2. 

Sample queries that may be required later in Phase 2: In addition to the workflow process, additional queries may be submitted to the system in order to generate specific reports. Some examples include: 
•	 Search for an applicant using different fields
•	Update applicant’s academic and personal information – an applicant may choose to update their information at any time. This can be simplified by having only the GS perform this  -- but this is not an ideal solution. An applicant should be able to update their information.
•	Generating statistics (number of applications, average GRE etc.) using different search fields such as year, semester, degree program etc. Which class of users can submit this query?

Users and Roles:
Observe that there are different categories of users of the REGS system, and each type of user has specific roles and authorizations.
•	Systems administrator
o	Has access to everything and must create the different types of users
•	Grad Secretary (GS)
o	 Has complete access to applicant’s data and can update status of applicant. Note that they cannot create new users.
•	 Faculty Reviewers (including the Chair of department or Chair of Committee – CAC) 
o	They can review the student’s application – they have access to all the applicant’s information. They enter their review into a review form which is stored in the system. 
•	CAC/Chair: Is a faculty reviewer but can also update the final decision (of admit or reject).
•	Applicants: They can enter their graduate application form information, and can check on the status of their application. They are not permitted to perform any other functions.
  
  
## Advising System

The ADS (Advising System, much like DegreeMap) provides functions that help with advising and graduation requirements.

o	Each student fills out an online Form 1 which lists the courses they will take to meet graduation requirements. When the student applies for graduation, the system must check to see if all graduation requirements are met (i.e., the student has taken the courses listed on the Form 1 and met GPA and course requirements). Once they are met, and the student is cleared to graduate they are then added to an alumni list.  
o	The ADS must support graduation audit by students, faculty advisor, and Grad Secretary (GS), search for transcripts, and graduation of a student by the GS

In Phase 1, you should assume the students use a separate system (REGS) that allows them to register for courses. Thus your web interface does not need to support registering/setting grades and you can directly insert enrollment histories with courses and grades into the ADS database.

You will eventually deploy your system on our production server using MySQL and Python Flask. Remember that you will need to integrate your application with other modules in Phase 2 – so be careful about what other software you use.

User Interface Design: For the final project we will evaluate your user interface more stringently. In Phase 1 the emphasis is correctness but we expect good user interface design methods applied to your project (such as user friendly system, input form validation, etc.)

Description of the ADS System

The  ADS component provides some advising functions (for the student and advisor) including checking if degree requirements are met.

ADS workflow: You must implement the workflow below. For specific data needed for this component, refer to the information below as well as your analysis of what other data may be required.
•	Each graduate student should be able to create an account that enables them to log into the system.
•	A graduate student has personal information that identifies them. 
o	Each student has a unique university ID (UID) which is an 8 digit number.
o	The system must store the last and first name of the student, and other personal information such as address.
o	A student can be enrolled in the Masters program or the PhD program; the system must store this information.
o	A graduate student in the university is assigned a faculty advisor by the GS.
o	The system must be able to provide a login for each student in the university.
•	We assume that the student has taken some courses, and the system stores course enrollment information for each student. This information includes courses taken by the student, the semester and year taken, the final grade for the course (if completed), number of credit hours. In other words, information that is typically found on a transcript.
•	 A student must specify their entire program of study plan by filling out a Form 1 and having a faculty advisor view the form. This lists the courses that they will take to meet the Degree requirements (this is somewhat similar to the curriculum sheets that undergraduates must follow to meet their degree requirements.). A sample of a Form 1 is provided in the Appendix in this document. 
•	After completing the requirements for the degree to which they are admitted, the student formally applies for graduation by visiting the “Apply for Graduation” portion of the website, and selecting the degree to which they are applying. If you want to make a simplifying assumption for Phase 1, at risk of losing some points, then assume students are only applying for the MS degree. 
•	Since you will need to look up their enrollment information (transcript), assume that they have taken courses only from the course catalog provided in this document (in the Appendix.
o	 Assume that the valid final grades are (A, A-, B+, B, B-, C+, C, F).Courses currently in progress show up with a grade of IP (in progress).
•	 Once a student has applied for graduation, the system automatically performs an ‘audit’. Specifically the system checks to see if the student has satisfied all the degree program requirements:
o	This requires that the system check the courses the student has taken and compare them with the program requirements (both course requirements and GPA requirements) and compares them with the courses the student listed on their Form 1. (For example, if they have taken a different set of courses than listed on their Form 1 then they will not be cleared for graduation). You could simplify the process by checking for program requirements when they submit their Form 1 -- i.e., check if the courses listed on their Form 1 meet the course requirements of the MS program; thus, the application for graduation will only test if they have filed a Form 1 and if they satisfy the GPA rule.
o	If you want to simplify the project in Phase 1 (at the risk of losing 10% of the points), assume that only MS students will apply for graduation. The program requirements for both the MS and PhD are provided in the appendix. 
o	In general, program requirements for the degree (e.g., required courses for the MS degree) should be stored in the database. This will allow changes to the program requirements to be made without code modifications.
•	Once a student is cleared for graduation by passing the audit, the GS formally process their application and they “graduate”. Note that a student can be cleared for graduation but they do not actually graduate until the GS, or another authorized user,  enters this information into the system and formally clears them. 
o	The process of graduation must be automated; i.e., the GS need only check the “cleared for graduation” students and approve their graduation by clicking on some selection. (In practice the GS actually looks through their folder and transcript, and their accounts payable balance.)
•	When a student “graduates” they are removed from the Graduate student table and their information must be entered into an Alumni table. Note that only a summary of their academic information should be kept in the Alumni table.
o	In a real system, the enrollment information for a student is not removed since they may re-enroll at GWU for another degree. Thus, a graduation process would only require that their data be tagged to indicate that they have graduated with a degree while keeping all their information intact.
•	An alumni can only edit their personal information (such as email, address) and view their transcript.


Note on planning for scalability (i.e, for future enhancements and features) and Important relevant information:  In Phase 2, you will also need to implement a number of queries/reports (specified at a later time). Keep this in mind during your table designs. Further, for the final system, there are different types of common users each with specific functionality (and authorization) that must be satisfied by the system at each phase even though some of the queries will be implemented in Phase 2. 

Sample queries that may be required later: In addition to the workflow process, additional queries may be submitted to the system in order to generate specific reports. Some examples include: 
•	Generate statistics on total number of graduates, filtered by different parameters.
•	Generate list of graduating students (select by year/semester or other?)
•	Change advisor of student
•	Search utilities to find advisees, alumni etc. 

Users and Roles:
Observe that there are different categories of users of the ADS system, and each type of user has specific roles and authorizations.
•	Systems administrator
o	Has access to everything and must create the different types of user accounts
•	Grad Secretary (GS)
o	 Has complete access to current student’s data. They are responsible for assigning an advisor and for graduating a student. Note that they cannot create new users.
•	 Faculty advisors
o	These are faculty in the department and can review Form 1; for PhD students they have to approve (pass) the PhD thesis. 
o	They can view their advisees’ transcript but cannot update the transcript. This is the only access they are given.
•	Graduate Students
o	They can view their enrollment information (such as courses taken and grades) but cannot update their grades. They enter the Form1 data, and can apply for graduation.  They can update their personal information (address, email etc.) but no other information.
•	Alumni: They can log into the system and edit their personal information only.

  
## Registration System
  
The REGS system provides a course registration system. 
•	Students use your online system to register for courses. After a course is taken, instructors are able to submit grades, and a transcript can be viewed showing courses and grades.
•	The REGS must support course registration by students, grade entry by instructors and Grad Secretary (GS), and both students and GS can search for transcripts.

You will eventually deploy your system on our production server using MySQL and Python Flask. Remember that you will need to integrate your application with other modules in Phase 2 – so be careful about what other software you use.

User Interface Design: For the final project we will evaluate your user interface more stringently. In Phase 1 the emphasis is correctness but we expect good user interface design methods applied to your project (such as user friendly system, input form validation, etc.). 

Description of the REGS System

The REGS system provides an online course registration system that allows students to register (add/drop) for courses, check for their registration record (courses they have taken and grades received – similar to a transcript), and allows faculty instructors to enter grades, and grad secretary (GS) to search for transcripts and enter/change grades.

REGS workflow: You must implement the workflow below. For specific data needed for this application, refer to the information below as well as your analysis of what other data may be required.
•	Each graduate student should be able to create an account that enables them to log into the system.
•	A user registered in the system as a graduate student can enroll for graduate courses using a web registration system. 
•	A graduate student has personal information that identifies them. 
o	Each student has a unique university ID (UID) which is an 8 digit number.
o	The system must store the last and first name of the student, and other personal information such as address.
o	A student can be enrolled in the Masters program or the PhD program; the system must store this information.
o	The system must be able to provide a login for each student in the university.
•	The system stores course enrollment information for each student. This information reflects the functionality provided by the registration system; i.e., courses taken by the student, the semester and year taken, the final grade for the course (if completed), number of credit hours. In other words, information that is typically found on a transcript.
•	The web registration system enables students to enroll for courses, and faculty (or the GS) to assign grades. A student will be able to use the online registration system to register for courses, and a faculty (or the GS) can use the system only to enter the final grades. The valid final grades are (A, A-, B+, B, B-, C+, C, F).
•	At any time the GS, a faculty member, or the student can query the system for the current transcript of the student. Courses currently in progress show up with a grade of IP (in progress).
•	The registration system must store information on the courses, the faculty teaching the course, the grades (if a final grade is not assigned then a grade of IP should show up), the schedule (time and day). The course registration application must check for schedule conflicts.
o	To simplify the registration system you can assume the following:
	Each course has a department (subject), course number, title and number of credit hours associated with the course. No two departments can have the same department name and within a department the course number is unique. The schedule should include the course information above, a section number, the semester it is offered in, and the day and time. For Phase 1 you can make a simplifying assumption that each course has only one section (but your design should allow changes to allow multiple sections if requested in Phase 2). 
	The courses that are scheduled are part of a university course catalog. The course list specifies the pre-requisites for each course. The initial data for the course catalog is provided in the appendix in this document.
	To simplify the registration system, you MUST implement the schedule provided in the appendix. You can choose to populate with additional courses if you choose. The schedule specifies a day and time, and a course number as explained in the appendix. (In Phase 2 you may be required to extend this system so that an authorized user can add courses to the schedule of classes.)
	 The enrollment/registration information must store the course, the semester, the class time, day, the student identification, the instructor information, and the grade. Note that a course offering is unique when one considers the department, course number and the semester & year (and section if there are multiple sections) that it was offered in – this is what a CRN captures in Banner (but we will stick to a simpler format). For simplicity you can assume that courses are scheduled on M, T, W, R,F and each course meets once a week (like a lot of our grad courses), and the valid time slots are 3-5:30pm, 4-6:30pm and 6-8:30pm only (i.e., only three time slots). Assume that the same schedule is applied every semester (i.e., the schedule shown in the list is assumed to be in place every semester). To simplify matters, your system can allow students to take two consecutive classes that are 30 minutes apart in their end time and start time.
	Additional parameters that the registration system could require in the final product are location (room) and capacity (max class capacity). While this is not required in Phase 1, think of how your system may scale.
	For further simplification, assume that (a) there is no limit on the number of students in the class,  and (b) assume that PhD students can only register for graduate credit courses (they are numbered 6000 level). You will get extra points if you implement a more complex system.
	A student can register for courses by adding a course. The system must also support the feature of dropping a course.
	A faculty instructor teaching the course can submit grades. Once submitted the grades cannot be changed by the faculty. 

Note on planning for scalability (i.e, for future enhancements and features) and Important relevant information:  In Phase 2, you will also need to implement a number of queries/reports (specified at a later time). Keep this in mind during your table designs. Further, for the final system, there are different types of common users each with specific functionality (and authorization) that must be satisfied by the system at each phase even though some of the queries will be implemented in Phase 2. 

Sample queries that may be required later: In addition to the workflow process, additional queries may be submitted to the system in order to generate specific reports. Some examples include: 
•	Generate total list of current students (by degree or by admit year).
•	Generate  a complete transcript (list of courses and the current GPA); although you will be implementing most of the functionality for this during Phase 1.
•	For a faculty, find all courses they are teaching. 

Users and Roles:
Observe that there are different categories of users of the REGS system, and each type of user has specific roles and authorizations.
•	Systems administrator
o	Has access to everything and must create the different types of users
•	Grad Secretary (GS)
o	Has complete access to current student’s data. Note that they cannot create new users.
•	 Faculty Instructors
o	They can enter grades for the students in the courses they are teaching (i.e., courses for which they are the instructor) only once. Only the GS can override/change the grade.
•	Graduate Students
o	They can view their enrollment information (such as courses taken and grades) and can register for courses (add/drop). They can update their personal information (address, email etc.) but no other information.

