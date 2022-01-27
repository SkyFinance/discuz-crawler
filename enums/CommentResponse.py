from enum import Enum

class CommentResponse(Enum):
    success = 1,
    intervalLimit = 2,
    perHourLimit = 3
    unknown = 4