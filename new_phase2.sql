use university;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uid            int(8) not null AUTO_INCREMENT,
    uname          varchar(50) not null UNIQUE,
    fname          varchar(32) not null,
    lname          varchar(32) not null,
    email          varchar(32) not null UNIQUE,
    password       varchar(32) not null UNIQUE,
    address        varchar(64),   
    ss_num         varchar(9) not null UNIQUE,
    role           varchar(50) not null,
    program        varchar(10),
    grad_status    varchar(50),
    thesis_status  varchar(50),
    is_alumni      varchar(50),
    thesis         LONGTEXT,
    PRIMARY KEY (uid)
);

DROP TABLE IF EXISTS application;
CREATE TABLE application (
    id             int(8) PRIMARY KEY,
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
    date           varchar(32),
    FOREIGN KEY(id) REFERENCES users(uid)
);

DROP TABLE IF EXISTS degree;

CREATE TABLE degree (
    uid             int(8), 
    degree_name     varchar(4), 
    gpa             float,
    major           varchar(32),
    degree_year     int(4),
    university      varchar(32),
    PRIMARY KEY (uid, degree_name),
    FOREIGN KEY (uid) REFERENCES users(uid)
);



DROP TABLE IF EXISTS gas_rating;

CREATE TABLE gas_rating (
    id                  int(8) PRIMARY KEY,
    review_rating       varchar(1),
    deficiency_course   varchar(40),
    reason_reject       varchar(4),
    gas_comment         varchar(40),
    advisor             varchar(32),
    decision            varchar(16),
    FOREIGN KEY (id)
                REFERENCES users(uid)
);

DROP TABLE IF EXISTS letter_review;

CREATE TABLE letter_review (
    id          int(8),
    rating      int(1),
    generic     varchar(1),
    credible    varchar(1),
    university  varchar(32),
    PRIMARY KEY (id, university),
    FOREIGN KEY (id)
                REFERENCES users(uid)
);

DROP TABLE IF EXISTS letter;

CREATE TABLE letter (
    id        int(8),
    name      varchar(32),
    message   varchar(250),
    PRIMARY KEY (id, message),
    FOREIGN KEY (id)
                REFERENCES users(uid)
    
    
);

DROP TABLE IF EXISTS reference;

CREATE TABLE reference (
    id              int(8) PRIMARY KEY,
    ref_fname       varchar(32),
    ref_lname       varchar(32),
    ref_email       varchar(32),
    title           varchar(32),
    affiliation     VARCHAR(32),

    FOREIGN KEY (id)
                REFERENCES users(uid)
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
  fid      int(8) not null,
  dname    varchar(50) not null,
  student_id int(8) not null,
  foreign key(fid) references users(uid),
  primary key (fid, student_id)
);

DROP TABLE IF EXISTS program_study;
CREATE TABLE program_study (
  univ_id      int(8) not null,
  lname        varchar(50) not null,
  fname        varchar(50) not null, 
  dname        varchar(50) not null,
  cnum         varchar(4) not null,
  c_id         char(2) not null,
  primary key(univ_id, c_id),
  foreign key(univ_id) references users(uid),
  foreign key(c_id) references course(courseid)
);

DROP TABLE IF EXISTS constants;
CREATE TABLE constants (
  cur_year    char(4) not null,
  cur_sem     varchar(20) not null
);

DROP TABLE IF EXISTS takes_course;
CREATE TABLE takes_course (
  studentid    int(8) not null,
  courseid     char(2) not null,
  semester     varchar(20) not null,
  year_taken   char(4) not null,
  grade        varchar(2) not null,
  foreign key (studentid) references users(uid) ON DELETE CASCADE,
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
  facultyid       int(8) not null,
  courseid        char(2) not null,
  semester        varchar(20) not null,
  year            char(4) not null,
  foreign key (courseid) references course_offered(courseid) ON DELETE CASCADE,
  foreign key (facultyid) references users(uid) ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS=1;

INSERT INTO users VALUES ('11111111', 'bnarahari', 'Bhagi', 'Narahari', 'bnarahari@gwu.edu', 'narahari', '123 narahari lane', '123456789', 'faculty', NULL, NULL, NULL, NULL, NULL);
INSERT INTO users VALUES ('22222222', 'gradsecretary', 'Grad', 'Secretary', 'gradsecretary@gwu.edu', 'gspass', '456 gradsec ave', '987654321', 'grad_secretary', NULL, NULL, NULL, NULL, NULL);
INSERT INTO users VALUES ('33333333', 'systemsadmin', 'Systems', 'Admin', 'systemsadmin@gwu.edu', 'sapass', '789 systems road', '457893847', 'system_admin', NULL, NULL, NULL, NULL, NULL);
INSERT INTO users VALUES ('44444444', 'pravinkhanal', 'Pravin', 'Khanal', 'pkhanal@gwu.edu', 'khanal', '3456 nepal street', '865444687', 'student', 'PHD', 'no', NULL, 'no', NULL);
INSERT INTO users VALUES ('55555555', 'joshrizika', 'Joshua', 'Rizika', 'joshrizika@gwu.edu', 'rizika', '332 josh street', '953659532', 'student', 'MS', 'no', NULL, 'no', NULL);
INSERT INTO users VALUES ('66666666', 'abdullahalm', 'Abdullah', 'Almaayoof', 'abdullah@gwu.edu', 'almaayoof', '986 aa lane', '696726849', 'student', 'PHD', 'done', NULL, 'yes', NULL);
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

INSERT INTO takes_course VALUES ('44444444','02', 'SPRING', '2022', 'IP');
INSERT INTO takes_course VALUES ('44444444','03', 'SPRING', '2022', 'IP');
INSERT INTO takes_course VALUES ('55555555','02', 'SPRING', '2022', 'IP');
INSERT INTO takes_course VALUES ('55555555','03', 'SPRING', '2022', 'IP');

INSERT INTO teaches VALUES ('11111111', '02', 'SPRING', '2022');
INSERT INTO teaches VALUES ('11111111', '03', 'SPRING', '2022');

INSERT INTO advises_on VALUES ('11111111', 'CSCI', '44444444');
INSERT INTO advises_on VALUES ('11111111', 'CSCI', '55555555');

INSERT INTO reqMScourses VALUES ('01');
INSERT INTO reqMScourses VALUES ('02');
INSERT INTO reqMScourses VALUES ('03');

INSERT INTO requirements VALUES ('PHD', '3.5', '36');
INSERT INTO requirements VALUES ('MS' , '3.0', '30');

INSERT INTO application VALUES ('44444444','Khanal','Pravin','PHD','Fall 2020','Computer Science','Worked at Microsoft','3','220','200','2020','200','200','150','2019', '5', DEFAULT, '07/04/2022');
INSERT INTO degree VALUES ('44444444','BS','4.0','Computer Science','2020','University of Maryland');
INSERT INTO reference VALUES ('44444444','George','Martin','martingeorge@email.com','Professor','EMI');
INSERT INTO letter VALUES ('44444444','George Martin','Very good student. Please admit.');
