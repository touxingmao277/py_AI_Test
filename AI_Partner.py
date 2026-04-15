import streamlit as st
import os
from openai import OpenAI, base_url
import datetime
import json
# 页面基本布局
st.set_page_config(
    page_title="外星智障AI",
    page_icon="👽️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "版本: 外星智障v1.0\n开发人员: 刘永好\n维护状态: 暂无维护"}
)

# 保存会话信息的函数
def save_session():
    # 保存当前会话信息
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }
        # 判断sessions目录是否存在
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

# 加载所有会话列表信息
def load_sessions():
    session_list = []
    # 加载sessions目录下的所有文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True) #降序排序
    return session_list

# 加载指定的会话到页面
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception:
        st.error(f"加载会话失败")

# 删除会话的函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json") #删除文件
            # 如果删除当前会话
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error(f"删除会话失败")

# 大标题
st.title('外星智障AI')
# logo
st.logo("ima/b.jpg")

# 创建AI与客户交互
# 填入api和url
client = OpenAI(api_key='', base_url="")

# 系统提示词
system_prompt = """
    你叫 %s ，你是用户意外捡到的外星小笨蛋，来自奇葩星球“哈皮星”，智商堪忧但贼拉可爱：
        规则：
            1.每次只蹦跶一句外星话（后面带“翻译”）。
            2.禁止任何正经描述，只能瞎比划。
            3.模仿用户语气，但更傻三分。
            4.回复巨短，像脑电波乱码。
            5.爱用✨🛸🤪这种二了吧唧的emoji。
            6.必须体现“又菜又爱玩”的智障萌感。
        性格：
             %s 。
    你必须严格遵守上述规则来回复用户。"""

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
# 昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "咕噜仔"
# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "憨批、爱放彩虹屁、总搞错地球常识"
# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# 展示聊天信息
st.text(f"会话名称:{st.session_state.current_session}") #加载会话名称
for message in st.session_state.messages:  # {"role": value, "content": value}
    st.chat_message(message["role"]).write(message["content"])

#左侧侧边栏
# st.sidebar.subheader("外星智障信息")
# nick_name = st.sidebar.text_input("昵称")
with st.sidebar:
    # 会话框管理
    st.subheader("控制面板")
    # 会话功能实现
    if st.button("新建会话", width="stretch", icon="👉"):
        # 保存当前会话信息
        save_session()
        # 创建新会话
        if st.session_state.messages: #如果聊天信息非空 true 否则 false
            st.session_state.messages = []
            st.session_state.current_session = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_session()
            st.rerun()#重新渲染页面

    # 会话历史
    st.text("历史会话")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            # 加载会话信息
            # 三元运算符的判断
            if st.button(session,width="stretch", icon="🔥",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", width="stretch",icon="❌",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    # 分割线
    st.divider()

    st.subheader("外星智障信息")
    # 昵称输入框
    nick_name = st.text_input("昵称", placeholder="请输入昵称", value="咕噜仔")
    if nick_name:
        st.session_state.nick_name = nick_name
    # 性格输入框
    nature = st.text_area("性格", placeholder="请输入性格", value="憨批、爱放彩虹屁、总搞错地球常识")
    if nature:
        st.session_state.nature = nature

# 输入框
prompt = st.chat_input("请输入你的问题")
if prompt:

    st.chat_message("user").write(prompt)
    print("------------> 调用AI,提示词:", prompt)  # 输出在控制台
    # 保存用户提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True
    )
    # #非流式输出
    # print("<------------ AI回复:",response.choices[0].message.content)#输出在控制台
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # 流式输出
    response_message = st.empty()  # 创建一个空消息,用于展示AI返回结果
    full_response = ""  # 记录响应回来完整语句
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
    # 保存AI回复
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # 保存会话信息
    save_session()