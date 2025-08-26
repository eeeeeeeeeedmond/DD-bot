# backend/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from .. import models
from .. import database
from ..services.user_service import UserService

router = APIRouter()

# Parent signup
@router.post("/parent-signup/")
def parent_signup(user_data: models.UserRegister, session: Session = Depends(database.get_session)) -> bool:

    user_service = UserService(session)
    success = user_service.registerAccount(user_data)
    return success
