from sqlalchemy import Column, Integer, BigInteger, String, Text, Date, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="student", nullable=False)
    register_number = Column(BigInteger, unique=True, nullable=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    url = Column(String(500), nullable=True)

    staff = relationship("Staff", back_populates="department", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="department")
    students = relationship("StudentResult", back_populates="department")


class Club(Base):
    __tablename__ = "clubs"

    club_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    parent_body = Column(String(255), nullable=True)

    events = relationship("Event", back_populates="club")


class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey("departments.department_id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    qualification = Column(String(255), nullable=True)

    department = relationship("Department", back_populates="staff")


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey("departments.department_id", ondelete="SET NULL"), nullable=True)
    club_id = Column(Integer, ForeignKey("clubs.club_id", ondelete="SET NULL"), nullable=True)
    title = Column(String(500), nullable=False)
    event_date = Column(Date, nullable=False, index=True)
    venue = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)

    department = relationship("Department", back_populates="events")
    club = relationship("Club", back_populates="events")


class StudentResult(Base):
    __tablename__ = "student_result"

    s_no = Column(Integer, nullable=True)
    register_number = Column(BigInteger, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.department_id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=True)
    python_practical = Column(Integer, nullable=True)
    tamil = Column(Integer, nullable=True)
    english = Column(Integer, nullable=True)
    python = Column(Integer, nullable=True)
    office_automation = Column(Integer, nullable=True)
    naan_mudhalvan = Column(Integer, nullable=True)
    main_total = Column(Integer, nullable=True)
    percentage = Column(Numeric(5, 2), nullable=True)
    rank = Column(Integer, nullable=True)

    department = relationship("Department", back_populates="students")
