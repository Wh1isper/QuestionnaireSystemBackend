# 如果你连ORM都想看，那么代码一定出了bug
# 或者你懒到不想看DOC
# See doc https://github.com/Wh1isper/QuestionnaireSystemDoc

from db_config import *
# sqlalchemy原生用法
# from sqlalchemy import create_engine
#
# engine = create_engine(
#     'mysql+mysqldb://{username}:{password}@{host}:{port}/{db_name}?charset=utf8'.format(username=USERNAME,
#                                                                                         password=PASSWORD,
#                                                                                         db_name=DBNAME,
#                                                                                         host=HOST,
#                                                                                         port=PORT),
#     pool_recycle=3600)
#
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(engine)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, MetaData, Table
from sqlalchemy import (BigInteger, SmallInteger, DateTime, VARCHAR, CHAR, Text)

Meta = MetaData()
Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "userInfo"

    U_ID = Column("U_ID", BigInteger, primary_key=True, autoincrement=True)
    U_Email = Column("U_Email", VARCHAR(50))
    U_Name = Column("U_Name", VARCHAR(20))
    U_Sex = Column("U_Sex", SmallInteger)
    U_Birth = Column("U_Birth", DateTime)
    U_State = Column("U_State", SmallInteger)


UserInfoTable = Table('userInfo', Meta,
                      Column("U_ID", BigInteger, primary_key=True, autoincrement=True),
                      Column("U_Email", VARCHAR(50)),
                      Column("U_Name", VARCHAR(20)),
                      Column("U_Sex", SmallInteger),
                      Column("U_Birth", DateTime),
                      Column("U_State", SmallInteger)
                      )


class UserPwd(Base):
    __tablename__ = "userPwd"

    U_ID = Column("U_ID", BigInteger, ForeignKey("userInfo.U_ID"), primary_key=True)
    U_Pwd = Column("U_Pwd", CHAR(64))


UserPwdTable = Table('userPwd', Meta,
                     Column("U_ID", BigInteger, ForeignKey("userInfo.U_ID"), primary_key=True),
                     Column("U_Pwd", CHAR(64))
                     )


class UserLoginRecord(Base):
    __tablename__ = "userLoginRecord"

    U_ID = Column("U_ID", BigInteger, ForeignKey("userInfo.U_ID"), primary_key=True)
    U_Login_Date = Column("U_Login_Date", DateTime)
    U_Login_IP = Column("U_Login_IP", VARCHAR(20))


UserLoginRecordTable = Table('userLoginRecord', Meta,
                             Column("U_ID", BigInteger, ForeignKey("userInfo.U_ID"), primary_key=True),
                             Column("U_Login_Date", DateTime),
                             Column("U_Login_IP", VARCHAR(20)))


class QuestionNaireInfo(Base):
    __tablename__ = "quesNaireInfo"

    QI_ID = Column("QI_ID", BigInteger, autoincrement=True, primary_key=True)
    QI_Name = Column("QI_Name", VARCHAR(60))
    U_ID = Column("U_ID", BigInteger, ForeignKey("userInfo.U_ID"))
    QI_Creat_Date = Column("QI_Creat_Date", DateTime)
    QI_Deadline_Date = Column("QI_Deadline_Date", DateTime)
    QI_State = Column("QI_State", SmallInteger)
    QI_Limit_Type = Column("QI_Limit_Type", SmallInteger)


QuestionNaireInfoTable = Table('quesNaireInfo', Meta,
                               Column("QI_ID", BigInteger, autoincrement=True, primary_key=True),
                               Column("QI_Name", VARCHAR(60)),
                               Column("U_ID", BigInteger, ForeignKey("userInfo.U_ID")),
                               Column("QI_Creat_Date", DateTime),
                               Column("QI_Deadline_Date", DateTime),
                               Column("QI_State", SmallInteger),
                               Column("QI_Limit_Type", SmallInteger),
                               )


class QuestionNaireQuestion(Base):
    __tablename__ = "quesNaireQuestion"

    QQ_ID = Column("QQ_ID", BigInteger, primary_key=True)
    QI_ID = Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"), primary_key=True)
    QQ_Type = Column("QQ_Type", SmallInteger)
    QQ_Content = Column("QQ_Content", VARCHAR(140))


QuestionNaireQuestionTable = Table('quesNaireQuestion', Meta,
                                   Column("QQ_ID", BigInteger, primary_key=True),
                                   Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"), primary_key=True),
                                   Column("QQ_Type", SmallInteger),
                                   Column("QQ_Content", VARCHAR(140))
                                   )


class QuestionNaireOption(Base):
    __tablename__ = "quesNaireOption"

    QO_ID = Column("QO_ID", BigInteger, primary_key=True)
    QQ_ID = Column("QQ_ID", BigInteger, ForeignKey("quesNaireQuestion.QQ_ID"), primary_key=True)
    QI_ID = Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"), primary_key=True)
    QO_Type = Column("QO_Type", SmallInteger)
    QO_Content = Column("QO_Content", VARCHAR(140))


QuestionNaireOptionTable = Table('quesNaireOption', Meta,
                                 Column("QO_ID", BigInteger, primary_key=True),
                                 Column("QQ_ID", BigInteger, ForeignKey("quesNaireQuestion.QQ_ID"),
                                        primary_key=True),
                                 Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"), primary_key=True),
                                 Column("QO_Type", SmallInteger),
                                 Column("QO_Content", VARCHAR(140)),
                                 )


class QuestionNaireTemp(Base):
    __tablename__ = "quesNaireTemp"

    QI_ID = Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"), primary_key=True)
    Q_Content = Column("Q_Content", Text)


QuestionNaireTempTable = Table('quesNaireTemp', Meta,
                               Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"), primary_key=True),
                               Column("Q_Content", Text))


class AnswerOption(Base):
    __tablename__ = "answerOption"
    AO_ID = Column("AO_ID", BigInteger, primary_key=True, autoincrement=True)
    QO_ID = Column("QO_ID", BigInteger, ForeignKey("quesNaireOption.QO_ID"))
    QQ_ID = Column("QQ_ID", BigInteger, ForeignKey("quesNaireQuestion.QQ_ID"))
    QI_ID = Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"))
    QO_Type = Column("QO_Type", SmallInteger)
    AO_Content = Column("AO_Content", VARCHAR(140))


AnswerOptionTable = Table('answerOption', Meta,
                          Column("AO_ID", BigInteger, primary_key=True, autoincrement=True),
                          Column("QO_ID", BigInteger, ForeignKey("quesNaireOption.QO_ID")),
                          Column("QQ_ID", BigInteger, ForeignKey("quesNaireQuestion.QQ_ID")),
                          Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID")),
                          Column("QO_Type", SmallInteger),
                          Column("AO_Content", VARCHAR(140)),
                          )

AnswerRecorderTable = Table('answerRecord', Meta,
                            Column("QI_ID", BigInteger, ForeignKey("quesNaireInfo.QI_ID"), primary_key=True),
                            Column("Count", BigInteger),
                            )

if __name__ == '__main__':
    # 测试映射类能正常初始化
    UserInfo()
    UserPwd()
    UserLoginRecord()
    QuestionNaireInfo()
    QuestionNaireQuestion()
    QuestionNaireOption()
    QuestionNaireTemp()
    AnswerOption()
    # 测试表获取是否成功
    from sqlalchemy import create_engine  # 原生的sqlalchemy engine

    engine = create_engine(
        'mysql+mysqldb://{username}:{password}@{host}:{port}/{db_name}?charset=utf8'.format(username=USERNAME,
                                                                                            password=PASSWORD,
                                                                                            db_name=DBNAME,
                                                                                            host=HOST,
                                                                                            port=PORT),
        pool_recycle=3600)

    with engine.connect() as conn:
        for i in [UserInfoTable,
                  UserPwdTable,
                  UserLoginRecordTable,
                  QuestionNaireInfoTable,
                  QuestionNaireQuestionTable,
                  QuestionNaireOptionTable,
                  QuestionNaireTempTable,
                  AnswerOptionTable,
                  AnswerRecorderTable]:
            result = conn.execute(i.select())
            try:
                print(result.fetchall())
            except:
                pass
