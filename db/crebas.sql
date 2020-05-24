/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2020/5/18 16:58:19                           */
/*==============================================================*/
CREATE SCHEMA IF NOT EXISTS QUESTIONNAIRESYSTEM;

USE QUESTIONNAIRESYSTEM;

DROP TABLE IF EXISTS ANSWEROPTION;

DROP TABLE IF EXISTS QUESNAIREOPTION;

DROP TABLE IF EXISTS QUESNAIREQUESTION;

DROP TABLE IF EXISTS QUESNAIRETEMP;

DROP TABLE IF EXISTS USERLOGINRECORD;

DROP TABLE IF EXISTS USERPWD;

DROP TABLE IF EXISTS QUESNAIREINFO;

DROP TABLE IF EXISTS USERINFO;

/*==============================================================*/
/* Table: AnswerOption                                          */
/*==============================================================*/
CREATE TABLE ANSWEROPTION
(
    AO_ID      BIGINT   NOT NULL AUTO_INCREMENT,
    QO_ID      BIGINT   NOT NULL,
    QQ_ID      BIGINT   NOT NULL,
    QI_ID      BIGINT   NOT NULL,
    QO_TYPE    SMALLINT NOT NULL,
    AO_CONTENT VARCHAR(140),
    PRIMARY KEY (AO_ID)
);

/*==============================================================*/
/* Table: QuesnaireInfo                                         */
/*==============================================================*/
CREATE TABLE QUESNAIREINFO
(
    QI_ID            BIGINT      NOT NULL AUTO_INCREMENT,
    QI_NAME          VARCHAR(60) NOT NULL,
    U_ID             BIGINT      NOT NULL,
    QI_CREAT_DATE    DATETIME    NOT NULL,
    QI_DEADLINE_DATE DATETIME    NOT NULL,
    QI_STATE         SMALLINT    NOT NULL,
    QI_LIMIT_TYPE    SMALLINT    NOT NULL,
    PRIMARY KEY (QI_ID)
);

/*==============================================================*/
/* Table: QuesnaireOption                                       */
/*==============================================================*/
CREATE TABLE QUESNAIREOPTION
(
    QO_ID      BIGINT   NOT NULL,
    QQ_ID      BIGINT   NOT NULL,
    QI_ID      BIGINT   NOT NULL,
    QO_TYPE    SMALLINT NOT NULL,
    QO_CONTENT VARCHAR(140),
    PRIMARY KEY (QO_ID, QQ_ID, QI_ID)
);

/*==============================================================*/
/* Table: QuesnaireQuestion                                     */
/*==============================================================*/
CREATE TABLE QUESNAIREQUESTION
(
    QQ_ID      BIGINT       NOT NULL,
    QI_ID      BIGINT       NOT NULL,
    QQ_TYPE    SMALLINT     NOT NULL,
    QQ_CONTENT VARCHAR(140) NOT NULL,
    PRIMARY KEY (QQ_ID, QI_ID)
);
/*==============================================================*/
/* Table: QuesnaireTemp                                         */
/*==============================================================*/
CREATE TABLE QUESNAIRETEMP
(
    QI_ID     BIGINT NOT NULL,
    Q_CONTENT TEXT,
    PRIMARY KEY (QI_ID)
);

/*==============================================================*/
/* Table: UserInfo                                              */
/*==============================================================*/
CREATE TABLE USERINFO
(
    U_ID    BIGINT      NOT NULL AUTO_INCREMENT,
    U_EMAIL VARCHAR(50) NOT NULL,
    U_NAME  VARCHAR(20) NOT NULL,
    U_SEX   SMALLINT,
    U_BIRTH DATETIME,
    U_STATE SMALLINT,
    PRIMARY KEY (U_ID)
);

/*==============================================================*/
/* Table: UserLoginRecord                                       */
/*==============================================================*/
CREATE TABLE USERLOGINRECORD
(
    U_ID         BIGINT NOT NULL,
    U_LOGIN_DATE DATETIME,
    U_LOGIN_IP   VARCHAR(20),
    PRIMARY KEY (U_ID)
);

/*==============================================================*/
/* Table: UserPwd                                               */
/*==============================================================*/
CREATE TABLE USERPWD
(
    U_ID  BIGINT   NOT NULL,
    U_PWD CHAR(64) NOT NULL,
    PRIMARY KEY (U_ID)
);

ALTER TABLE ANSWEROPTION
    ADD CONSTRAINT FK_AO_QO FOREIGN KEY (QO_ID, QQ_ID, QI_ID)
        REFERENCES QUESNAIREOPTION (QO_ID, QQ_ID, QI_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE QUESNAIREINFO
    ADD CONSTRAINT FK_USER_QI FOREIGN KEY (U_ID)
        REFERENCES USERINFO (U_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE QUESNAIREOPTION
    ADD CONSTRAINT FK_QI_QO FOREIGN KEY (QI_ID)
        REFERENCES QUESNAIREINFO (QI_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE QUESNAIREOPTION
    ADD CONSTRAINT FK_QQ_QO FOREIGN KEY (QQ_ID, QI_ID)
        REFERENCES QUESNAIREQUESTION (QQ_ID, QI_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE QUESNAIREQUESTION
    ADD CONSTRAINT FK_QI_QQ FOREIGN KEY (QI_ID)
        REFERENCES QUESNAIREINFO (QI_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE QUESNAIRETEMP
    ADD CONSTRAINT FK_QI_QT FOREIGN KEY (QI_ID)
        REFERENCES QUESNAIREINFO (QI_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE USERLOGINRECORD
    ADD CONSTRAINT FK_USERINFO_USERLOGINRECORD FOREIGN KEY (U_ID)
        REFERENCES USERINFO (U_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE USERPWD
    ADD CONSTRAINT FK_USERINFO_USERPWD FOREIGN KEY (U_ID)
        REFERENCES USERINFO (U_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

