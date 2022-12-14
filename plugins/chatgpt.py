
import asyncio
from nonebot import on_command
from chatgpt.api import ChatGPT
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.log import logger
from nonebot.params import CommandArg
chat=on_command("chat",aliases={"chatgpt"})
@chat.handle()
async def work(event:Event,cmd_arg: Message = CommandArg()):
    text=cmd_arg.extract_plain_text()
    logger.info(text)
    loop=asyncio.get_event_loop()
    # await chat.send("别急")
    te=await loop.run_in_executor(None,chatpre,text);
    # te=await chatpre(text)
    logger.error(text)
    user_id=event.get_user_id()
    msg=Message(f'[CQ:at,qq={user_id}]'+te)
    await chat.finish(msg)

def chatpre(x):
    with ChatGPT(response_timeout=50,session_token="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..sSAAdl45KQfxmtlk.mAgCdbQ3yssEtUmc_0qgUaFzVnE7iO_2_04uboMd2YJeWfpm6btRwZT9MZ_efcgEaNPsGkvz_WYARnsavmRbgKbQ4l1dXDnZ0ypwdyh5gOjMOak19001lkk5YAkmLyalMldVtvEN2WWpH9TaduUdGZ3PHi1EzlGbcNtzz1CQwwIV-HijAmU7vc_D9HQTw2jEBN0x-PL6Q4yU6YCxgPFVDR9-n5wcYYMCpxPEkMXoxKRHENGUpka3_dVj557nxL1_x1QuTv86uKrs0vZgs27iUxa_9N5HEVl0vDST3c6wUDB7MwCHEaF3naCFJbJMNHMW_YeEswiOW719pkrsXx_hn6iqbLCOWceO5bbFjrGxWDlaCdE66mo0b-2IxRphZ0jwHq76F1sPo-3UrPcT_CSGSZn6sxsN95cTWwa1GvRPbNaHMrNLE9V6_CwCPsGqyTWH3Anzz6tbgICxMS52Odzy7xhCW6_8E66ejJ3R-sQpxl8BwgqisRUnCKQs2W1en0c0ZIKRCGWYFSaC0RJqh34zSfp85JHQsUzGOCuBa2bz9Jq1cRFR2CDSmW9h6AolbsTKAcmJVjV1SZARkeDbmb4QjXlMbNVHx502P1u4h1J6sRHwKPCCq17qmgDGBFUVWsUs08EqbdDCSO6ea9QS72imRzKE57x_aCHsWjtG4spjHtIhUEwarhz4qbLwJgnDtcX4dOXn-OviF8wEkCprUKYBsKRI6yxwfPOWTAqpJXmAjuRzihPMFdfokis7g25hWicT8-KcUb7NDotdlAwI4GAULcMqUdgQx2-k3NSgtaUabHBD_7KV1fEnXeMA_9e4coZ8UzIPIR-0JthGQqUloXdsHlPx-ezsOKxkIfGyJlphsxYHqy2PPLwxhJm7vO4ns0HNL7EE6rmNmqjmxnfbh2WKPqIEjIhJYFl7vk3C4XbwHmKmZs-MvL9apAuvOWBcU3dDXGIb8o5srLfbIT2Tbs2u5hf9Vca19h2f_BH73KuD5bz7AQf8Zw4lOBGsRKhTXhd62NWdLPE1lxxVXBq_o7iWO4wQECqq0y2eh1f2bqg44Xwq3BOCZHeHsRC6aS8BJ9UTE4BFgA1hTBwly-6VHTuizKk2_3Do-JGpoaat2iBZCkJcsca3JuDFKKrPLzHM0ZCRJuyOgQ55JBDcxsXhVgiVTZN26FAzInAkllr9ZXL3CT774EXQEoi7OzYAbguqrRGqP3P7ElUrTLW-69xSgt5SC48jkl7Tz5csep9nJACpyWmkxOb8vYA_dIvGfneHC-2RB5xtM3_0D56cKGS0sDy-GG3qcxLddy45sd-DHtZJq5biwa6G0oOGZRAwRZNBc-80Aq2tpMKSxboMurxBdjm6Wx5PD0qS0HQL3HhRACSt4E_qBI0V6jcYlphcibHnByOnEZN2xkFruvn0s9CzrdNgDRhSiYk7gmBItj-aBy7gYVxxbUE2EXPSIQpSzJvOm77YN7PvRDs_kOJ0J_O18rY94BkPSVmRH-FUZQ5Yn7h0qbtAN1kycjJKBw4qiiUm9O2z1FBhepTnUwWegffr1ainzAIubJb2vEeUMM_SbVTljwI3lqE2KFQ5-g63e8WtQHWQqL3uybY3Sl52hJut5AkyVcB7q6BnD4lkbJKxL188RjEXfSnzAI-gcUKp_OakgMC1mt2h_a5Fd-cK3ShMGEfReuO3ry8_GSd0v9YMKNrGEirxnCy-_GmmQrBbJ88KdjSt9E3fnzrgDMRSqTwg-wQ_xJqOlFj9ES3JZRfLJrqIFm1Q1Mg4OCLnwFwBNYgPllSQWXZ1_CCPw-tksJRQxMU41XnZah55ANl42yMfPL7JSTpl2N_fqpbd6umGrnTOzzbR7WIU18QwHg9Iis1VWdf6mJHxmQfQk6ktFss5IZfcAVD1XW6nB59M-reAbaDUQBV43t6aRFa4-rX-0WPAbFja5PTaJC09LR3gGnlzuZI3jWYlXuoxwpCMdi8wJwvBQCmi-7n1Vxp_BvF5yBxI6dzbFmXQ8VbVDs4FJCrF77EaWbV_6XUeUsGlUSiIDkBsttYQqNHPDYqJCKTyIOhhuFAQ12KKrq99HVursvUkjV-esUgnUAODjESE7Ast2ZnGahV2brDxPktHHOEcJ6B8VrvfCy0-r6TTRMNuCuFJ0NWtDfoWfN-kqAP7m036qP9aG8U1RAeXni_TM3_Yd27FzQyYoPxsvWXspBABWHDEFKgUfETOzBxUImWFFKNruhSURZ-6Jzt5HJs3MMTE0DCl3g.0Twi5xdB1Uj76WQJlLIYZw",proxies="http://localhost:7890") as chat:
        response = chat.send_message(x)
        return response.content