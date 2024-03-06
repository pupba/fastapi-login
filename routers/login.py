from fastapi import APIRouter, Form, Depends, Request
from sqlalchemy.orm import Session
from hashlib import sha256
from typing import Union
# model
from models.login import UserIn, UserOut
# DB
from db import dbConnect, User
# Template
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix='/login',
    tags=['login'],
    responses={404: {'description': 'Not Found...'}}
)

form = {
    'ID': {"title": "ID", "description": "ID 입력"},
    'PW': {"title": "Password", "description": "Password 입력"}
}


def encryption(password: str) -> str:
    return sha256(password.encode()).hexdigest()


def connDB():
    engine, db = dbConnect("users")
    try:
        yield db
    finally:
        db.close()


@router.post('/', response_model=Union[UserOut, int])
async def login(
    request: Request,
    ID: str = Form(..., **form['ID']),
    PW: str = Form(..., **form['PW']),
    db: Session = Depends(connDB)
):
    """
    ### Login API
        - Form으로 부터 받은 ID, PW를 User 모델에 저장
        - DB 연결 후 orm을 이용해 DB에서 ID에 해당하는 레코드 검색
        - sha2로 암호화한 pw와 DB에서 가져온 해시 값과 비교하여 같으면 로그인 다를 경우 다시 로그인 화면으로.
    """
    user: UserIn = UserIn(id=ID, pw=encryption(PW))
    q = db.query(User).filter(User.id == user.id).first()
    # ID가 없는 경우
    if q == None:
        return RedirectResponse(url='/', status_code=303)
    else:
        if q.pw == user.pw:
            return UserOut(id=ID)
        else:  # PW가 틀린경우
            return RedirectResponse(url='/', status_code=303)
