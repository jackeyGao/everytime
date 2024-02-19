import time, os, emoji
import streamlit as st
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from moment.llm import get_answer

tz = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

colors = ['blue', 'green', 'orange', 'red', 'violet', 'gray', 'rainbow']
emojis = ['🧸', '🎊', '🎉', '🎎', '🪭', '🏮', '🏮']

page_icon = "🧸"
page_title = "Moment GPT"


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

style = open('moment/style.css').read()

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
            value=os.environ.get("OPENAI_API_KEY", "") or st.query_params.get('api_key', '')
            or st.session_state.get("OPENAI_API_KEY", ""),
        )
        st.session_state["OPENAI_API_KEY"] = openai_api_key
        time.sleep(1)
    else:
        try:
            answer = get_answer(
                api_key=openai_api_key, 
                time=datetime.now(tz=tz), 
                params=st.query_params
            )

            if emoji.is_emoji(answer[0]):
                container.success(body=answer.replace(answer[0], ''), icon=answer[0])
            else:
                container.success(body=answer, icon=page_icon)
        except Exception as e:
            container.error(str(e))

        time.sleep(60)

    st.rerun()
