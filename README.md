# Graduate-Administrative-System

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
