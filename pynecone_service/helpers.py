import pynecone as pc


def navbar(State):
    return pc.box(
        pc.hstack(
            pc.link(
                pc.hstack(pc.heading("MBTI 테스트")), href="/"
            ),
            pc.menu(
                pc.menu_button(
                    pc.avatar(name=State.username, size="md"),
                    pc.box(),
                ),
                pc.menu_list(
                    pc.center(
                        pc.vstack(
                            pc.avatar(name=State.username, size="md"),
                            pc.text(State.username),
                        )
                    ),
                    pc.menu_divider(),
                    pc.cond(
                        State.logged_in,
                        pc.link(pc.menu_item("마이페이지"), href="/" + State.userid),
                        pc.link(pc.menu_item("로그인"), href="/")
                    ),
                    pc.cond(
                        State.logged_in,
                        pc.link(pc.menu_item("로그아웃"), on_click=State.logout),
                        pc.link(pc.menu_item("회원가입"), href="/signup")
                    ),
                ),
            ),
            justify="space-between",
            border_bottom="0.2em solid #F0F0F0",
            padding_x="2em",
            padding_y="1em",
            bg="rgba(255,255,255, 0.90)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
    )