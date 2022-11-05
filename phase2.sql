use University;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uid            int(8) not null AUTO_INCREMENT,
    uname          varchar(50) not null UNIQUE,
    fname          varchar(32) not null,
    lname          varchar(32) not null,
    email          varchar(32) not null,
    password       varchar(32) not null,
    address        varchar(64),   
    ss_num         varchar(12) not null,
    role           varchar(12) not null,
    program        varchar(10),
    is_alumni      varchar(50),
    thesis_status  varchar(50),
    grad_status    varchar(50),
    thesis         LONGTEXT,
    PRIMARY KEY (uid)
);

DROP TABLE IF EXISTS application;

CREATE TABLE application (
    id             int(1) PRIMARY KEY,
    lname          varchar(32),
    fname          varchar(32),
    app_degree     varchar(3),
    semester       varchar(32),
    area_interest  varchar(32),
    experience     varchar(32),
    complete       int(1),
    gre_verbal     int(1),
    gre_quant      int(1),
    gre_year       int(1),
    gre_adv_sub    varchar(32),
    gre_adv_score  int(1),
    toefl_score    int(1),
    toefl_year     int(1),
    avg_rank       float,
    app_status     varchar(40) DEFAULT "Application Complete and Under Review",
    FOREIGN KEY (id)
                REFERENCES user(UID)
);



DROP TABLE IF EXISTS degree;

CREATE TABLE degree (
    uid             int(1), 
    degree_name     varchar(4), 
    gpa             float,
    major           varchar(32),
    degree_year     int,
    university      varchar(32),
    PRIMARY KEY (uid, degree_name),
    FOREIGN KEY (uid)
                REFERENCES user(uid)
);



DROP TABLE IF EXISTS gas_rating;

CREATE TABLE gas_rating (
    id                  int(1) PRIMARY KEY,
    review_rating       varchar(1),
    deficiency_course   varchar(40),
    reason_reject       varchar(4),
    gas_comment         varchar(40),
    advisor             varchar(32),
    decision            varchar(16),
    FOREIGN KEY (id)
                REFERENCES user(uid)
);

DROP TABLE IF EXISTS letter_review;

CREATE TABLE letter_review (
    id          int(1),
    rating      int(1),
    generic     varchar(1),
    credible    varchar(1),
    university  varchar(32),
    PRIMARY KEY (id, university),
    FOREIGN KEY (id)
                REFERENCES user(uid)
);

DROP TABLE IF EXISTS letter;

CREATE TABLE letter (
    id        int(1),
    name      varchar(32),
    message   varchar(250),
    PRIMARY KEY (id, message),
    FOREIGN KEY (id)
                REFERENCES user(uid)
    
    
);

DROP TABLE IF EXISTS reference;

CREATE TABLE reference (
    id              int(1) PRIMARY KEY,
    ref_fname       varchar(32),
    ref_lname       varchar(32),
    ref_email       varchar(32),
    title           varchar(32),
    affiliation     VARCHAR(32),

    FOREIGN KEY (id)
                REFERENCES user(uid)
);

/* ///////// Pravin's ///////// */
CREATE TABLE users (
  user_id         varchar(8) not null PRIMARY KEY,
  password        varchar(50) not null,
  type_user       varchar(50) not null,
  name            varchar(50) not null
);

DROP TABLE IF EXISTS grad_students;
CREATE TABLE grad_students (
  uid          char(8) not null,
  lname        varchar(50) not null,
  fname        varchar(50) not null,
  enrollment   varchar(50) not null,
  address      varchar(50) not null,
  phonenmbr    varchar(50) not null,
  email        varchar(50) not null,
  grad_status  varchar(50) not null,
  thesis_status varchar(50),
  is_alumni     varchar(50) not null,
  thesis        LONGTEXT,
  
  primary key (uid),


  foreign key(uid) references users(user_id)

);


DROP TABLE IF EXISTS requirements;

CREATE TABLE requirements (
  degree_type    varchar(50) not null PRIMARY KEY,
  minGPA         decimal(3,2) not null,
  mincredit      int(2) not null
);


DROP TABLE IF EXISTS reqMScourses;

CREATE TABLE reqMScourses (
  cid     varchar(50) not null PRIMARY KEY

);

DROP TABLE IF EXISTS advises_on;
CREATE TABLE advises_on (
  fid      char(8) not null,
  dname    varchar(50) not null,
  student_id varchar(50) not null,
  foreign key(fid) references users(user_id),
  primary key (fid, student_id)
);

DROP TABLE IF EXISTS transcript;
CREATE TABLE transcript(
  course_id   varchar(8) not null,
  student_id  varchar(50) not null,
  grade       varchar(2) not null, 

  foreign key(course_id) references course(course_id),
  primary key (course_id, student_id)

);

DROP TABLE IF EXISTS course;
CREATE TABLE course (
  course_id   varchar(8) not null PRIMARY KEY,
  dept        varchar(50) not null,
  course_num  varchar(4) not null,
  title       varchar(50) not null,
  credits     int(1) not null,
  pre_req     varchar(50),
  pre_req2    varchar(50)
);


DROP TABLE IF EXISTS program_study;
CREATE TABLE program_study (
  univ_id      char(8) not null,
  lname        varchar(50) not null,
  fname        varchar(50) not null, 
  dname        varchar(50) not null,
  cnum         varchar(4) not null,
  c_id         char(8) not null,
  primary key(univ_id, c_id),
  foreign key(univ_id) references grad_students(uid),
  foreign key(c_id) references course(course_id)
);
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO users VALUES ('55555555', 'aaaa', 'student', 'Paul McCartney');
INSERT INTO users VALUES ('66666666', 'bbbb', 'student', 'George Harrison');
INSERT INTO users VALUES ('11111111', 'cccc', 'student', 'Ringo Starr');
INSERT INTO users VALUES ('77777777', 'dddd', 'student', 'Eric Clapton');
INSERT INTO users VALUES ('99999999', 'ffff', 'grad_secretary', 'Virus Sahastrabuddhe');
INSERT INTO users VALUES ('22222222', 'vvvv', 'system_admin', 'Phunsukh Wangdu');
INSERT INTO users VALUES ('33333333', 'zzzz', 'faculty_advisor', 'Narahari');
INSERT INTO users VALUES ('00000000', 'xxxx', 'faculty_advisor', 'Parmer');



INSERT INTO grad_students VALUES ('55555555', 'McCartney', 'Paul', 'MS', '999 Can Drive', '7035054245', 'pm@gwu.edu', 'no', NULL, 'no', NULL);

INSERT INTO grad_students VALUES ('66666666', 'Harrison', 'George', 'MS', '777 Rancho Square', '5552036954', 'gh@gwu.edu', 'no', NULL, 'no', NULL);

INSERT INTO grad_students VALUES ('11111111', 'Starr', 'Ringo', 'PHD', '222 Raju Drive', '8881122545', 'rs@gwu.edu', 'no', NULL, 'no', NULL);

INSERT INTO grad_students VALUES ('77777777', 'Clapton', 'Eric', 'MS', '555 Farhan Plaza', '7894561232', 'ec@gwu.edu', 'done', NULL, 'yes', NULL);



INSERT INTO course VALUES ('CSCI6212','CSCI','6212','Algorithms','3','None','None');
INSERT INTO course VALUES ('CSCI6220','CSCI','6220','Machine Learning','3','None','None');
INSERT INTO course VALUES ('CSCI6221','CSCI','6221','SW Paradigms','3','None','None');
INSERT INTO course VALUES ('CSCI6232','CSCI','6232','Networks 1','3','None','None');
INSERT INTO course VALUES ('CSCI6233','CSCI','6233','Networks 2','3','CSCI6232','None');
INSERT INTO course VALUES ('CSCI6241','CSCI','6241','Database 1','3','None','None');
INSERT INTO course VALUES ('CSCI6242','CSCI','6242','Database 2','3','CSCI6241','None');
INSERT INTO course VALUES ('CSCI6246','CSCI','6246','Compilers','3','CSCI6461','CSCI6212');
INSERT INTO course VALUES ('CSCI6251','CSCI','6251','Cloud Computing','3','CSCI6461','None');
INSERT INTO course VALUES ('CSCI6254','CSCI','6254','SW Engineering','3','CSCI6221','None');
INSERT INTO course VALUES ('CSCI6260','CSCI','6260','Multimedia','3','None','None');
INSERT INTO course VALUES ('CSCI6262','CSCI','6262','Graphics 1','3','None','None');
INSERT INTO course VALUES ('CSCI6283','CSCI','6283','Security 1','3','CSCI6212','None');
INSERT INTO course VALUES ('CSCI6284','CSCI','6284','Cryptography','3','CSCI6212','None');
INSERT INTO course VALUES ('CSCI6286','CSCI','6286','Network Security','3','CSCI6283','CSCI6232');
INSERT INTO course VALUES ('CSCI6325','CSCI','6325','Algorithms 2','3','CSCI6212','None');
INSERT INTO course VALUES ('CSCI6339','CSCI','6339','Embedded Systems','3','CSCI6461','CSCI6212');
INSERT INTO course VALUES ('CSCI6384','CSCI','6384','Cryptography 2','3','CSCI6284','None');
INSERT INTO course VALUES ('CSCI6461','CSCI','6461','Computer Architecture','3','None','None');
INSERT INTO course VALUES ('ECE6241','ECE','6241','Communication Theory','3','None','None');
INSERT INTO course VALUES ('ECE6242','ECE','6242','Information Theory','2','None','None');
INSERT INTO course VALUES ('MATH6210','MATH','6210','Logic','2','None','None');


INSERT INTO transcript VALUES ('CSCI6221', '55555555', 'A');
INSERT INTO transcript VALUES ('CSCI6212', '55555555', 'A');

INSERT INTO transcript VALUES ('CSCI6461', '55555555', 'A');
INSERT INTO transcript VALUES ('CSCI6232', '55555555', 'A');
INSERT INTO transcript VALUES ('CSCI6233', '55555555', 'A');
INSERT INTO transcript VALUES ('CSCI6241', '55555555', 'B');
INSERT INTO transcript VALUES ('CSCI6246', '55555555', 'B');
INSERT INTO transcript VALUES ('CSCI6262', '55555555', 'B');
INSERT INTO transcript VALUES ('CSCI6283', '55555555', 'B');
INSERT INTO transcript VALUES ('CSCI6242', '55555555', 'B');

INSERT INTO transcript VALUES ('ECE6242', '66666666', 'C');
INSERT INTO transcript VALUES ('CSCI6221', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6461', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6212', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6232', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6233', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6241', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6242', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6283', '66666666', 'B');
INSERT INTO transcript VALUES ('CSCI6284', '66666666', 'B');

INSERT INTO transcript VALUES ('CSCI6221', '77777777', 'B');
INSERT INTO transcript VALUES ('CSCI6212', '77777777', 'B');
INSERT INTO transcript VALUES ('CSCI6461', '77777777', 'B');
INSERT INTO transcript VALUES ('CSCI6232', '77777777', 'B');
INSERT INTO transcript VALUES ('CSCI6233', '77777777', 'B');
INSERT INTO transcript VALUES ('CSCI6241', '77777777', 'B');
INSERT INTO transcript VALUES ('CSCI6242', '77777777', 'B');
INSERT INTO transcript VALUES ('CSCI6283', '77777777', 'A');
INSERT INTO transcript VALUES ('CSCI6284', '77777777', 'A');
INSERT INTO transcript VALUES ('CSCI6286', '77777777', 'A');



INSERT INTO transcript VALUES ('CSCI6384', '11111111','A');
INSERT INTO transcript VALUES ('CSCI6339', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6325', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6286', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6284', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6283', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6262', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6254', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6251', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6260', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6221', '11111111', 'A');
INSERT INTO transcript VALUES ('CSCI6461', '11111111', 'A');


INSERT INTO advises_on VALUES ('00000000', 'CSCI', '66666666');
INSERT INTO advises_on VALUES ('00000000', 'CSCI', '11111111');

INSERT INTO advises_on VALUES ('33333333', 'CSCI', '55555555');



INSERT INTO reqMScourses VALUES ('CSCI6212');
INSERT INTO reqMScourses VALUES ('CSCI6221');
INSERT INTO reqMScourses VALUES ('CSCI6461');


INSERT INTO requirements VALUES ('PHD', '3.5', '36');
INSERT INTO requirements VALUES ('MS' , '3.0', '30');

/* ///////// Josh's ///////// */
DROP TABLE IF EXISTS constants;
CREATE TABLE constants (
  cur_year    char(4) not null,
  cur_sem     varchar(20) not null
);


DROP TABLE IF EXISTS student;
CREATE TABLE student (
  studentid   char(8) not null PRIMARY KEY,
  uname       varchar(50) not null UNIQUE,
  password    varchar(50) not null UNIQUE,
  email       varchar(50) not null UNIQUE,
  fname       varchar(20) not null,
  minit       char(1),
  lname       varchar(20) not null,
  address     varchar(50) not null,
  
);

DROP TABLE IF EXISTS faculty;
CREATE TABLE faculty (
  facultyid   char(8) not null PRIMARY KEY,
  uname       varchar(50) not null UNIQUE,
  password    varchar(50) not null UNIQUE,
  email       varchar(50) not null UNIQUE,
  fname       varchar(20) not null,
  minit       char(1),
  lname       varchar(20) not null,
  address     varchar(50) not null,
  facultytype varchar(20) not null
);

DROP TABLE IF EXISTS takes_course;
CREATE TABLE takes_course (
  studentid    char(8) not null,
  courseid     char(2) not null,
  semester     varchar(20) not null,
  year_taken   char(4) not null,
  grade        varchar(2) not null,
  foreign key (studentid) references student(studentid) ON DELETE CASCADE,
  foreign key (courseid) references course(courseid) ON DELETE CASCADE
);
  
DROP TABLE IF EXISTS course_offered;
CREATE TABLE course_offered (
  courseid       char(2) not null PRIMARY KEY,
  day            char(1) not null,
  start_time     int(4) not null,
  end_time       int(4) not null,
  foreign key (courseid) references course(courseid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS course;
CREATE TABLE course (
  courseid       char(2) not null PRIMARY KEY,
  dept           varchar(50) not null,
  cnum           char(4) not null,
  title          varchar(50) not null,
  credits        int(1) not null
);

DROP TABLE IF EXISTS prereq_of;
CREATE TABLE prereq_of (
  courseid       char(2) not null,
  pr_cid         char(2) not null,
  foreign key (courseid) references course(courseid) ON DELETE CASCADE,
  foreign key (pr_cid) references course(courseid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS teaches;
CREATE TABLE teaches (
  facultyid       char(8) not null,
  courseid        char(2) not null,
  semester        varchar(20) not null,
  year            char(4) not null,
  foreign key (courseid) references course_offered(courseid) ON DELETE CASCADE,
  foreign key (facultyid) references faculty(facultyid) ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS=1;

INSERT INTO constants VALUES ('2022', 'SPRING');

-- DEMO START STATE --

INSERT INTO course VALUES ('01', 'CSCI', '6221', 'SW Paradigms', 3);
INSERT INTO course VALUES ('02', 'CSCI', '6461', 'Computer Architecture', 3);
INSERT INTO course VALUES ('03', 'CSCI', '6212', 'Algorithms', 3);
INSERT INTO course VALUES ('04', 'CSCI', '6220', 'Machine Learning', 3);
INSERT INTO course VALUES ('05', 'CSCI', '6232', 'Networks 1', 3);
INSERT INTO course VALUES ('06', 'CSCI', '6233', 'Networks 2', 3);
INSERT INTO course VALUES ('07', 'CSCI', '6241', 'Database 1', 3);
INSERT INTO course VALUES ('08', 'CSCI', '6242', 'Database 2', 3);
INSERT INTO course VALUES ('09', 'CSCI', '6246', 'Compilers', 3);
INSERT INTO course VALUES ('10', 'CSCI', '6260', 'Multimedia', 3);
INSERT INTO course VALUES ('11', 'CSCI', '6251', 'Cloud Computing', 3);
INSERT INTO course VALUES ('13', 'CSCI', '6262', 'Graphics 1', 3);
INSERT INTO course VALUES ('14', 'CSCI', '6283', 'Security 1', 3);
INSERT INTO course VALUES ('15', 'CSCI', '6284', 'Cryptography', 3);
INSERT INTO course VALUES ('16', 'CSCI', '6286', 'Network Security', 3);
INSERT INTO course VALUES ('17', 'CSCI', '6325', 'Algorithms 2', 3);
INSERT INTO course VALUES ('18', 'CSCI', '6339', 'Embedded Systems', 3);
INSERT INTO course VALUES ('19', 'CSCI', '6384', 'Cryptography 2', 3);
INSERT INTO course VALUES ('20', 'ECE', '6241', 'Communication Theory', 3);
INSERT INTO course VALUES ('21', 'ECE', '6242', 'Information Theory', 2);
INSERT INTO course VALUES ('22', 'MATH', '6210', 'Logic', 2);


INSERT INTO prereq_of VALUES ('06', '05');
INSERT INTO prereq_of VALUES ('08', '07');
INSERT INTO prereq_of VALUES ('09', '02');
INSERT INTO prereq_of VALUES ('09', '03');
INSERT INTO prereq_of VALUES ('11', '02');
INSERT INTO prereq_of VALUES ('14', '03');
INSERT INTO prereq_of VALUES ('15', '03');
INSERT INTO prereq_of VALUES ('16', '14');
INSERT INTO prereq_of VALUES ('16', '05');
INSERT INTO prereq_of VALUES ('17', '03');
INSERT INTO prereq_of VALUES ('18', '02');
INSERT INTO prereq_of VALUES ('18', '03');
INSERT INTO prereq_of VALUES ('19', '15');


INSERT INTO course_offered VALUES ('01', 'M', 1500, 1730);
INSERT INTO course_offered VALUES ('02', 'T', 1500, 1730);
INSERT INTO course_offered VALUES ('03', 'W', 1500, 1730);
INSERT INTO course_offered VALUES ('05', 'M', 1800, 2030);
INSERT INTO course_offered VALUES ('06', 'T', 1800, 2030);
INSERT INTO course_offered VALUES ('07', 'W', 1800, 2030);
INSERT INTO course_offered VALUES ('08', 'R', 1800, 2030);
INSERT INTO course_offered VALUES ('09', 'T', 1500, 1730);
INSERT INTO course_offered VALUES ('11', 'M', 1800, 2030);
INSERT INTO course_offered VALUES ('10', 'R', 1800, 2030);
INSERT INTO course_offered VALUES ('13', 'W', 1800, 2030);
INSERT INTO course_offered VALUES ('14', 'T', 1800, 2030);
INSERT INTO course_offered VALUES ('15', 'M', 1800, 2030);
INSERT INTO course_offered VALUES ('16', 'W', 1800, 2030);
INSERT INTO course_offered VALUES ('19', 'W', 1500, 1730);
INSERT INTO course_offered VALUES ('20', 'M', 1800, 2030);
INSERT INTO course_offered VALUES ('21', 'T', 1800, 2030);
INSERT INTO course_offered VALUES ('22', 'W', 1800, 2030);
INSERT INTO course_offered VALUES ('18', 'R', 1600, 1830);

INSERT INTO student VALUES ('88888888', 'bholiday', 'holiday', 'bholiday@school.edu', 'Billie', '', 'Holiday', '123 Main St', 'MS');
INSERT INTO student VALUES ('99999999', 'dkrall', 'krall', 'dkrall@school.edu', 'Diana', '', 'Krall', '456 Main St', 'MS');

INSERT INTO takes_course VALUES ('88888888','02', 'SPRING', '2022', 'IP');
INSERT INTO takes_course VALUES ('99999999','02', 'SPRING', '2022', 'IP');
INSERT INTO takes_course VALUES ('88888888','03', 'SPRING', '2022', 'IP');

INSERT INTO faculty VALUES ('00000012', 'bnarahari', 'narahari', 'bhagi@school.com', 'Bhagirath', '', 'Narahari', '789 Main St', 'Instructor');
INSERT INTO faculty VALUES ('00000013', 'hchoi', 'choi', 'hchoi@school.com', 'Hyeong-Ah', '', 'Choi', '101 Main St', 'Instructor');
INSERT INTO faculty VALUES ('00000016', 'gradsecretary', 'gspass', 'grad@secretary.com', 'Grad', '', 'Secretary', '567 GS Road', 'GS');
INSERT INTO faculty VALUES ('00000017', 'systemsadmin', 'sapass', 'systems@administrator.com', 'System', '', 'Admin', '3784 SA Drive', 'SA');

INSERT INTO teaches VALUES ('00000012', '02', 'SPRING', '2022');
INSERT INTO teaches VALUES ('00000013', '03', 'SPRING', '2022');

INSERT INTO users VALUES ('55555555', 'paulm', 'pass', 'paul@dot.com', 'Paul', 'McCartney', null, null, null, null, null, null, null, null, );

INSERT INTO takes_course VALUES ('55555555', '01', 'FALL', '2021', 'A');
INSERT INTO takes_course VALUES ('55555555', '03',  'FALL', '2021', 'A');
INSERT INTO takes_course VALUES ('55555555', '02',  'FALL', '2021', 'A');
INSERT INTO takes_course VALUES ('55555555', '05',  'FALL', '2021', 'A');
INSERT INTO takes_course VALUES ('55555555', '06',  'FALL', '2021', 'A');
INSERT INTO takes_course VALUES ('55555555', '07',  'SPRING', '2022', 'B');
INSERT INTO takes_course VALUES ('55555555', '09',  'SPRING', '2022', 'B');
INSERT INTO takes_course VALUES ('55555555', '13',  'SPRING', '2022', 'B');
INSERT INTO takes_course VALUES ('55555555', '14',  'SPRING', '2022', 'B');
INSERT INTO takes_course VALUES ('55555555', '08',  'SPRING', '2022', 'B');

-- TEST SQL --


-- INSERT INTO student VALUES ('00000001', 'libbonati', 'joshisstupid', 'josielibbon@libbon.gov', 'Josie', 'S', 'Libbon', '8419 Vermillion Circle', 'PhD');
-- INSERT INTO student VALUES ('00000002', 'khalushka', 'joshisverystupid', 'khalushka@joshisfuckingstupid.com', 'Kate', 'R', 'Halushka', '123456 Main Street', 'PhD');
-- INSERT INTO student VALUES ('00000003', 'joshrizika', 'joshiscool', 'joshrizika@amongus.gov', 'Joshua', 'R', 'Rizika', '267 Eliot Street', 'Masters');
-- INSERT INTO student VALUES ('00000004', 'kushdaddy', 'hotdoglover', 'sam@sam.sam', 'Samantha', 'N', 'Kusner', '1500 Combustion Lane', 'Masters');
-- INSERT INTO student VALUES ('00000005', 'colinranck', 'ilovefood', 'colin@food.com', 'Colin', 'M', 'Ranck', '123 Sesame Street', 'PhD');
-- INSERT INTO student VALUES ('00000006', 'ryahcarp', 'iloveflowers', 'ryah@yourmomshouse.com', 'Ryah', 'M', 'Carpenter', '1010 Sillygoose Lane', 'Masters');
-- INSERT INTO student VALUES ('00000007', 'sarjags', 'winniethepooh', 'sarahjags@hotmail.com', 'Sarah', 'M', 'Jagerdeo', '19345 Goobertown Circle', 'Masters');
-- INSERT INTO student VALUES ('00000008', 'yacobroedel', 'devoutjew', 'jacob@longisland.com', 'Jacob', 'J', 'Roedel', '1 Long Island Road', 'PhD');
-- INSERT INTO student VALUES ('00000009', 'jonnyboy', 'baskeballboy', 'jonathan@please.com', 'Jonathan', 'D', 'Nguyen', '101010 Johnny Road', 'Masters');
-- INSERT INTO student VALUES ('00000010', 'praviner', 'itsnoteventhatcold', 'praviner@pravin.nepal', 'Pravin', '', 'Khanal', '101 Pravintown Road', 'PhD');

-- INSERT INTO faculty VALUES ('00000011', 'timwood', 'itstimothy', 'timwood@timwood.com', 'Timothy', '', 'Wood', '101 Timwood Road', 'Instructor');
-- INSERT INTO faculty VALUES ('00000012', 'bnarahari', 'itsbhagirath', 'bhagi@bhagi.com', 'Bhagirath', '', 'Narahari', '234 Narahari Lane', 'Instructor');
-- INSERT INTO faculty VALUES ('00000013', 'gpalmer', 'itsgabriel', 'gabe@palmer.com', 'Gabriel', '', 'Palmer', '101 Gabetown Drive', 'Instructor');
-- INSERT INTO faculty VALUES ('00000014', 'pvora', 'itspoorvi', 'poorvi@vora.com', 'Poorvi', 'L', 'Vora', '101 Vora Street', 'Instructor');
-- INSERT INTO faculty VALUES ('00000015', 'testprof', 'testpass', 'professor@gwu.org', 'Prof', '', 'Essor', '111 Professor Lane', 'Instructor');
-- INSERT INTO faculty VALUES ('00000016', 'gradsecretary', 'gspass', 'grad@secretary.com', 'Grad', '', 'Secretary', '567 GS Road', 'GS');
-- INSERT INTO faculty VALUES ('00000017', 'systemsadmin', 'sapass', 'systems@administrator.com', 'System', '', 'Admin', '3784 SA Drive', 'SA');

-- INSERT INTO teaches VALUES ('00000011', '01', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000014', '02', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000011', '03', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000012', '05', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000014', '06', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000012', '07', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000014', '08', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000013', '09', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000015', '11', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000011', '10', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000013', '13', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000015', '14', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000012', '15', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000012', '16', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000014', '19', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000015', '20', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000015', '21', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000011', '22', 'SPRING', '2022');
-- INSERT INTO teaches VALUES ('00000012', '18', 'SPRING', '2022');


-- INSERT INTO takes_course VALUES ('00000001','15', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000001','18', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000001','22', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000001','03', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000002','21', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000002','15', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000002','18', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000002','05', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000003','14', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000003','05', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000003','01', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000003','09', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000004','16', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000004','11', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000004','03', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000004','20', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000005','21', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000005','19', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000005','16', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000005','05', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000006','01', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000006','08', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000006','06', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000006','14', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000007','22', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000007','10', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000007','06', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000007','19', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000008','22', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000008','09', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000008','20', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000008','10', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000009','07', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000009','11', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000009','13', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000009','02', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000010','13', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000010','07', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000010','02', 'SPRING', '2022', 'IP');
-- INSERT INTO takes_course VALUES ('00000010','08', 'SPRING', '2022', 'IP');

-- INSERT INTO takes_course VALUES ('00000001','01', 'FALL', '2020', 'A');
-- INSERT INTO takes_course VALUES ('00000001','02', 'SPRING', '2020', 'A');
-- INSERT INTO takes_course VALUES ('00000001','03', 'FALL', '2019', 'B');
-- INSERT INTO takes_course VALUES ('00000001','04', 'FALL', '2020', 'B+');


SET FOREIGN_KEY_CHECKS = 1;