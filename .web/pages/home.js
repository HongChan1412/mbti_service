import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Avatar, Box, Center, HStack, Heading, Link, Menu, MenuButton, MenuDivider, MenuItem, MenuList, Text, VStack, useColorMode} from "@chakra-ui/react"
import NextLink from "next/link"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"confirm_password": "", "get_answer_1": null, "get_answer_2": null, "get_ask": null, "get_color1": null, "get_color2": null, "logged_in": false, "mbti_data": {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}, "password": "", "question_answer": {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": "", "12": ""}, "question_data": [], "question_data_state": false, "question_idx": 1, "question_progress": 8.333333333333334, "user": "", "user_page": "\uc874\uc7ac\ud558\uc9c0 \uc54a\ub294 \uc544\uc774\ub514\uc785\ub2c8\ub2e4", "userid": "", "usermbti": "", "username": "", "username_set": "", "events": [{"name": "state.hydrate"}]})
const [result, setResult] = useState({"state": null, "events": [], "processing": false})
const router = useRouter()
const socket = useRef(null)
const { isReady } = router;
const { colorMode, toggleColorMode } = useColorMode()
const Event = events => setState({
  ...state,
  events: [...state.events, ...events],
})
useEffect(() => {
  if(!isReady) {
    return;
  }
  if (!socket.current) {
    connect(socket, state, setState, result, setResult, router, EVENT, ['websocket', 'polling'])
  }
  const update = async () => {
    if (result.state != null) {
      setState({
        ...result.state,
        events: [...state.events, ...result.events],
      })
      setResult({
        state: null,
        events: [],
        processing: false,
      })
    }
    await updateState(state, setState, result, setResult, router, socket.current)
  }
  update()
})
return (
<Center sx={{"paddingTop": "6em", "textAlign": "top", "position": "relative"}}><Box sx={{"position": "fixed", "width": "100%", "top": "0px", "zIndex": "500"}}><HStack justify="space-between"
sx={{"borderBottom": "0.2em solid #F0F0F0", "paddingX": "2em", "paddingY": "1em", "bg": "rgba(255,255,255, 0.90)"}}><NextLink passHref={true}
href="/"><Link><HStack><Heading>{`MBTI 테스트`}</Heading></HStack></Link></NextLink>
<Menu><MenuButton><Avatar name={state.username}
size="md"/>
<Box/></MenuButton>
<MenuList><Center><VStack><Avatar name={state.username}
size="md"/>
<Text>{state.username}</Text></VStack></Center>
<MenuDivider/>
{state.logged_in ? <NextLink passHref={true}
href={("/" + state.userid)}><Link><MenuItem>{`마이페이지`}</MenuItem></Link></NextLink> : <NextLink passHref={true}
href="/"><Link><MenuItem>{`로그인`}</MenuItem></Link></NextLink>}
{state.logged_in ? <NextLink passHref={true}
href="#"><Link onClick={() => Event([E("state.logout", {})])}><MenuItem>{`로그아웃`}</MenuItem></Link></NextLink> : <NextLink passHref={true}
href="/signup"><Link><MenuItem>{`회원가입`}</MenuItem></Link></NextLink>}</MenuList></Menu></HStack></Box>
<VStack><Center sx={{"width": "100%"}}><VStack><Heading sx={{"fontSize": "1.52m"}}>{`MBTI 테스트`}</Heading></VStack></Center></VStack>
<NextHead><title>{`Pynecone App`}</title>
<meta name="description"
content="A Pynecone app."/>
<meta content="favicon.ico"
property="og:image"/></NextHead></Center>
)
}