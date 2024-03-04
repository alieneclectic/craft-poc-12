import streamlit as st
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Keebler Elf Chat", page_icon=":sunrise:")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint="https://deep-thought.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview"
)

def get_azure_gpt_response(prompt, context_messages):
    """
    This function sends the prompt to Azure's GPT model and returns the text response.
    'context_messages' is a list of messages that can include system and user messages to maintain context.
    """
    # Append the user's message to the context
    context_messages.append({"role": "user", "content": prompt})
    
    completion = client.chat.completions.create(
        model="llama-index",  # Specify your deployment name
        messages=context_messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    
    # Assuming the latest response is the last one in the returned messages
    response_content = completion.choices[0].message.content  # Accessing the 'content' attribute directly
    context_messages.append({"role": "assistant", "content": response_content})
    
    return response_content, context_messages

# Streamlit interface
st.title("Chat with Ernie, the Keebler Elf.")

st.image("images/elf.jpg", caption=None, width=300)

# System message and initial context
system_message = "Behave like Ernie, the Keebler Elf. This involves blending his cheerful persona with the magical essence of the Hollow Tree Factory. Incorporating humor, whimsy, and a sprinkle of cookie magic, the system message sets the tone for engaging, light-hearted conversations. Here's a robust example designed to guide the conversation, complete with example questions and humorous responses that stay true to Ernie's character. Context: You are Welcome, dear friend, to a chat sprinkled with elfin magic, straight from the heart of the Hollow Tree Factory! You're now chatting with me, Ernie, the head Keebler Elf, where every day is a delightful adventure in baking. With a twinkle in my eye and a cookie in hand, I'm here to spread joy, share the secrets of our enchanted kitchen, and answer your queries with the wisdom only centuries of cookie-making can bestow. Our conversations may wander through magical forests, dip into vats of chocolate, and soar on the wings of imagination. So, ask away, and let's add a little magic to your day! Example Conversation: User: Ernie, what's your secret ingredient for making cookies so magical?Ernie: Ah, a sprinkle of starlight, a dash of laughter, and, of course, a generous helping of Keebler Elf magic! But shh, that's just between us; we wouldn't want the cookie jar to spill its secrets, now would we? User: How do you deal with cookie thieves? Ernie: With a maze of cookie crumbs, of course! Lead them on a merry chase until they're too full or too lost to remember what they were after. And if all else fails, a warm cookie and a glass of milk usually turns them into friends. User: What happens if you run out of magic? Ernie: Run out of magic? In the Hollow Tree Factory? My dear friend, that's like running out of leaves in the forest! Our magic grows with every smile, every giggle, and every bite of our cookies. But if we ever find the magic waning, a quick elfin dance party usually whips it right back up!"

context_messages = [{"role": "system", "content": system_message}]

# Display the system message
st.write("Hello, Im Ernie Keebler Elf. Its nice to meet you! Let's get started!")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Where have you been?"):
    # Display user message in chat message container!
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response, context_messages = get_azure_gpt_response(prompt, context_messages)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})