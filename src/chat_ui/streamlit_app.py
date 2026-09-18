import streamlit as st
import requests
from typing import Dict, Any


st.set_page_config(
    page_title="GitHub MCP Assistant",
    page_icon="🤖",
    layout="wide"
)


FASTAPI_URL = "http://mcp-client:8000"
ASK_ENDPOINT = f"{FASTAPI_URL}/ask"


def send_message_to_api(prompt: str) -> Dict[str, Any]:
    """
    Send a message to the FastAPI server and return the response.
    """
    try:
        payload = {"prompt": prompt}

        response = requests.post(
            ASK_ENDPOINT,
            json=payload,
            timeout=65
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out. Please try again."
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": (
                "Could not connect to the MCP client. "
                "Please make sure the FastAPI server is running."
            )
        }

    except requests.exceptions.HTTPError:
        if response.status_code == 504:
            return {
                "error": "The AI service timed out. Please try again."
            }

        elif response.status_code in (429, 500):
            return {
                "error": (
                    f"Server error: "
                    f"{response.json().get('detail', 'Unknown error')}"
                )
            }

        else:
            return {
                "error": (
                    f"HTTP error {response.status_code}: "
                    f"{response.json().get('detail', 'Unknown error')}"
                )
            }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }


def main():
    st.title("GitHub MCP Assistant")

    st.markdown(
        "Chat with your AI assistant powered by Gemini "
        "and GitHub MCP tools."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new message
    if prompt := st.chat_input("Ask something about GitHub..."):

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = send_message_to_api(prompt)

            if "error" in response_data:
                error_message = f" {response_data['error']}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

            else:
                ai_response = response_data.get(
                    "response",
                    "No response received"
                )

                st.markdown(ai_response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

    # Sidebar
    with st.sidebar:
        st.header("Chat Options")

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):
            st.session_state.messages = []
            st.rerun()

        st.header("Server Status")

        if st.button(
            "🔍 Check Server",
            use_container_width=True
        ):
            try:
                response = requests.get(
                    f"{FASTAPI_URL}/docs",
                    timeout=5
                )

                if response.status_code == 200:
                    st.success(" Server is running")
                else:
                    st.error(" Server responded with an error")

            except requests.exceptions.RequestException:
                st.error(" Server is not accessible")

        st.header("Configuration")

        st.text_input(
            "FastAPI Server URL",
            value=FASTAPI_URL,
            disabled=True
        )

        st.caption(
            "Update FASTAPI_URL in the code to change the server address."
        )


if __name__ == "__main__":
    main()
