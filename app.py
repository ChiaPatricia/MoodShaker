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

def generate_response(prompt):
    client = openai.OpenAI(api_key=os.environ["API_TOKEN"])
    instruction = "Please generate a cocktail recipe based on the user's following preferences.\n\n"
    prompt = f"Mood: {mood}\nTaste: Sweetness {sweetness}, Sour {sour}, Savory {savory}, Bitter {bitter}\nFlavor Association: {flavor_association}\nDrinking Experience: {drinking_experience}\nLevel of Soberness: {soberness_level}\nAllergies: {allergies}\nAdditional Requests: {additional_requests}\n\nRecipe:"
    prompt = instruction + prompt

    messages=[
    {"role": "system", "content": "You are a helpful bartender assistant."},
    {"role": "user", "content": prompt}
  ]
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview", 
            messages=messages,
            max_tokens=150)
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

# Creating the Gradio interface
with gr.Blocks(css=".gradio-container {background: url('https://static.vecteezy.com/system/resources/thumbnails/030/814/051/small/wooden-table-and-blur-tropical-green-grass-background-product-display-montage-high-quality-8k-fhd-ai-generated-photo.jpg');}") as demo:
    with gr.Row():
        gr.Markdown("## MoodShaker Cocktail Generator")
        gr.Markdown("### Enter your preferences and let AI create a unique cocktail recipe for you!")
    
    with gr.Column(scale=1):
        mood = gr.Textbox(label="Mood")
        sweetness = gr.Slider(label="Sweetness", minimum=0, maximum=10)
        sour = gr.Slider(label="Sour", minimum=0, maximum=10)
        savory = gr.Slider(label="Savory", minimum=0, maximum=10)
        bitter = gr.Slider(label="Bitter", minimum=0, maximum=10)
        flavor_association = gr.CheckboxGroup(label="Flavor Association", choices=["Fruity", "Herbal", "Spicy", "Floral", "Nutty", "Woody", "Earthy"], inline=True)
        drinking_experience = gr.CheckboxGroup(label="Drinking Experience", choices=["Refreshing", "Warming", "Comforting", "Energizing", "Relaxing"], inline=True)
        soberness_level = gr.Slider(label="Level of Soberness", minimum=0, maximum=10)
        allergies = gr.Textbox(label="Allergies")
        additional_requests = gr.Textbox(label="Anything else you would like to address")
    
    with gr.Row():
        generate_button = gr.Button("Generate Your Cocktail Recipe")
        output_recipe = gr.Textbox(label="Your Cocktail Recipe", value="", readonly=True)
    
    generate_button.click(
        fn=generate_cocktail,
        inputs=[mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests],
        outputs=output_recipe
    )


# with gr.Blocks(css=".gradio-container {background: url(https://static.vecteezy.com/system/resources/thumbnails/030/814/051/small/wooden-table-and-blur-tropical-green-grass-background-product-display-montage-high-quality-8k-fhd-ai-generated-photo.jpg)}") as demo:
#     gr.Markdown("## To create an OpenAI Assistant please fill in the following sections. Upload a file to give the Assistant knowledge and a focus on something outside of it's normal training. Then add an assistant name and message. The Assistant message should guide the model into in a role. An example would be, You are a helpful Asssitant who is knowledgable in the field of...")
#     gr.Markdown("## After creating the ID head to [OpenAI_Assistant_Chat](https://huggingface.co/spaces/jadend/OpenAI_Assistant_Chat).")
#     with gr.Row():
#         # file_input = gr.File(label="Upload your file", type="filepath")
#         description = gr.Textbox(label="The User Input")
#         # chatbot = gr.Textbox(label="Chatbot Response")
#     generate_button = gr.Button("Generate Your Cocktail Recipe") 
#     output_id = gr.Textbox(label="Your Cocktail Recipe", value="")
    
#     generate_button.click(
#         fn=generate_response,
#         inputs=description,
#         outputs=output_id
#     )

if __name__ == "__main__":
    demo.launch(#enable_queue=False,
        # Creates an auth screen 
        auth_message="Welcome! Enter a Username and Password"
               ).queue()