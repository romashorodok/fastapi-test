
from typing import TypeVar

from .database import Base, SessionLocal

Model = TypeVar("Model", bound=Base)

class Container:

    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
