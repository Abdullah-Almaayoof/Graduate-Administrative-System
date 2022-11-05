-- CREATE DATABASE test1
--     DEFAULT CHARACTER SET = 'utf8mb4';


use University;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    lname          varchar(32) not null,
    fname          varchar(32) not null,
    uid            int(8) not null AUTO_INCREMENT,
    email          varchar(32) not null,
    password       varchar(32) not null,
    address        varchar(64),   
    ss_num         varchar(12) not null,
    role           varchar(12) not null,
    PRIMARY KEY (uid, email)
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


SET FOREIGN_KEY_CHECKS = 1;



