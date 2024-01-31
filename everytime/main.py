import time, os
import streamlit as st
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from everytime.llm import get_answer

tz = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

colors = ['blue', 'green', 'orange', 'red', 'violet', 'gray', 'rainbow']
emojis = ['🧸', '🎊', '🎉', '🎎', '🪭', '🏮', '🏮']

page_icon = "🧸"
page_title = "EveryTime GPT"


answer = """
Enter api_key to start.
"""

img_url = "https://source.unsplash.com/1600x900/?background"
img_ref = "https://unsplash.com/"

st.set_page_config(
    page_title=page_title, 
    page_icon=page_icon, 
)
# sidebar()

style = open('everytime/style.css').read()

st.markdown(f"""
<style>
{style}
</style>""",unsafe_allow_html=True)

n = 0
while True:
    now = datetime.now(tz=tz)

    openai_api_key = st.session_state.get("OPENAI_API_KEY")

    image = st.image(
        f'{img_url}&_m={str(datetime.now(tz=tz).minute)}'
    )

    container = st.empty()

    n += 1; 
    if not openai_api_key:
        container.warning(f"Paste your OpenAI API key here (sk-.../sess-...)", icon="🎊")

        openai_api_key = container.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", "")
            or st.session_state.get("OPENAI_API_KEY", ""),
        )
        st.session_state["OPENAI_API_KEY"] = openai_api_key
        time.sleep(1)
    else:
        answer = get_answer(openai_api_key, datetime.now(tz=tz))
        container.success(answer, icon=page_icon)
        time.sleep(60)

    st.rerun()