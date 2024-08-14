import streamlit as st
from anthropic import Anthropic
import dotenv
import os

dotenv.load_dotenv()

anthropic_models = [
    "claude-3-5-sonnet-20240620"
]

# Function to convert the messages format to Anthropic
def messages_to_anthropic(messages):
    anthropic_messages = []
    prev_role = None
    for message in messages:
        if prev_role and (prev_role == message["role"]):
            anthropic_message = anthropic_messages[-1]
        else:
            anthropic_message = {
                "role": message["role"],
                "content": [],
            }
        anthropic_message["content"].append(message["content"][0])

        if prev_role != message["role"]:
            anthropic_messages.append(anthropic_message)

        prev_role = message["role"]
        
    return anthropic_messages

# Function to query and stream the response from Anthropic's Claude model
def stream_llm_response(model_params, api_key=None):
    response_message = ""
    client = Anthropic(api_key=api_key)

    with client.messages.stream(
        model=model_params["model"] if "model" in model_params else "claude-3-5-sonnet-20240620",
        messages=messages_to_anthropic(st.session_state.messages),
        temperature=model_params["temperature"] if "temperature" in model_params else 0.3,
        max_tokens=4096,
    ) as stream:
        for text in stream.text_stream:
            response_message += text
            yield text

    st.session_state.messages.append({
        "role": "assistant", 
        "content": [
            {
                "type": "text",
                "text": response_message,
            }
        ]
    })

def main():

    # --- Page Config ---
    st.set_page_config(
        page_title="The OmniChat",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # --- Header ---
    st.markdown("""<h1 style="text-align: center; color: #6ca395;">🤖 <i>The OmniChat</i> 💬</h1>""", unsafe_allow_html=True)

    # --- Side Bar ---
    with st.sidebar:
        default_anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") if os.getenv("ANTHROPIC_API_KEY") is not None else ""
        anthropic_api_key = st.text_input("Introduce your Anthropic API Key (https://console.anthropic.com/)", value=default_anthropic_api_key, type="password")

    # --- Main Content ---
    if anthropic_api_key == "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" or anthropic_api_key is None:
        st.write("#")
        st.warning("⬅️ Please introduce an Anthropic API Key to continue...")
    else:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Displaying the previous messages if there are any
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                for content in message["content"]:
                    if content["type"] == "text":
                        st.markdown(content["text"])

        # User input
        with st.chat_message("user"):
            model_params = {
                "model": st.selectbox("Model:", anthropic_models),
                "temperature": st.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.3, step=0.1),
            }

            user_message = st.text_area("Write your message here:", height=100)
            if user_message:
                user_input = {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message,
                        }
                    ],
                }
                st.session_state.messages.append(user_input)

        # Displaying the response in a stream manner
        with st.chat_message("assistant"):
            st.markdown("")
            for chunk in stream_llm_response(
                model_params=model_params, 
                api_key=anthropic_api_key,
            ):
                st.markdown(chunk)

if __name__ == "__main__":
    main()
