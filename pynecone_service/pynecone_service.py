import pynecone as pc
from .helpers import navbar


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
    target_result: str


class State(pc.State):
    userid: str = ""
    username_set: str = ""
    username: str = ""
    password: str = ""
    confirm_password: str = ""
    logged_in: bool = False

    question_idx: int = 1
    question_progress: float = 100 / 12 * question_idx

    question_answer: dict = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "", 11: "", 12: "", }
    question_data: list = []
    question_data_state: bool = False

    usermbti: str = ""
    mbti_data: dict = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}


    user_text: str = ""

    #############################################
    target_userid: str = ""
    target_userid_set: str = ""
    target_user: dict = {}
    target_data: dict = {"user": {"userid": "", "username": ""}, "info": {"userid": "", "target_userid": "", "username": "", "target_username": "", "mbti": "", "score": "", "question_result": "", "target_result": ""}}

    exist_user: bool = False
    exist_result: bool = False
    exist_answer: bool = False

    # results: list[MbtiResult] = []

    def login(self):
        with pc.session() as session:
            user = session.query(User).where(User.userid == self.userid).first()
            if user and user.password == self.password:
                self.logged_in = True
                self.username = user.username
                return self.load_user(True)
                # return pc.redirect("/"+self.userid)

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
                user = User(userid=self.userid, password=self.password, username=self.username_set)
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

    def load_user(self, mypage=False):
        if mypage:
            self.target_userid = self.userid
        else:
            if not self.target_userid:
                self.target_userid = self.get_query_params().get("user")

        self.target_data = {"user": {"userid": self.target_userid, "username": ""}, "info": {"userid": "", "target_userid": "", "username": "", "target_username": "", "mbti": "", "score": "", "question_result": "", "target_result": ""}}
        self.exist_user = False
        self.exist_result = False
        self.exist_answer = False

        with pc.session() as session:
            exist_user = session.query(User).where(User.userid == self.target_userid).first()
            if exist_user:
                self.exist_user = True
                self.target_data["user"] = {"userid": exist_user.userid, "username": exist_user.username}
                exist_result = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid).all()
                if exist_result:
                    self.exist_result = True
                    exist_answer = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid, MbtiResult.userid == self.userid).first()
                    if exist_answer:
                        self.exist_answer = True
                        self.target_data["info"] = {"userid": exist_answer.userid, "target_userid": exist_answer.target_userid, "username": exist_answer.username, "target_username": exist_answer.target_username, "mbti": exist_answer.mbti, "score": exist_answer.score, "question_result": exist_answer.question_result, "target_result": exist_answer.target_result}
        self.target_userid = ""
        return pc.redirect("/" + self.target_data["user"]["userid"])


    # def get_target_data(self):
    #     if not self.target_userid_set:
    #         self.target_userid = self.get_query_params().get("user")
    #     else:
    #         self.target_userid = self.target_userid_set
    #         self.target_userid_set = ""
    #     self.target_user = {}
    #     self.target_data = {}
    #     self.exist_user = False
    #     self.exist_result = False
    #     self.exist_answer = False
    #
    #     with pc.session() as session:
    #         exist_user = session.query(User).where(User.userid == self.target_userid).first()
    #         if exist_user:
    #             self.exist_user = True
    #             self.target_user = {"target_userid": exist_user.userid, "target_username": exist_user.username}
    #             exist_result = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid).all()
    #             if exist_result:
    #                 self.exist_result = True
    #                 exist_answer = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid, MbtiResult.userid == self.userid).first()
    #                 if exist_answer:
    #                     self.exist_answer = True
    #                     self.target_data = {"userid": exist_answer.userid, "target_userid": exist_answer.target_userid, "username": exist_answer.username, "target_username": exist_answer.target_username, "mbti": exist_answer.mbti, "score": exist_answer.score, "question_result": exist_answer.question_result, "target_result": exist_answer.target_result}
    #
    #     return pc.redirect("/"+self.target_userid)



        #             # print(f"exist_result: {exist_result}")
        #             # print(f"exist_reuslt_type: {type(exist_result)}")
        #             # print(f"exist_result[0]: {exist_result[0]}")
        #             # print(f"exist_result[0]_type: {type(exist_result[0])}")
        #             # ret = next((item for item in exist_result if item.userid == self.userid), None)[0]
        #             # ret = (next(item for item in exist_result if item.userid == self.userid), None)[0]
        #             # if ret:
        #             #     self.target_data = {"userid": ret.userid, "target_userid": ret.target_userid, "username": ret.username, "target_username": ret.target_username, "mbti": ret.mbti, "score": ret.score, "question_result": ret.question_result, "target_result": ret.target_result}
        #             # else:
        #             #     self.target_data = {}
        #         else:
        #             self.target_data = {}
        #     else:
        #         self.target_data = {}
        #
        # # print(self.target_data)

    # @pc.var
    # def user_page(self):
    #     self.target_userid = self.get_query_params().get("user")
    #     with pc.session() as session:
    #         exist_user = session.query(User).where(User.userid == self.target_userid).first()
    #         if exist_user:
    #             exist_result = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid).first()
    #             if exist_result:
    #                 exist_answer = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid, MbtiResult.userid == self.userid).first()
    #                 if exist_answer:
    #                     self.target_user = {"userid": exist_answer.userid, "target_userid": exist_answer.target_userid, "username": exist_answer.username, "target_username": exist_answer.target_username, "mbti": exist_answer.mbti, "score": exist_answer.score, "question_result": exist_answer.question_result,
    #                                         "target_result": exist_answer.target_result}
    #                     if self.target_userid == self.userid:
    #                         self.user_text = f"{self.target_user['username']}님의 MBTI는 {self.target_user['mbti']}입니다"
    #                     else:
    #                         self.user_text = f"{self.username}님이 생각하시는 {self.target_user['username']}님의 MBTI는 {self.target_user['mbti']}입니다 정확도는 {self.target_user['score']}입니다"
    #                 else:
    #                     self.target_user = {}
    #                     self.user_text = f"{exist_user.username}님의 MBTI를 맞춰보세요"
    #             else:
    #                 self.target_user = {}
    #                 if self.target_userid == self.userid:
    #                     self.user_text = f"MBTI 테스트를 진행해주세요"
    #                 else:
    #                     self.user_text = f"{exist_user.username}님이 MBTI 테스트를 진행하지 않으셨습니다"
    #         else:
    #             self.target_user = {}
    #             self.user_text = f"{self.target_userid}는 존재하지 않는 아이디입니다"
    #
    #     print(self.target_user)
        # return self.user_text

    # def move_page(self):
    #     print(f"target_id: {self.target_id}")
    #     self.target_userid = self.target_id
    #     return pc.redirect("/" + self.target_userid)


    def load_question(self):
        with pc.session() as session:
            self.question_data = session.query(Question).all()
            self.question_data_state = True
            return pc.redirect("/question")

    def next_question(self):
        if self.question_idx == 12:
            return self.get_result()
        self.question_idx += 1
        self.question_progress = 100 / 12 * self.question_idx

    def prev_question(self):
        if self.question_idx == 1:
            return pc.redirect(f"/{self.userid}")
        self.question_idx -= 1
        self.question_progress = 100 / 12 * self.question_idx

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
        if self.question_answer[self.question_idx] in ["E", "S", "T", "J"]:
            return "rgb(29 161 242)"

    @pc.var
    def get_color2(self):
        if self.question_answer[self.question_idx] in ["I", "N", "F", "P"]:
            return "rgb(29 161 242)"

    def change_answer(self, question_answer):
        self.question_answer[self.question_idx] = self.question_data[(self.question_idx - 1) * 2 + question_answer].mbti_type

        if self.question_idx == 12:
            return self.get_result()
        self.question_idx += 1
        self.question_progress = 100 / 12 * self.question_idx

    def get_result(self):
        for k, v in self.question_answer.items():
            if not v:
                return pc.window_alert(f"{k}번 질문의 답변을 확인해주세요")
            self.mbti_data[v] += 1
        if self.mbti_data["E"] > self.mbti_data["I"]: self.usermbti += "E"
        else: self.usermbti += "I"
        if self.mbti_data["S"] > self.mbti_data["N"]: self.usermbti += "S"
        else: self.usermbti += "N"
        if self.mbti_data["T"] > self.mbti_data["F"]: self.usermbti += "T"
        else: self.usermbti += "F"
        if self.mbti_data["J"] > self.mbti_data["P"]: self.usermbti += "J"
        else: self.usermbti += "P"

        with pc.session() as session:
            exist_result = session.query(MbtiResult).where(MbtiResult.userid == self.userid, MbtiResult.target_userid == self.target_userid)
            if exist_result:
                session.query(MbtiResult).where(MbtiResult.userid == self.userid, MbtiResult.target_userid == self.target_userid).update({"userid": self.userid, "try_userid": self.userid, "username": self.username, "try_username": self.username, "mbti": self.usermbti, "score": 100.0, "question_result": str(self.question_answer), "try_question": str(self.question_answer)})
            else:
                result = MbtiResult(userid=self.userid, target_userid=self.target_userid, username=self.username, target_username=self.username, mbti=self.usermbti, score=100.0, question_result=str(self.question_answer), try_question=str(self.question_answer))
                session.add(result)
            session.commit()
        self.mbti_data = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "", 11: "", 12: "", }
        return pc.redirect("/result")

    @pc.var
    def get_target_username(self):
        return self.target_data["user"]["username"]

    @pc.var
    def get_target_mbti(self):
        return self.target_data["info"]["mbti"]

    # @pc.var
    # def get_results(self) -> list[MbtiResult]:
    #     with pc.session() as session:
    #         self.results = session.query(MbtiResult).where(MbtiResult.target_userid == self.target_userid).all()
    #         return self.results



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
                    pc.input(
                        on_blur=State.set_userid, placeholder="Userid", width="100%"
                    ),
                    pc.input(
                        type_="password", on_blur=State.set_password, placeholder="Password", width="100%"
                    ),
                    pc.input(
                        type_="password",
                        on_blur=State.set_confirm_password,
                        placeholder="Password Confirm",
                        width="100%",
                    ),
                    pc.button("회원가입", on_click=State.signup, width="100%"),
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
                                                pc.text(State.username+"님이 생각하시는 "+State.get_target_username+"님의 MBTI는 "+State.get_target_mbti+"입니다"),
                                                pc.button(State.get_target_username + "님의 MBTI 테스트 다시하기", on_click=State.load_question, width="100%"),
                                            ),
                                            pc.button(State.get_target_username + "님의 MBTI 테스트하기", on_click=State.load_question, width="100%"),
                                        ),
                                        pc.table_container(
                                            pc.table(
                                                pc.table_caption("Table"),
                                                pc.thead(
                                                    pc.tr(
                                                        pc.th("username"),
                                                        pc.th("mbtiresult"),
                                                        pc.th("score")
                                                    )
                                                ),
                                                # pc.tbody(pc.foreach(State.get_results, show_result))
                                            )
                                        )
                                    ),
                                    pc.text(State.get_target_username + "님이 MBTI 테스트를 진행하지 않으셨습니다")
                                )
                            ),
                            pc.heading("존재하지 않는 userid"),
                        ),
                        pc.center(
                            pc.input(on_blur=State.set_target_userid, placeholder="Userid", width="100%"),
                            pc.button("친구 페이지로 이동하기", on_click=lambda: State.load_user(False), width="100%"),
                        ),
                        pc.button("마이페이지로 이동하기", on_click=lambda: State.load_user(True), width="100%")
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
                State.question_data_state,
                pc.container(
                    pc.vstack(
                        pc.heading("질문"+State.question_idx),
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
                pc.center(
                    pc.vstack(
                        pc.cond(
                            State.logged_in,
                            pc.button(
                                "테스트 진행하기",
                                on_click=State.load_question
                            ),
                            login(),
                        )
                    )
                )
            )
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
                        pc.text(State.username+"의 MBTI: "+State.usermbti),
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


# def show_result(res: MbtiResult):
#     return pc.tr(
#         pc.td(res.username),
#         pc.td(res.mbti),
#         pc.td(res.score)
#     )


app = pc.App(state=State)
app.add_page(index, title="MBTI 테스트")
app.add_page(signup, title="MBTI 테스트")
app.add_page(home)
app.add_page(user, title="MBTI 테스트", route="/[user]", on_load=State.load_user)
app.add_page(question, title="MBTI 테스트")
app.add_page(result, title="MBTI 테스트")
# app.add_page(question, route="/question/[user]")
app.compile()
