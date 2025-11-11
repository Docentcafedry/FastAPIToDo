from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db_connection

db_connection = Annotated[Session, Depends(get_db_connection)]
