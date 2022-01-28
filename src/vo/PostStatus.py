from dataclasses import dataclass

@dataclass
class PostStatus:
    url:str = ""
    post:int = "1"
    title:str = ""
    isAvailable:bool = "False"
    isLocked:bool = "False"
    feiMao:str = ""
    unZip:str = "" 
    formhash:str = ""
    tid:int = "1"
    fid:int = "1"
    
