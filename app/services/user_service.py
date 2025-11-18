from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.exceptions import NotFoundException, ConflictException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_user(self, user_create: UserCreate) -> User:
        existing_user = self.db.query(User).filter(
            (User.username == user_create.username) | (User.email == user_create.email)
        ).first()
        
        if existing_user:
            if existing_user.username == user_create.username:
                raise ConflictException("Username already exists")
            if existing_user.email == user_create.email:
                raise ConflictException("Email already exists")
        
        hashed_password = self.get_password_hash(user_create.password)
        
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hashed_password
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User", user_id)
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).order_by(User.id.desc()).offset(skip).limit(limit).all()
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_user(user_id)
        
        update_data = user_update.dict(exclude_unset=True)
        
        if "username" in update_data:
            existing_user = self.db.query(User).filter(
                User.username == update_data["username"], User.id != user_id
            ).first()
            if existing_user:
                raise ConflictException("Username already exists")
        
        if "email" in update_data:
            existing_user = self.db.query(User).filter(
                User.email == update_data["email"], User.id != user_id
            ).first()
            if existing_user:
                raise ConflictException("Email already exists")
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()
        return True