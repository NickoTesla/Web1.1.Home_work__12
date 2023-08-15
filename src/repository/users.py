import logging

from libgravatar import Gravatar
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserSchema


async def get_user_by_email(email: str, db: Session) -> User:
    sq = select(User).filter_by(email=email)
    result = db.execute(sq)
    user = result.scalar_one_or_none()
    logging.info(user)
    return user


async def create_user(body: UserSchema, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        logging.error(e)
    new_user = User(**body.model_dump(), avatar=avatar)  # User(username=username, email=email, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    await db.commit()