--ctrl + k + c : 註解多行. ctrl + k + u : 取消多行註釋

DROP TABLE Classes;
DROP TABLE Students;
DROP TABLE Courses;
DROP TABLE Instructors;
------------------------------------------

CREATE TABLE    Students  (
    sid        CHAR(4)       NOT NULL ,   --please define sid as a primary key
    name       VARCHAR(12)    NOT NULL ,
    tel        VARCHAR(15) ,
    birthday   DATETIME ,
    GPA        FLOAT   

) ;

CREATE TABLE    Courses  (
    cno      CHAR(5)      NOT NULL , --please define cno as a primary key
    title     VARCHAR(30)   NOT NULL ,
    credits   INT           DEFAULT 3 
);

CREATE TABLE    Instructors  (
    eid          CHAR(4)        NOT NULL ,--please define eid as a primary key
    name         VARCHAR(12)    NOT NULL ,
    rank         VARCHAR(25) ,
    department   VARCHAR(5) 
);


CREATE TABLE    Classes  (
    eid      CHAR(4)     NOT NULL , --please define (eid, sid, cno) as a primary key
    sid      CHAR(4)     NOT NULL ,
    cno     CHAR(5)     NOT NULL ,
    time     DATETIME ,
    room     VARCHAR(8) ,
    score    FLOAT 
 
);

-----------------------------------------------------------------------------------------------------------------------------
ALTER TABLE Students 
ADD 
  constraint PK_Students primary key (sid) ; 

ALTER TABLE Instructors
ADD 
  constraint  PK_Instructors  primary key (eid) ; 

ALTER TABLE Courses
ADD 
  constraint PK_Courses primary key (cno) ; 


ALTER TABLE Classes
ADD
  constraint PK_Classes primary key (sid, eid, cno) ; 
 
-----------------------------------------------------------------------------------------------------------------------------

-- alter table classes  
-- add
  -- constraint fk_classes_instructors foreign key ( eid) references instructors ( eid  ) ,
  -- constraint fk_classes_students    foreign key ( sid ) references students  ( sid ) ,
  -- constraint fk_classes_courses     foreign key (cno) references courses  ( cno);

 -----------------------------------------------------------------------------------------------------------------------------

ALTER TABLE    Students 
ADD 
CONSTRAINT  ck_gpa CHECK ( GPA   >=  0.0 and  GPA  <=  4.0),
CONSTRAINT  ck_birthday CHECK ( birthday  >= '1999-1-1' and  birthday  <= '2024-12-31');   
-----------------------------------------------------------------------------------------------------------------------------

INSERT INTO  COURSES  VALUES ('CS101','Introduction to Computers',4);
INSERT INTO   COURSES  VALUES ('CS121','Discrete Mathematics',default);
INSERT INTO  COURSES   VALUES ('CS203','Programming',default);
INSERT INTO  COURSES   VALUES ('CS213','Object-oriented Programming',2);
INSERT INTO   COURSES   VALUES ('CS222','DBMS',default);


INSERT INTO    INSTRUCTORS   VALUES ('E001','Lily Li','Professor','CS');
INSERT INTO     INSTRUCTORS  VALUES ('E002','Cris Chang','Associate Professor','CIS');
INSERT INTO     INSTRUCTORS  VALUES ('E003','Amy Wang','Professor','MATH');

INSERT INTO Students VALUES ('S001','Ann Chen','02-22222222','2000/09/03',3.7); --陳會安
INSERT INTO Students VALUES ('S002','Yu Chiang','03-33333333','2000/02/02', 3); --江小魚
INSERT INTO Students  VALUES ('S003','Bob Chang','04-44444444','2001/03/13',3.2); --張三丰
INSERT INTO Students  VALUES ('S004','Charles Lee','05-55555555','2001/04/14',2.9); --李四方

INSERT INTO    Classes  VALUES ('E001','S001','CS101','12:00:00','180-M',85);
INSERT INTO    Classes  VALUES ('E001','S003','CS213','09:00:00','622-G',66);
INSERT INTO    Classes  VALUES ('E002','S001','CS222','13:00:00','100-M',78);
INSERT INTO    Classes  VALUES ('E002','S002','CS222','13:00:00','100-M',58);
INSERT INTO    Classes  VALUES ('E002','S003','CS121','08:00:00','221-S',75);
INSERT INTO    Classes  VALUES ('E002','S004','CS222','13:00:00','100-M',92);
INSERT INTO    Classes  VALUES ('E003','S001','CS203','10:00:00','221-S',68);
INSERT INTO    Classes  VALUES ('E003','S001','CS213','12:00:00','500-K',78);
INSERT INTO    Classes  VALUES ('E003','S002','CS203','14:00:00','327-S',85);


 

 