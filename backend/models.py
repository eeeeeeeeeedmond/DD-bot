# backend/models.py
import enum
from typing import Optional, List

from sqlalchemy import Column, Enum
from sqlmodel import Field, SQLModel, Relationship, Session 

# The Enum for all possible user types in the database
class UserType(str, enum.Enum):
    ADMIN = "admin"
    PARENT = "parent"
    KID = "kid"
    LIBRARIAN = "librarian"

# Restrictive Enum for registration
class RegisterableUserType(str, enum.Enum):
    PARENT = "parent"
    LIBRARIAN = "librarian"
    KID = "kid"

#status types for librarians 
class StatusType(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# ---------------------- SCHEMAS FOR ROUTES (INTAKE) ---------------------------------
class UserRegister(SQLModel):
    username: str
    password: str
    email: str
    usertype: RegisterableUserType

class UserLogin(SQLModel):
    username: str
    password: str

class KidCreate(SQLModel):
    username: str
    password: str



# ---------------------- SCHEMAS FOR ROUTES (OUTPUT) ---------------------------------
class LoginMessage(SQLModel):
    success: bool
    message: str
    usertype: Optional[str] = None






# ------------------------ SQL TABLES ----------------------------------------
class Roles (SQLModel, table=True):
    role_id: int | None = Field(default=None, primary_key=True)
    name: UserType = Field(sa_column=Column(Enum(UserType)))

    # A Role can have many Users.
    # 'back_populates' points to the 'role' attribute in the Users model
    users: list["Users"] = Relationship(back_populates="role")

class Users(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)

    # Foreign key references the primary key of the Roles table
    role_id: int | None = Field(default=None, foreign_key="roles.role_id")

    role: Roles | None = Relationship(back_populates="users")

class LibrarianProfiles(SQLModel, table=True):
    # 1-to-1 relationship 
    user_id: int | None = Field(default=None, foreign_key="users.user_id", primary_key=True)

    status: StatusType = Field(sa_column=Column(Enum(StatusType)), default=StatusType.PENDING)


class KidProfiles(SQLModel, table=True):
    # 1-to-1 relationship
    user_id: int | None = Field(default=None, foreign_key="users.user_id", primary_key=True)

    parent_id: int = Field(foreign_key="users.user_id")







