import os
import gradio as gr
import json
from datetime import datetime
import openai


# Assistant Creation function
def create_assistant_json(uploaded_file, assistant_name,  assistant_message):
    client = openai.OpenAI(api_key=os.environ["API_TOKEN"])
    # Check if a file was uploaded
    print(uploaded_file)
    df = open(uploaded_file, "rb")
    file = client.files.create(file=df,
                               purpose='assistants')

    assistant = client.beta.assistants.create(
        name=assistant_name,
        instructions=assistant_message,
        model="gpt-4-0125-preview",
        tools=[
            {
                "type": "retrieval"  # This adds the knowledge base as a tool
            }
        ],
        file_ids=[file.id])
    
    return assistant.id

# Creating the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## To create an OpenAI Assistant please fill in the following sections. Upload a file to give the Assistant knowledge and a focus on something outside of it's normal training. Then add an assistant name and message. The Assistant message should guide the model into in a role. An example would be, You are a helpful Asssitant who is knowledgable in the field of...")
    gr.Markdown("## After creating the ID head to [OpenAI_Assistant_Chat](https://huggingface.co/spaces/jadend/OpenAI_Assistant_Chat).")
    with gr.Row():
        file_input = gr.File(label="Upload your file", type="filepath")
        assistant_name = gr.Textbox(label="The Assistant's Name")
        assistant_message = gr.Textbox(label="Assistant Message")
    generate_button = gr.Button("Generate Your Assistant ID") 
    output_id = gr.Textbox(label="Your Asssistant ID", value="")
    
    generate_button.click(
        fn=create_assistant_json,
        inputs=[file_input, assistant_name, assistant_message],
        outputs=output_id
    )

if __name__ == "__main__":
    demo.launch(#enable_queue=False,
        # Creates an auth screen 
        auth=lambda u, p: user_db.get(u) == p,
        auth_message="Welcome! Enter a Username and Password"
               ).queue()