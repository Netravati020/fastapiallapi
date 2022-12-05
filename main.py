import shutil
from typing import Optional

from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, status, HTTPException, Response, Request, Form, File, UploadFile, Cookie, Header, BackgroundTasks
from fastapi import WebSocket
from fastapi.responses import HTMLResponse



authjwt_token_location: set = {"cookies"}
authjwt_cookie_csrf_protect: bool = False
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



from sqlalchemy.orm import Session

import schema
import models
import hashing
from database import engine, SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)

# Inserting new employee
@app.post('/creat', status_code=status.HTTP_201_CREATED, tags=['Employees'])
def create_emp(request: schema.Employee, db:Session=Depends(get_db)):

    e= models.Employee(

        unit_code=request.unit_code,
        category_code=request.category_code,
        employee_id=request.employee_id,
        name=request.name,
        gender=request.gender,
        relegion=request.relegion,
        relegion_description=request.relegion_description,
        nationality=request.nationality,
        factory_act_flag=request.factory_act_flag,
        designation_code=request.designation_code,
        class_of_employee=request.class_of_employee,
        weekly_off_day=request.weekly_off_day,
        direct_recruity_promotee=request.direct_recruity_promotee,
        section_code=request.section_code,
        dob=request.dob,
        initial_appointment_date=request.initial_appointment_date,
        date_of_regular=request.date_of_regular,
        date_of_last_increment_drawn=request.date_of_last_increment_drawn,
        date_of_medical_examination_done=request.date_of_medical_examination_done,
        basic_pay=request.basic_pay,
        protected_pay=request.protected_pay,
        grade_pay=request.grade_pay,
        special_pay=request.special_pay,
        family_planning_pay=request.family_planning_pay,
        telangana_incentive=request.telangana_incentive,
        graduation_increment=request.graduation_increment,
        equalisation_allowance=request.equalisation_allowance,
        special_allowance=request.special_allowance,
        special_allowance1=request.special_allowance1,
        father_spouse_name=request.father_spouse_name,
        caste_code=request.caste_code,
        caste_description=request.caste_description,
        qualification=request.qualification,
        specialization=request.specialization,
        native_place=request.native_place,
        native_dist_code=request.native_dist_code,
        native_district=request.native_district,
        date_of_promotion_to_present_post=request.date_of_promotion_to_present_post,
        date_from_working_in_present_place=request.date_from_working_in_present_place,
        date_of_probation_declared=request.date_of_probation_declared,
        date_of_confirmation=request.date_of_confirmation,
        date_of_splgrade_12yrs=request.date_of_splgrade_12yrs,
        date_of_splgrade_20yrs=request.date_of_splgrade_20yrs,
        opted_zone_while_appointment=request.opted_zone_while_appointment,
        opted_region_while_appointment=request.opted_region_while_appointment,
        opted_division_while_appointment=request.opted_division_while_appointment,
        physically_handicapped_falg=request.physically_handicapped_falg,
        nature_of_appointment=request.nature_of_appointment,
        nature_of_promotion=request.nature_of_promotion
    )

    db.add(e)
    db.commit()
    db.refresh(e)
    return e

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)


# reading all the employees detail
@app.get('/', tags=['Employees'])
def read_emps(db: Session = Depends(get_db),current_user: schema.User=Depends(get_current_user)):
    emp= db.query(models.Employee).all()
    # emp=db.execute("SELECT * FROM employees LIMIT 20 OFFSET 16")
    # return emp, create_user
    return {"data":emp[16:100], "user":current_user}



# delete perticular employee detail
@app.delete('/{employee_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Employees'])
def delete(employee_id,  db:Session=Depends(get_db)):
    emp=db.query(models.Employee).filter(models.Employee.employee_id == employee_id).delete(synchronize_session=False)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"employee not found with employee_id {employee_id}")

    db.commit()
    return'employee deleted'

# create user
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user', tags=['Userlogin'])
def create_user(request: schema.User, db:Session=Depends(get_db)):

    new_user= models.User(Name=request.Name, email=request.email, password=hashing.Hash.bcrypt(request.password))


    # if '@' not in new_user.email:
    #     return {"status":"Error provide valid email"}
    # else:
    #     return {"status":"Successfuly user Created","User":new_user}

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# user authentication
@app.post("/token", tags=['Authentication'])
async def login_access(request:OAuth2PasswordRequestForm= Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password")

    # if not Hash.verify(user.password, request.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Incorrect  password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception




# update employee details
@app.put('/{id}', tags=['Employee Update'])
def update(id, request: schema.Employee, db:Session=Depends(get_db)):
    emp=db.query(models.Employee).filter(models.Employee.employee_id == id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"employee not found with id {id}")

    emp.update(dict(request))
    db.commit()

    return 'employee updated'

# update employee details partialy
@app.patch("/emp/{id}", response_model=schema.Employee, tags=['Employee Update'])
def update_emp(id: str, emp: schema.Emp):
    with Session(engine) as session:
        db_emp = session.get(models.Employee, id)
        if not db_emp:
            raise HTTPException(status_code=404, detail="employee not found")
        emp_data = emp.dict(exclude_unset=True)
        for key, value in emp_data.items():
            setattr(db_emp, key, value)
        session.add(db_emp)
        session.commit()
        session.refresh(db_emp)
        return db_emp

@app.patch("/e/{employee_id}", response_model=schema.Employee, tags=['Employee Update'])
async def update_item(employee_id, request: schema.Emp):
    stored_item_data =models.Employee.employee_id==employee_id
    stored_item_model = schema.Emp(**dict(stored_item_data))
    update_data = request.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    models.Employee.employee_id= jsonable_encoder(updated_item)
    return update_item



# upload images or files

@app.post("/upload files", tags=['Files'])
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@app.post("/", tags=['loginform'])
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password":password}




@app.post("/session/")
def cookie(response: Response):
    response.set_cookie(key="mysession", value="1430")
    return {"message": "Wanna cookie?"}


@app.get("/get_cookie/")
def read_cookie(mysession: Optional[str] = Cookie(None)):
    return {"Cookie": mysession}


@app.get("/item/")
async def headers(user: str = Header(123)):
    return {"User-Agent": user}

from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


@app.get("/Employee/{id}", response_class=HTMLResponse)
async def employ(request: Request, id: str):
    return templates.TemplateResponse("base.html", {"request": request, "id": id})


@app.get('/login html')
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


app.mount("/static", StaticFiles(directory="static"), name="static")


# client chat
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
                alert(preventDefault())
            }
        </script>
    </body>
</html>
"""


@app.get("/websockets")
async def get():
    return HTMLResponse(html)


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

# upload files
@app.post('/upload', tags=['Files'])
def get_uploadfile(upload_file: UploadFile=File(...)):
    path=f"files/{upload_file.filename}"
    with open(path,'w+b')as buffer:
        shutil.copyfileobj(upload_file.file,buffer)
    return {
        'filename':path,
        'type': upload_file.content_type
    }
app.mount("/files", StaticFiles(directory="files"), name="files")

# download uploaded files
@app.get('/download/{name}', response_class= FileResponse, tags=['Files'])
def get_file(name:str):
    path=f"files/{name}"
    return path


# search employee with employee name
@app.get('/name', tags=['Employees'])
def search(term: Optional[str] = None, db: Session = Depends(get_db)):
    nam = db.query(models.Employee).filter(models.Employee.name.contains(term)).all()
    names = []
    for models.Employee.name in nam:
        names.append(models.Employee.name)
    return names

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# read a perticular employee detail
@app.get('/{employee_id}', status_code=status.HTTP_200_OK, tags=['Employees'])
def read_emp(employee_id,  db:Session=Depends(get_db)):
    emp= db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Employee with employee_id {employee_id} is not available")
    return (emp)

# background task managing
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}







