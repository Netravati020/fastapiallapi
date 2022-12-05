from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, BigInteger, table
from sqlalchemy.schema import Column
from datetime import date

from database import Base

class Employee(Base):
    __tablename__ = "employees"
    # employee_id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    #
    # Name= Column(String(50), index=True)
    # contact=Column(String(50), index=True)
    # email=Column(String(100), unique=True)
    # department= Column(String(100), index=True)
    # salary=Column(String(50), index=True)

    id=Column(Integer, primary_key=True, autoincrement=True, index=True)
    unit_code=Column(String(100), index=True)
    category_code = Column(String(100), index=True)
    employee_id = Column(String(100), unique=True, index=True)
    name = Column(String(300), index=True)
    gender = Column(String(100), index=True)
    relegion = Column(String(100), index=True)
    relegion_description = Column(String(100), index=True)
    nationality = Column(String(100), index=True)
    factory_act_flag = Column(String(100), index=True)
    designation_code = Column(String(50), index=True)
    class_of_employee = Column(String(100), index=True)
    weekly_off_day = Column(String(100), index=True)
    direct_recruity_promotee = Column(String(100), index=True)
    section_code = Column(String(50), index=True)
    dob = Column(Date(), index=True)
    initial_appointment_date = Column(Date(), index=True)
    date_of_regular = Column(Date(), index=True)
    date_of_last_increment_drawn = Column(Date(), index=True)
    date_of_medical_examination_done = Column(Date(), index=True)
    basic_pay = Column(BigInteger(), index=True)
    protected_pay = Column(BigInteger(), index=True)
    grade_pay = Column(BigInteger(), index=True)
    special_pay = Column(BigInteger(), index=True)
    family_planning_pay = Column(BigInteger(), index=True)
    telangana_incentive = Column(BigInteger(), index=True)
    graduation_increment = Column(BigInteger(), index=True)
    equalisation_allowance = Column(BigInteger(), index=True)
    special_allowance = Column(BigInteger(), index=True)
    special_allowance1 = Column(BigInteger(), index=True)
    father_spouse_name = Column(String(50), index=True)
    caste_code = Column(String(100), index=True)
    caste_description = Column(String(100), index=True)
    subcast_code = Column(String(100), index=True)
    subcast_description = Column(String(100), index=True)
    qualification = Column(String(200), index=True)
    specialization = Column(String(100), index=True)
    native_place = Column(String(100), index=True)
    native_dist_code = Column(String(50), index=True)
    native_district = Column(String(50), index=True)
    date_of_promotion_to_present_post = Column(Date(), index=True)
    date_from_working_in_present_place = Column(Date(), index=True)
    date_of_probation_declared = Column(Date(), index=True)
    date_of_confirmation = Column(Date(), index=True)
    date_of_splgrade_12yrs = Column(Date(), index=True)
    date_of_splgrade_20yrs = Column(Date(), index=True)
    opted_zone_while_appointment = Column(String(50), index=True)
    opted_region_while_appointment = Column(String(50), index=True)
    opted_division_while_appointment = Column(String(50), index=True)
    physically_handicapped_falg = Column(String(50), index=True)
    nature_of_appointment = Column(String(50), index=True)
    nature_of_promotion=Column(String(50),index=True)




class User(Base):
    __tablename__ = "usersdetail"
    employee_id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    Name= Column(String(50), index=True)
    email=Column(String(100), unique=True)
    password=Column(String(100), index=True)


