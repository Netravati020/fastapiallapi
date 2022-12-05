from typing import Optional, List, Union

from pydantic import BaseModel, EmailStr


class Employee(BaseModel):

    unit_code:str
    category_code: str
    employee_id: str
    name: str
    gender: str
    relegion: str
    relegion_description: str
    nationality: str
    factory_act_flag: str
    designation_code: str
    class_of_employee: str
    weekly_off_day: str
    direct_recruity_promotee: str
    section_code: str
    dob: str
    initial_appointment_date: str
    date_of_regular: str
    date_of_last_increment_drawn: str
    date_of_medical_examination_done: str
    basic_pay: str
    protected_pay: str
    grade_pay: str
    special_pay: str
    family_planning_pay: str
    telangana_incentive: str
    graduation_increment: str
    equalisation_allowance: str
    special_allowance: str
    special_allowance1: str
    father_spouse_name: str
    caste_code: str
    caste_description: str
    subcast_code :str
    subcast_description: str
    qualification: str
    specialization: str
    native_place: str
    native_dist_code: str
    native_district: str
    date_of_promotion_to_present_post: str
    date_from_working_in_present_place: str
    date_of_probation_declared: str
    date_of_confirmation: str
    date_of_splgrade_12yrs: str
    date_of_splgrade_20yrs: str
    opted_zone_while_appointment: str
    opted_region_while_appointment: str
    opted_division_while_appointment: str
    physically_handicapped_falg: str
    nature_of_appointment: str
    nature_of_promotion: str


    class Config:
        orm_mode = True

class User(BaseModel):
    Name: str
    email:str
    password:str


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


class Emp(Employee):

    unit_code:Optional[str]=None
    category_code:Optional[str]=None
    employee_id: Optional[str]=None
    name: Optional[str]=None
    gender: Optional[str]=None
    relegion: Optional[str]=None
    relegion_description: Optional[str]=None
    nationality: Optional[str]=None
    factory_act_flag: Optional[str]=None
    designation_code: Optional[str]=None
    class_of_employee: Optional[str]=None
    weekly_off_day: Optional[str]=None
    direct_recruity_promotee: Optional[str]=None
    section_code: Optional[str]=None
    dob: Optional[str]=None
    initial_appointment_date: Optional[str]=None
    date_of_regular: Optional[str]=None
    date_of_last_increment_drawn: Optional[str]=None
    date_of_medical_examination_done: Optional[str]=None
    basic_pay: Optional[str]=None
    protected_pay: Optional[str]=None
    grade_pay: Optional[str]=None
    special_pay: Optional[str]=None
    family_planning_pay: Optional[str]=None
    telangana_incentive: Optional[str]=None
    graduation_increment: Optional[str]=None
    equalisation_allowance: Optional[str]=None
    special_allowance: Optional[str]=None
    special_allowance1: Optional[str]=None
    father_spouse_name: Optional[str]=None
    caste_code: Optional[str]=None
    caste_description: Optional[str]=None
    subcast_code :Optional[str]=None
    subcast_description: Optional[str]=None
    qualification: Optional[str]=None
    specialization: Optional[str]=None
    native_place: Optional[str]=None
    native_dist_code: Optional[str]=None
    native_district: Optional[str]=None
    date_of_promotion_to_present_post: Optional[str]=None
    date_from_working_in_present_place: Optional[str]=None
    date_of_probation_declared: Optional[str]=None
    date_of_confirmation: Optional[str]=None
    date_of_splgrade_12yrs: Optional[str]=None
    date_of_splgrade_20yrs: Optional[str]=None
    opted_zone_while_appointment: Optional[str]=None
    opted_region_while_appointment: Optional[str]=None
    opted_division_while_appointment: Optional[str]=None
    physically_handicapped_falg: Optional[str]=None
    nature_of_appointment: Optional[str]=None
    nature_of_promotion: Optional[str]=None

class EmailSchema(BaseModel):
   email: List[EmailStr]

