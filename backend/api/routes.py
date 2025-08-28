# backend/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from .. import models
from .. import database
from ..services.user_service import UserService
from ..services.parent_service import ParentService 

router = APIRouter()

# Parent & librarian signup
@router.post("/signup/")
def signup(user_data: models.UserRegister, session: Session = Depends(database.get_session)) -> bool:

    user_service = UserService(session)
    success = user_service.registerAccount(user_data)
    return success

@router.post("/login/")
def login(user_data: models.UserLogin, session: Session = Depends(database.get_session)) -> models.LoginMessage:

    user_service = UserService(session)
    login_type = user_service.login(user_data)
    return login_type

# ------------------------------- PARENTS ------------------------------
@router.post("/create-kid-account/")
def create_kid_account(kid_data: models.KidCreate, session: Session = Depends(database.get_session)) -> models.CreateKidAccountMessage:

    parent_service = ParentService(session)
    creation_data = parent_service.create_kid_account(kid_data)
    return creation_data

@router.get("/view-kid-accounts/")
def view_kids_accounts(parent_id: int, session: Session = Depends(database.get_session)) -> List[models.KidAccountDetails]:

    parent_service = ParentService(session)
    kids_accounts = parent_service.view_kids_accounts(parent_id)
    return kids_accounts