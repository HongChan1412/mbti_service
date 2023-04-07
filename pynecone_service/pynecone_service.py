import pynecone as pc
from .helpers import navbar
from typing import List
import bcrypt
import os
import re

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


class State(pc.State):
    userid: str = ""
    username_set: str = ""
    username: str = ""
    password: str = ""
    confirm_password: str = ""
    logged_in: bool = False

    question_idx: int = 1
    question_progress: float = round(100 / 12 * question_idx, 2)

    question_answer: dict = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "", 11: "", 12: ""}
    question_data: list = []

    result_mbti: str = ""
    result_score: float = 0.0


    mbti_data: dict = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}


    #############################################
    target_userid: str = ""
    target_data: dict = {"user": {"userid": "", "username": "", "target_userid": "", "target_username": ""}, "info": {"mbti": "", "score": 0.0, "question_result": {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "", 11: "", 12: ""}}}

    exist_user: bool = False
    exist_result: bool = False
    exist_answer: bool = False

    target_results: List[MbtiResult] = []


    def login(self):
        with pc.session() as session:
            user = session.query(User).where(User.userid == self.userid).first()
            if user and bcrypt.checkpw(self.password.encode('utf-8'), user.password.encode('utf-8')):
                self.logged_in = True
                self.username = user.username
                return self.load_user(self.userid)

            else:
                return pc.window_alert("아이디, 비밀번호를 확인해주세요")

    def logout(self):
        self.reset()
        return pc.redirect("/")

    def signup(self):
        with pc.session() as session:
            if not (self.username_set and self.userid and self.password):
                return pc.window_alert("이름, 아이디, 비밀번호를 확인해주세요")
            exist_user = session.query(User).where(User.userid == self.userid).first()
            if exist_user:
                return pc.window_alert("이미 존재하는 아이디입니다")
            if self.password == self.confirm_password:
                password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user = User(userid=self.userid, password=password, username=self.username_set)
                session.add(user)
                session.commit()
            else:
                return pc.window_alert("비밀번호가 일치하지 않습니다")
        return pc.redirect("/")

    def set_username(self, username):
        self.username_set = username.strip()

    def set_userid(self, userid):
        self.userid = userid.strip()

    def set_password(self, password):
        self.password = password.strip()

    def set_confirm_password(self, confirm_password):
        self.confirm_password = confirm_password.strip()

    def set_target_userid(self, target_userid):
        self.target_userid = target_userid.strip()

    @pc.var
    def alert_password(self):
        if len(self.password) > 7:
            return False
        else:
            return True

    @pc.var
    def alert_confirm_password(self):
        if self.password == self.confirm_password:
            return False
        else:
            return True

    @pc.var
    def alert_id(self):
        if re.search(r'^[A-Za-z0-9_]{4,20}$', self.userid):
            return False
        else:
            return True

    def load_user(self, target_userid=None):
        if not target_userid:
            self.target_userid = self.get_query_params().get("user")
        else:
            self.target_userid = target_userid
        self.target_userid = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", self.target_userid)
        self.target_data = {"user": {"userid": self.userid, "username": "", "target_userid": self.target_userid, "target_username": ""}, "info": {"mbti": "", "score": 0.0, "question_result": {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "", 11: "", 12: ""}}}
        self.exist_user = False
        self.exist_result = False
        self.exist_answer = False
        self.target_results = []
        with pc.session() as session:
            exist_user = session.query(User).where(User.userid == self.target_userid).first()
            if exist_user:
                self.exist_user = True
                self.target_data["user"] = {"userid": self.userid, "username": self.username, "target_userid": exist_user.userid, "target_username": exist_user.username}
                self.target_results = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid, MbtiResult.userid != self.target_userid).all()
                exist_result = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid).all()
                if exist_result:
                    self.exist_result = True
                    exist_answer = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid, MbtiResult.userid == self.userid).first()
                    if exist_answer:
                        self.exist_answer = True
                        self.target_data["user"] = {"userid": exist_answer.userid, "target_userid": exist_answer.target_userid, "username": exist_answer.username, "target_username": exist_answer.target_username}
                        self.target_data["info"] = {"mbti": exist_answer.mbti, "score": exist_answer.score, "question_result": eval(exist_answer.question_result)}
        self.target_userid = ""
        return pc.redirect("/" + self.target_data["user"]["target_userid"])

    def load_question(self):
        with pc.session() as session:
            self.question_data = session.query(Question).all()
            return pc.redirect("/question")

    def next_question(self):
        if self.question_idx == 12:
            return self.get_mbti()
        self.question_idx += 1
        self.question_progress = round(100 / 12 * self.question_idx, 2)

    def prev_question(self):
        if self.question_idx == 1:
            return pc.redirect(f"/{self.userid}")
        self.question_idx -= 1
        self.question_progress = round(100 / 12 * self.question_idx, 2)

    @pc.var
    def get_ask(self):
        if self.question_data:
            return self.question_data[(self.question_idx - 1) * 2].ask

    @pc.var
    def get_answer_1(self):
        if self.question_data:
            return self.question_data[(self.question_idx - 1) * 2].answer

    @pc.var
    def get_answer_2(self):
        if self.question_data:
            return self.question_data[(self.question_idx - 1) * 2 + 1].answer

    @pc.var
    def get_color1(self):
        if self.target_data["info"]["question_result"][self.question_idx] in ["E", "S", "T", "J"]:
            return "rgb(29 161 242)"

    @pc.var
    def get_color2(self):
        if self.target_data["info"]["question_result"][self.question_idx] in ["I", "N", "F", "P"]:
            return "rgb(29 161 242)"

    def change_answer(self, question_answer):
        self.target_data["info"]["question_result"][self.question_idx] = self.question_data[(self.question_idx - 1) * 2 + question_answer].mbti_type

        if self.question_idx == 12:
            return self.get_mbti()
        self.question_idx += 1
        self.question_progress = round(100 / 12 * self.question_idx)

    def get_mbti(self):
        users = self.target_data["user"]
        info = self.target_data["info"]
        info["mbti"], info["score"] = "", 0.0
        for k, v in info["question_result"].items():
            if not v:
                return pc.window_alert(f"{k}번 질문의 답변을 확인해주세요")
            self.mbti_data[v] += 1
        if self.mbti_data["E"] > self.mbti_data["I"]: info["mbti"] += "E"
        else: info["mbti"] += "I"
        if self.mbti_data["S"] > self.mbti_data["N"]: info["mbti"] += "S"
        else: info["mbti"] += "N"
        if self.mbti_data["T"] > self.mbti_data["F"]: info["mbti"] += "T"
        else: info["mbti"] += "F"
        if self.mbti_data["J"] > self.mbti_data["P"]: info["mbti"] += "J"
        else: info["mbti"] += "P"

        with pc.session() as session:
            target_answer = session.query(MbtiResult).where(MbtiResult.userid == users["userid"], MbtiResult.target_userid == users["target_userid"]).first()
            if users["userid"] == users["target_userid"]:
                info["score"] = 100.0
            else:
                for num, i in enumerate(eval(target_answer.question_result).items()):
                    if info["question_result"][num+1] == i[1]:
                        info["score"] += 100 / 12
            if target_answer:
                session.query(MbtiResult).where(MbtiResult.userid == self.userid, MbtiResult.target_userid == users["target_userid"]).update({"userid": users["userid"], "target_userid": users["target_userid"], "username": users["username"], "target_username": users["target_username"], "mbti": info["mbti"], "score": round(info["score"], 2), "question_result": str(info["question_result"])})
            else:
                session.add(MbtiResult(userid=users["userid"], target_userid=users["target_userid"], username=users["username"], target_username=users["target_username"], mbti=info["mbti"], score=round(info["score"], 2), question_result=str(info["question_result"])))
            session.commit()

        self.question_idx = 1
        self.question_progress = round(100 / 12 * self.question_idx, 2)
        self.mbti_data = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        return pc.redirect("/result")


    @pc.var
    def get_target_username(self):
        return self.target_data["user"]["target_username"]

    @pc.var
    def get_target_mbti(self):
        return self.target_data["info"]["mbti"]

    @pc.var
    def get_target_score(self):
        return self.target_data["info"]["score"]


    @pc.var
    def judge_mypage(self):
        if self.target_data["user"]["userid"] == self.target_data["user"]["target_userid"]:
            return True
        return False

    @pc.var
    def judge_signup(self) -> bool:
        if (len(self.password) > 7) and (self.password == self.confirm_password):
            print(len(self.password))
            return False
        return True



def home():
    return pc.center(
        navbar(State),
        pc.vstack(
            pc.center(
                pc.vstack(
                    pc.heading("MBTI 테스트", font_size="1.52m"),
                ),
                width="100%",
            ),
        ),
        padding_top="6em",
        text_align="top",
        position="relative",
    )


def login():
    return pc.center(
        pc.vstack(
            pc.input(on_blur=State.set_userid, placeholder="Userid", width="100%"),
            pc.input(type_="password", on_blur=State.set_password, placeholder="Password", width="100%"),
            pc.button("로그인", on_click=State.login, width="100%"),
            pc.link(pc.button("회원가입", width="100%"), href="/signup", width="100%"),
        ),
        shadow="lg",
        padding="1em",
        border_radius="lg",
        background="white",
    )


def signup():
    return pc.box(
        pc.vstack(
            navbar(State),
            pc.center(
                pc.vstack(
                    pc.heading("MBTI 테스트 회원가입", font_size="1.5em"),
                    pc.input(
                        on_blur=State.set_username, placeholder="Username", width="100%"
                    ),
                    pc.cond(
                        State.alert_id,
                        pc.alert(
                            pc.alert_icon(),
                            pc.alert_title(
                                "아이디는 영어 대소문자, 숫자와 '_'기호만을 활용하여 4자 이상 20자 이하로 입력해주세요"
                            ),
                            status="error"
                        )
                    ),
                    pc.input(
                        on_blur=State.set_userid, placeholder="Userid", width="100%"
                    ),
                    pc.input(
                        type_="password", on_blur=State.set_password, placeholder="Password", width="100%"
                    ),
                    pc.cond(
                        State.alert_password,
                        pc.alert(
                            pc.alert_icon(),
                            pc.alert_title(
                                "비밀번호는 8자리 이상으로 입력해주세요"
                            ),
                            status="error"
                        ),
                    ),
                    pc.input(
                        type_="password",
                        on_blur=State.set_confirm_password,
                        placeholder="Password Confirm",
                        width="100%",
                    ),
                    pc.cond(
                        State.alert_confirm_password,
                        pc.alert(
                            pc.alert_icon(),
                            pc.alert_title(
                                "비밀번호를 확인해주세요"
                            ),
                            status="error"
                        ),
                    ),
                    pc.button(
                        "회원가입",
                        on_click=State.signup,
                        # is_disabled=State.judge_signup,
                        is_disabled=State.judge_signup,
                        width="100%"),
                ),
                shadow="lg",
                padding="1em",
                border_radius="lg",
                background="white",
            )
        ),
        padding_top="10em",
        text_align="top",
        position="relative",
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


def index():
    return pc.box(
        pc.vstack(
            navbar(State),
            pc.cond(
                State.logged_in,
                pc.center(
                    pc.link(pc.button("마이페이지", width="100%"), href="/"+State.userid, width="100%"),
                ),
                login(),
            ),
        ),
        padding_top="10em",
        text_align="top",
        position="relative",
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


def user():
    return pc.box(
        pc.vstack(
            navbar(State),
            pc.cond(
                State.logged_in,
                pc.center(
                    pc.vstack(
                        pc.cond(
                            State.exist_user,
                            pc.vstack(
                                pc.heading(State.get_target_username + "님의 페이지"),
                                pc.cond(
                                    State.exist_result,
                                    pc.vstack(
                                        pc.cond(
                                            State.exist_answer,
                                            pc.vstack(
                                                pc.text(State.username + "님이 생각하시는 " + State.get_target_username + "님의 MBTI는 "),
                                                pc.text(State.get_target_mbti + "입니다, 점수는 " + State.get_target_score+"입니다"),
                                                pc.button(State.get_target_username + "님의 MBTI 테스트 다시하기", on_click=State.load_question, width="100%"),
                                            ),
                                            pc.button(State.get_target_username + "님의 MBTI 테스트하기", on_click=State.load_question, width="100%"),
                                        ),
                                        pc.table_container(
                                            pc.table(
                                                pc.thead(
                                                    pc.tr(
                                                        pc.th("username"),
                                                        pc.th("mbtiresult"),
                                                        pc.th("score")
                                                    )
                                                ),
                                                pc.tbody(
                                                    pc.foreach(
                                                        State.target_results, show_results
                                                    )
                                                )
                                            ),
                                        )
                                    ),
                                    pc.vstack(
                                        pc.cond(
                                            State.judge_mypage,
                                            pc.button(State.get_target_username + "님의 MBTI 테스트하기", on_click=State.load_question, width="100%"),
                                            pc.text(State.get_target_username + "님이 MBTI 테스트를 진행하지 않으셨습니다")
                                        )
                                    )
                                )
                            ),
                            pc.heading("존재하지 않는 userid"),
                        ),
                        pc.center(
                            pc.input(on_blur=State.set_target_userid, placeholder="Userid", width="100%"),
                            pc.button("친구 페이지로 이동하기", on_click=lambda: State.load_user(State.target_userid), width="100%"),
                        ),
                        pc.button("마이페이지로 이동하기", on_click=lambda: State.load_user(State.userid), width="100%")
                    ),
                    shadow="lg",
                    padding="1em",
                    border_radius="lg",
                    background="white",
                ),
                login()
            )
        ),
        padding_top="10em",
        text_align="top",
        position="relative",
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )

def question():
    return pc.box(
        pc.vstack(
            navbar(State),
            pc.cond(
                State.logged_in,
                pc.box(
                    pc.vstack(
                        pc.heading("질문" + State.question_idx),
                        pc.text(State.get_ask),
                        pc.hstack(
                            pc.button(
                                State.get_answer_1,
                                on_click=lambda: State.change_answer(0),
                                bg=State.get_color1
                            ),
                            pc.center(
                                pc.divider(
                                    orientation="vertical", border_color="black"
                                ),
                                height="4em",
                            ),
                            pc.button(
                                State.get_answer_2,
                                on_click=lambda: State.change_answer(1),
                                bg=State.get_color2
                            )
                        ),
                        pc.hstack(
                            pc.button(
                                "<",
                                on_click=State.prev_question
                            ),
                            pc.button(
                                ">",
                                on_click=State.next_question
                            ),
                        ),
                        pc.vstack(
                            pc.progress(value=State.question_progress, width="100%"),
                            spacing="1em",
                            min_width=["10em", "20em"]
                        )
                    ),
                    shadow="lg",
                    padding="1em",
                    border_radius="lg",
                    background="white",
                ),
                login()
            ),
        ),
        padding_top="10em",
        text_align="top",
        position="relative",
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


def result():
    return pc.box(
        pc.vstack(
            navbar(State),
            pc.center(
                pc.vstack(
                    pc.cond(
                        State.logged_in,
                        pc.vstack(
                            pc.text(State.username+"님이 생각하시는 "+State.get_target_username+"님의 MBTI는 "),
                            pc.text(State.get_target_mbti+"입니다, 점수는 "+State.get_target_score+"입니다"),

                        ),

                        login()
                    ),
                ),
            )
        ),
        padding_top="10em",
        text_align="top",
        position="relative",
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )

def show_results(results: MbtiResult):
    return pc.tr(
        pc.td(results.username),
        pc.td(results.mbti),
        pc.td(results.score)
    )


app = pc.App(state=State)
app.add_page(index, title="MBTI 테스트")
app.add_page(signup, title="MBTI 테스트")
app.add_page(home)
app.add_page(user, title="MBTI 테스트", route="/[user]", on_load=State.load_user)
app.add_page(question, title="MBTI 테스트", on_load=State.load_question)
app.add_page(result, title="MBTI 테스트")
app.compile()
