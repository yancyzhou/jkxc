from sqlalchemy import Column
from sqlalchemy.orm import relationship,backref
from config import Base
from datetime import datetime
from sqlalchemy.dialects.mysql import BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE,DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR


class Staff(Base):
    __tablename__ = 'jkxc_staff'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    staff_id = Column(BIGINT(11),primary_key=True)
    staff_name = Column(VARCHAR(50))
    staff_code = Column(VARCHAR(13))
    staff_password = Column(VARCHAR(50))
    staff_ep_uid = Column(BIGINT(11))
    staff_state = Column(BIGINT(9))
    staff_schooluid = Column(BIGINT(11))

    def __init__(self, staff_name=None, staff_code=None, staff_password=None, staff_ep_uid=0, staff_state=0, staff_schooluid=None):
        self.staff_name = staff_name
        self.staff_code = staff_code
        self.staff_password = staff_password
        self.staff_ep_uid = staff_ep_uid
        self.staff_state = staff_state
        self.staff_schooluid = staff_schooluid


class Student(Base):
    __tablename__ = "jkxc_student"
    student_id = Column(BIGINT(11), primary_key=True)
    student_code = Column(VARCHAR(13))
    student_name = Column(VARCHAR(50))
    student_nickname = Column(VARCHAR(100))
    student_password = Column(VARCHAR(50))
    student_headpic = Column(VARCHAR(100))
    student_wxcode = Column(VARCHAR(50))
    student_id_number = Column(VARCHAR(20))
    student_pic = Column(VARCHAR(255))
    student_state = Column(BIGINT(11))
    student_packageuid = Column(BIGINT(11))
    student_create_time = Column(DATETIME(25))
    student_schooluid = Column(BIGINT(11))
    student_traineruid = Column(BIGINT(11))
    student_eqid = Column(BIGINT(11))

    def __init__(self, student_id=None, student_code=None, student_name=None, student_nickname=None, student_password=None, student_headpic=None,
                 student_wxcode=None, student_id_number=None, student_pic=None, student_state=0, student_packageuid=0,
                 student_create_time=None, student_schooluid=None, student_traineruid=None,student_eqid=0):
        self.student_id = student_id
        self.student_code = student_code
        self.student_name = student_name
        self.student_nickname = student_nickname
        self.student_password = student_password
        self.student_headpic = student_headpic
        self.student_wxcode = student_wxcode
        self.student_id_number = student_id_number
        self.student_pic = student_pic
        self.student_state = student_state
        self.student_packageuid = student_packageuid
        self.student_create_time = student_create_time
        self.student_schooluid = student_schooluid
        self.student_traineruid = student_traineruid
        self.student_eqid = student_eqid

class Trainer(Base):
    __tablename__ = 'jkxc_trainer'
    trainer_id = Column(BIGINT(11), primary_key=True)
    trainer_name = Column(VARCHAR(50))
    trainer_code = Column(VARCHAR(13))
    trainer_password = Column(VARCHAR(50))
    trainer_headpic = Column(VARCHAR(100))
    trainer_type= Column(BIGINT(9))
    trainer_rank = Column(BIGINT(9))
    trainer_state = Column(BIGINT(9))
    trainer_schooluid = Column(BIGINT(11))
    trainer_dic = Column(TEXT)
    trainer_years = Column(BIGINT(9))

    def __init__(self, trainer_id=None,trainer_name=None, trainer_code=None, trainer_password=None,trainer_headpic=None, trainer_type=0, trainer_rank=0,
                 trainer_state=0,trainer_schooluid=None, trainer_dic=None, trainer_years=0):
        self.trainer_id = trainer_id
        self.trainer_name = trainer_name
        self.trainer_code = trainer_code
        self.trainer_password = trainer_password
        self.trainer_headpic = trainer_headpic
        self.trainer_type = trainer_type
        self.trainer_rank = trainer_rank
        self.trainer_state = trainer_state
        self.trainer_schooluid = trainer_schooluid
        self.trainer_dic = trainer_dic
        self.trainer_years = trainer_years


class School(Base):
    __tablename__ = 'jkxc_school'
    school_id = Column(BIGINT(11), primary_key=True)
    school_name = Column(VARCHAR(50))
    school_address = Column(VARCHAR(255))
    school_phonenumber = Column(VARCHAR(20))

    def __init__(self, school_name=None, school_address=None, school_phonenumber=None):
        self.school_name = school_name
        self.school_address = school_address
        self.school_phonenumber = school_phonenumber


class Courses(Base):
    __tablename__ = 'jkxc_courses'
    courses_id = Column(BIGINT(11), primary_key=True,index=True)
    courses_traineruid = Column(BIGINT(11))
    courses_starttime = Column(DATETIME(25))
    courses_endtime = Column(DATETIME(25))
    courses_hour = Column(FLOAT(5))
    courses_type = Column(BIGINT(9))
    courses_state = Column(BIGINT(9))
    courses_current_number = Column(BIGINT(9),index=True)
    courses_limit_number = Column(BIGINT(9),index=True)
    courses_epuid = Column(BIGINT(11))
    courses_createtime = Column(DATETIME(25))

    def __init__(self, courses_traineruid=0, courses_starttime=None, courses_endtime=None,courses_hour=0, courses_type=0, courses_state=0,
                 courses_current_number=0,courses_limit_number=0,courses_epuid=0,courses_createtime=None):
        self.courses_traineruid = courses_traineruid
        self.courses_starttime = courses_starttime
        self.courses_endtime = courses_endtime
        self.courses_hour = courses_hour
        self.courses_type = courses_type
        self.courses_state = courses_state
        self.courses_current_number = courses_current_number
        self.courses_limit_number = courses_limit_number
        self.courses_epuid = courses_epuid
        self.courses_createtime = courses_createtime


class Exam_place(Base):
    __tablename__ = 'jkxc_exam_place'
    ep_id = Column(BIGINT(11), primary_key=True)
    ep_name = Column(VARCHAR(100))
    ep_address = Column(VARCHAR(255))
    ep_longitude = Column(VARCHAR(20))
    ep_latitude = Column(VARCHAR(20))
    ep_phonenumber = Column(VARCHAR(50))
    ep_schooluid = Column(BIGINT(11))

    def __init__(self, ep_name=None, ep_latitude=None,ep_longitude=None,ep_address=None, ep_phonenumber=None, ep_schooluid=0):
        self.ep_name = ep_name
        self.ep_address = ep_address
        self.ep_phonenumber = ep_phonenumber
        self.ep_schooluid = ep_schooluid
        self.ep_latitude = ep_latitude
        self.ep_longitude = ep_longitude


class SmLog(Base):
    __tablename__ = "jkxc_smlog"
    smlog_id = Column(BIGINT(11),primary_key=True)
    smlog_usercode = Column(VARCHAR(13))
    smlog_message = Column(VARCHAR(255))
    smlog_createtime = Column(DATETIME)
    smlog_usertype = Column(VARCHAR(9))

    def __init__(self, smlog_usercode=None, smlog_message=None, smlog_createtime=datetime.now(), smlog_usertype=0):
        self.smlog_usercode = smlog_usercode
        self.smlog_message = smlog_message
        self.smlog_createtime = smlog_createtime
        self.smlog_usertype = smlog_usertype

class Order(Base):
    __tablename__ = 'jkxc_order'
    order_id = Column(BIGINT(11), primary_key=True)
    order_money = Column(FLOAT(10))
    order_type = Column(BIGINT(9))
    order_studentuid = Column(VARCHAR(50))
    order_state = Column(BIGINT(9))
    order_wx_prepay_id = Column(VARCHAR(100))
    order_nonceStr = Column(VARCHAR(100))
    order_paySign = Column(VARCHAR(100))
    order_code = Column(VARCHAR(50))
    order_timestrampstr = Column(VARCHAR(50))
    order_packageuid = Column(BIGINT(11))
    order_createtime = Column(DATETIME(15))

    def __init__(self, order_money=0, order_type=0,nonceStr=None,timestrampstr = '',paySign=None, order_code=None,order_wx_prepay_id = None,order_studentuid=0, order_state=0, order_packageuid=0,
                 order_createtime=None):
        self.order_money = order_money
        self.order_type = order_type
        self.order_studentuid = order_studentuid
        self.order_state = order_state
        self.order_code = order_code
        self.order_wx_prepay_id = order_wx_prepay_id
        self.order_packageuid = order_packageuid
        self.order_createtime = order_createtime
        self.order_paySign = paySign
        self.order_timestrampstr = timestrampstr
        self.order_nonceStr = nonceStr


class Package(Base):
    __tablename__ = 'jkxc_package'
    package_id = Column(BIGINT(11), primary_key=True)
    package_money = Column(FLOAT(10))
    package_name = Column(VARCHAR(50))
    package_pic = Column(VARCHAR(100))
    package_describe = Column(TEXT)
    package_class_hour = Column(FLOAT(5))
    package_state = Column(BIGINT(9))
    package_schooluid = Column(BIGINT(11))
    package_detail = Column(TEXT)
    package_abstract = Column(TEXT)

    def __init__(self, package_money=0, package_name=None, package_describe=None, package_class_hour=0, package_state=0,
                 package_schooluid=0,package_detail=None,package_pic=None,package_abstract = None):
        self.package_money = package_money
        self.package_name = package_name
        self.package_describe = package_describe
        self.package_class_hour = package_class_hour
        self.package_state = package_state
        self.package_schooluid = package_schooluid
        self.package_detail = package_detail
        self.package_pic = package_pic
        self.package_abstract = package_abstract


class Student_courses(Base):
    __tablename__ = 'jkxc_student_courses'
    sc_id = Column(BIGINT(11), primary_key=True)
    sc_traineruid = Column(BIGINT(11))
    sc_coursesuid = Column(BIGINT(11))
    sc_studentuid = Column(BIGINT(11))
    sc_state = Column(BIGINT(9))
    sc_createtime = Column(DATETIME)

    def __init__(self, sc_traineruid=0, sc_coursesuid=0, sc_studentuid=0, sc_state=0, sc_createtime=datetime.now()):
        self.sc_traineruid = sc_traineruid
        self.sc_coursesuid = sc_coursesuid
        self.sc_studentuid = sc_studentuid
        self.sc_state = sc_state
        self.sc_createtime = sc_createtime


class Student_demo(Base):
    __tablename__ = 'jkxc_student_demo'
    sd_id = Column(BIGINT(11), primary_key=True)
    sd_studentuid = Column(BIGINT(11))
    sd_phone = Column(BIGINT(11))
    sd_state = Column(BIGINT(9))
    sd_createtime = Column(DATETIME)

    def __init__(self, sd_studentuid=0, sd_state=0, sd_phone=0, sd_createtime=datetime.now()):
        self.sd_studentuid = sd_studentuid
        self.sd_state = sd_state
        self.sd_phone = sd_phone
        self.sd_createtime = sd_createtime