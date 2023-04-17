import pynecone as pc
from .home import State, index, signup, home, user, question, result

app = pc.App(state=State)
app.add_page(index, title="MBTI 테스트")
app.add_page(signup, title="MBTI 테스트")
app.add_page(home)
app.add_page(user, title="MBTI 테스트", route="/[user]", on_load=State.load_user)
app.add_page(question, title="MBTI 테스트", on_load=State.load_question)
app.add_page(result, title="MBTI 테스트")
app.compile()
