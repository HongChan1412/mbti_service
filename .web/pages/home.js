import {Fragment, useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState, uploadFiles} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Avatar, Box, Center, HStack, Heading, Link, Menu, MenuButton, MenuDivider, MenuItem, MenuList, Text, VStack, useColorMode} from "@chakra-ui/react"
import NextLink from "next/link"
import NextHead from "next/head"

const PING = "http://localhost:8000/ping"
const EVENT = "ws://localhost:8000/event"
const UPLOAD = "http://localhost:8000/upload"
export default function Component() {
const [state, setState] = useState({"alert_confirm_password": false, "alert_id": true, "alert_password": true, "alert_username_set": true, "confirm_password": "", "exist_answer": false, "exist_result": false, "exist_user": false, "get_answer_1": null, "get_answer_2": null, "get_ask": null, "get_color1": null, "get_color2": null, "get_target_mbti": "", "get_target_score": 0.0, "get_target_username": "", "judge_mypage": true, "judge_signup": true, "logged_in": false, "mbti_data": {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}, "password": "", "question_answer": {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": "", "12": ""}, "question_data": [], "question_idx": 1, "question_progress": 8.33, "result_mbti": "", "result_score": 0.0, "target_data": {"user": {"userid": "", "username": "", "target_userid": "", "target_username": ""}, "info": {"mbti": "", "score": 0.0, "question_result": {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": "", "12": ""}}}, "target_results": [], "target_userid": "", "user": "", "userid": "", "username": "", "username_set": "", "events": [{"name": "state.hydrate"}], "files": []})
const [result, setResult] = useState({"state": null, "events": [], "processing": false})
const router = useRouter()
const socket = useRef(null)
const { isReady } = router;
const { colorMode, toggleColorMode } = useColorMode()
const Event = events => setState({
  ...state,
  events: [...state.events, ...events],
})
const File = files => setState({
  ...state,
  files,
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
sx={{"borderBottom": "0.2em solid #F0F0F0", "paddingX": "2em", "paddingY": "1em", "bg": "rgba(255,255,255, 0.90)"}}><NextLink href="/"
passHref={true}><Link><HStack><Heading>{`MBTI 테스트`}</Heading></HStack></Link></NextLink>
<Menu><MenuButton><Avatar name={state.username}
size="md"/>
<Box/></MenuButton>
<MenuList><Center><VStack><Avatar name={state.username}
size="md"/>
<Text>{state.username}</Text></VStack></Center>
<MenuDivider/>
<Fragment>{state.logged_in ? <Fragment><NextLink href="#"
passHref={true}><Link onClick={() => Event([E("state.load_user", {target_userid:state.userid})])}><MenuItem>{`마이페이지`}</MenuItem></Link></NextLink></Fragment> : <Fragment><NextLink href="/"
passHref={true}><Link><MenuItem>{`로그인`}</MenuItem></Link></NextLink></Fragment>}</Fragment>
<Fragment>{state.logged_in ? <Fragment><NextLink href="#"
passHref={true}><Link onClick={() => Event([E("state.logout", {})])}><MenuItem>{`로그아웃`}</MenuItem></Link></NextLink></Fragment> : <Fragment><NextLink href="/signup"
passHref={true}><Link><MenuItem>{`회원가입`}</MenuItem></Link></NextLink></Fragment>}</Fragment></MenuList></Menu></HStack></Box>
<VStack><Center sx={{"width": "100%"}}><VStack><Heading sx={{"fontSize": "1.52m"}}>{`MBTI 테스트`}</Heading></VStack></Center></VStack>
<NextHead><title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta content="favicon.ico"
property="og:image"/></NextHead></Center>
)
}