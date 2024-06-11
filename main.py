import streamlit as st
from utils import generate_script

st.title('短视频脚本生成器')

with st.sidebar:
    openai_api_key = st.text_input('请输入您的OpenAI API密钥', type='password')
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/api-keys)")
    openai_base_url = st.text_input('如果需要，您可以输入您的api base url')

title = st.text_input('请输入您的短视频主题')
time = st.number_input('请输入您期望的短视频时长（分钟）', min_value=0.1, step=0.1, max_value=1.0)
temperature = st.slider('请输入视频的创造力（数字越小代表越严谨）', min_value=0.1, value=0.5, max_value=1.0, step=0.1)
start = st.button('生成脚本！')

if start:
    warning_msg = ""
    if not openai_api_key:
        warning_msg = "请输入您的OpenAI API密钥！"
    elif not title:
        warning_msg = "请输入您的短视频主题"
    elif not time:
        warning_msg = "请输入您期望的短视频时长"

    if warning_msg:
        st.info(warning_msg)
        st.stop()
    else:
        with st.spinner(("AI思考中，请稍等...")):
            video_title, video_script = generate_script(title, temperature, time, openai_api_key, openai_base_url)
        st.success('视频脚本已生成')
        st.subheader('视频标题')
        st.write(video_title)
        st.subheader('视频脚本')
        st.write(video_script)
