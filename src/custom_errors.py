from fastapi import HTTPException

class MissingItemException(Exception):
    def __init__(self, message: str):
        self.message = message

class MissingUserException(Exception):
    def __init__(self, message: str):
        self.message = message
