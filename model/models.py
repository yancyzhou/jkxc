from sqlalchemy import Column
from sqlalchemy.orm import relationship,backref
from config import Base
from datetime import datetime
from sqlalchemy.dialects.mysql import BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE,DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
class User(Base):
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

    def __init__(self, staff_name=None, staff_code=None, staff_password = None, staff_ep_uid = 0, staff_state = 0,staff_schooluid = None):
        self.staff_name = staff_name
        self.staff_code = staff_code
        self.staff_password = staff_password
        self.staff_ep_uid = staff_ep_uid
        self.staff_state = staff_state
        self.staff_schooluid = staff_schooluid


class Student(Base):
    __tablename__ = "jkxc_student"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    student_id = Column(BIGINT(11),primary_key=True)
    student_code = Column(VARCHAR(13))
    student_name = Column(VARCHAR(50))
    student_nickname = Column(VARCHAR(100))
    student_password = Column(VARCHAR(50))
    student_headpic = Column(VARCHAR(100))
    student_wxcode = Column(VARCHAR(50))
    student_id_number = Column(VARCHAR(20))
    student_pic = Column(VARCHAR(255))
    student_state = Column(BIGINT(11))
    student_packageuid = Column(INTEGER(11))
    student_create_time = Column(DATETIME,default='CURRENT_TIMESTAMP')
    student_schooluid = Column(INTEGER(11))

    def __init__(self,student_code=None,student_name=None,student_nickname = None,student_password = None,student_headpic = None ,student_wxcode = '',student_id_number= None,student_pic = None,student_state = 0,student_packageuid = None,student_create_time = datetime.now(),student_schooluid = None):
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