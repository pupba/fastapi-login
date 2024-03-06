from pydantic import BaseModel


class UserIn(BaseModel):
    """
    ### UserIn Form
        - id : str
        - pw : sha2(str)
    """
    id: str
    pw: str


class UserOut(BaseModel):
    """
    ### UserOut Form
        - id : str
    """
    id: str
