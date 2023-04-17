import pynecone as pc

class User(pc.Model, table=True):
    username: str
    userid: str
    password: str


class Question(pc.Model, table=True):
    ask: str
    answer: str
    question_index: int
    classification: str
    mbti_type: str


class MbtiResult(pc.Model, table=True):
    userid: str
    target_userid: str
    username: str
    target_username: str
    mbti: str
    score: float
    question_result: str