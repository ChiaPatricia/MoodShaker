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

def generate_cocktail(prompt, mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests):
    client = openai.OpenAI(api_key=os.environ["API_TOKEN"])
    instruction = "Please provide a cocktail recipe given the mood and preference of the user.\n\n"
    user_prompt = f"Mood: {mood}\nTaste: Sweetness {sweetness}/10, Sour {sour}/10, Savory {savory}/10, Bitter {bitter}/10\nFlavor Association: {flavor_association}\nDrinking Experience: {drinking_experience}\nLevel of Soberness: {soberness_level}\nAllergies: {allergies}\nAdditional Requests: {additional_requests}\n\nMake sure to avoid all allergic ingredients.\n\nRecipe:"
    prompt = instruction + user_prompt

    messages=[
    {"role": "system", "content": "You are a helpful bartender assistant."},
    {"role": "user", "content": prompt}
  ]
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview", 
            messages=messages,
            max_tokens=1024)
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

# Creating the Gradio interface
with gr.Blocks(css='''
        .gradio-container {
            background: url('https://images.unsplash.com/photo-1514361726087-38371321b5cd?q=80&w=2370&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        }
        .gradio-textbox {
            opacity: 0.5; /* Change the opacity of the textbox */
        }
        .gradio-markdown {
            color: white; /* Change text color to white */
            font-size: 30px;
        }
        .slider-sweetness::-webkit-slider-thumb { background: #FAD02E; }
        .slider-sour::-webkit-slider-thumb { background: #4CAF50; }
        .slider-savory::-webkit-slider-thumb { background: #795548; }
        .slider-bitter::-webkit-slider-thumb { background: #F44336; }
        .slider-soberness_level::-webkit-slider-thumb { background: #2196F3; }
        .output_text { color: white !important; } /* Ensuring output text is white */
    ''') as demo:
    with gr.Row():
        gr.HTML("""
        <h2 style='text-align: center; color: white;'>MoodShaker Cocktail Generator</h2>
        <p style='text-align: center; color: white;'>Enter your preferences and let AI create a unique cocktail recipe for you!</p>
        """)
        
    with gr.Row():
        mood = gr.Textbox(label="Mood")
        
    with gr.Row():
        sweetness = gr.Slider(label="Sweetness", minimum=0, maximum=10, element_id="slider-sweetness")
        sour = gr.Slider(label="Sour", minimum=0, maximum=10, element_id="slider-sour")
        savory = gr.Slider(label="Savory", minimum=0, maximum=10, element_id="slider-savory")
        bitter = gr.Slider(label="Bitter", minimum=0, maximum=10, element_id="slider-bitter")
        soberness_level = gr.Slider(label="Level of Soberness", minimum=0, maximum=10, element_id="slider-soberness_level")

    with gr.Row():
        flavor_association = gr.CheckboxGroup(label="Flavor Association", choices=["Fruity", "Herbal", "Spicy", "Floral", "Nutty", "Woody", "Earthy"])
        drinking_experience = gr.CheckboxGroup(label="Drinking Experience", choices=["Refreshing", "Warming", "Comforting", "Energizing", "Relaxing"])
    with gr.Row():
        allergies = gr.Textbox(label="Allergies")
        additional_requests = gr.Textbox(label="Anything else you would like to address")
        
    with gr.Row():
        generate_button = gr.Button("Generate Your Cocktail Recipe")

    with gr.Row():
        output_recipe = gr.Markdown(label="Your Cocktail Recipe")
    
    generate_button.click(
        fn=generate_cocktail,
        inputs=[mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests],
        outputs=output_recipe
    )


        # sweetness .range-slider {background: #FAD02E;}
        # sour .range-slider {background: #4CAF50;}
        # savory .range-slider {background: #795548;}
        # bitter .range-slider {background: #F44336;}
        # soberness_level .range-slider {background: #2196F3;}

        
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