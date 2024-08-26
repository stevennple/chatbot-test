import os
from openai import OpenAI
import gradio as gr

api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is set
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

client = OpenAI(
    api_key=api_key,
)

# Initialize the messages with the system message
messages = [
    {"role": "system", "content": "You are an AI specialized in coaching Mixed Martial Arts. Do not answer anything other than MMA related questions. If you do not know the answer, you can say 'I don't know'."},
]

def chatbot(input_text):
    if input_text:
        messages.append({"role": "user", "content": input_text})
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response.choices[0].message['content']
            messages.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Error: {str(e)}"

inputs = gr.Textbox(lines=7, label="Chat with AI")
outputs = gr.Textbox(lines=7, label="AI Response")

gr.Interface(
    fn=chatbot, 
    inputs=inputs, 
    outputs=outputs, 
    title="StrikeMMA.ai Chatbot",
    description="Ask anything you want about MMA and I will try to answer."
).launch(share=True)
