from sqlalchemy import Column
from sqlalchemy.orm import relationship,backref
from config import Base
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
    student_id = Column(BIGINT(11),primary_key=True)
    student_code = Column(VARCHAR(13))
    student_name = Column(VARCHAR(50))
    varchar(50),
    student_nickname
    varchar(100),
    student_password
    varchar(50),
    student_headpic
    varchar(100),
    student_wxcode
    varchar(50),
    student_id_number
    varchar(20),
    student_pic
    varchar(255),
    student_state
    int(11),
    student_packageuid
    int(11),
    student_create_time
    datetime
    DEFAULT
    'CURRENT_TIMESTAMP',
    student_schooluid
    int(11)