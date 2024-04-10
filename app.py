import os
import gradio as gr
import json
import re
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

def generate_cocktail(mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests):
    client = openai.OpenAI(api_key=os.environ["API_TOKEN"])
    instruction = "Please provide a cocktail recipe given the mood and preference of the user.\n\n"
    user_prompt = f"Mood: {mood}\nTaste: Sweetness {sweetness}/10, Sour {sour}/10, Savory {savory}/10, Bitter {bitter}/10\nFlavor Association: {flavor_association}\nDrinking Experience: {drinking_experience}\nLevel of Soberness: {soberness_level}\nAllergies: {allergies}\nAdditional Requests: {additional_requests}\n\nMake sure to avoid all allergic ingredients.\n\n"
    output_format = "Please strictly follow this output format:\n\nCocktail Name:[name]\nQuote:[one sentence quote related to the cocktail and the mood description]\nIngredients:[ingredient 1]\n[ingredient 2]\n...\nInstruction:1. [step 1]\n2. [step 2]\n...\nNotes:[notes]"
    prompt = instruction + user_prompt + output_format

    messages=[
    {"role": "system", "content": "You are a helpful bartender assistant."},
    {"role": "user", "content": prompt}
  ]
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview", 
            messages=messages,
            max_tokens=1024)
        name, quote, ingredients, instruction, notes = extract_info(response.choices[0].message.content)
        return format_cocktail_output(name, quote, ingredients, instruction, notes)
    except Exception as e:
        return f'<p style="color: white; font-size: 20px;">{str(e)}</p>'

def extract_info(output_text):
    pattern = r"Cocktail Name:(.*?)Quote:(.*?)Ingredients:(.*?)Instruction:(.*?)Notes:(.*?)$"
    match = re.search(pattern, output_text, re.DOTALL)
    if match:
        name = match.group(1)
        quote = match.group(2)
        ingredients = match.group(3).strip().replace('\n', '<br>')
        instruction = match.group(4).strip().replace('\n', '<br>')
        notes = match.group(5).strip()
        return name, quote, ingredients, instruction, notes
    else:
        return None
        
def format_cocktail_output(name, quote, ingredients, instruction, notes):
    # Construct the HTML output
    html_output = f'''
    <div style="text-align: center; font-family: 'Verdana', sans-serif; color: white;">
        <h1 style="font-size: 48px; color: white;">{name}</h1>
        <p style="font-size: 36px; margin-top: -15px; font-style: italic; color: white;">{quote}</p>
        <p style="font-size: 20px; color: white;">
            <strong style="color: white;">Ingredients:</strong><br>
            {ingredients}<br>
            <strong style="color: white;">Instruction:</strong><br>
            {instruction}<br>
            <strong style="color: white;">Notes:</strong><br>
            {notes}<br>
        </p>
    </div>
    '''
    return html_output

# Creating the Gradio interface
with gr.Blocks(css='''
        .gradio-container {
            background: url('https://images.unsplash.com/photo-1514361726087-38371321b5cd?q=80&w=2370&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        }
        .gradio-textbox {
            opacity: 0.5; /* Change the opacity of the textbox */
        }
        .generate-button {
            background: linear-gradient(to right, #F0E68C, #E0FFFF, #FF6347);
            color: black;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            text-transform: uppercase;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .generate-button:hover {
            background: linear-gradient(to right, #E0FFFF, #FF6347, #F0E68C);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
    ''') as demo:
    with gr.Row():
        gr.HTML("""
        <h2 style='text-align: center; color: white;'>MoodShaker Cocktail Generator</h2>
        <p style='text-align: center; color: white;'>Enter your preferences and let AI create a unique cocktail recipe for you!</p>
        """)
        
    with gr.Row():
        mood = gr.Textbox(label="Mood")
        flavor_association = gr.CheckboxGroup(label="Flavor Association", choices=["Fruity", "Herbal", "Spicy", "Floral", "Nutty", "Woody", "Earthy"])
        drinking_experience = gr.CheckboxGroup(label="Drinking Experience", choices=["Refreshing", "Warming", "Comforting", "Energizing", "Relaxing"])
        
    with gr.Row():
        sweetness = gr.Slider(label="Sweetness", minimum=0, maximum=10, elem_id="slider-sweetness")
        sour = gr.Slider(label="Sour", minimum=0, maximum=10, elem_id="slider-sour")
        savory = gr.Slider(label="Savory", minimum=0, maximum=10, elem_id="slider-savory")
        bitter = gr.Slider(label="Bitter", minimum=0, maximum=10, elem_id="slider-bitter")
        soberness_level = gr.Slider(label="Level of Soberness", minimum=0, maximum=10, elem_id="slider-soberness_level")

    # with gr.Row():
    #     flavor_association = gr.CheckboxGroup(label="Flavor Association", choices=["Fruity", "Herbal", "Spicy", "Floral", "Nutty", "Woody", "Earthy"])
    #     drinking_experience = gr.CheckboxGroup(label="Drinking Experience", choices=["Refreshing", "Warming", "Comforting", "Energizing", "Relaxing"])
    with gr.Row():
        allergies = gr.Textbox(label="Allergies", scale=2)
        additional_requests = gr.Textbox(label="Anything else you would like to address", scale=2)
        generate_button = gr.Button("Generate Your Cocktail Recipe", scale=1, elem_classes=["generate-button"])

    with gr.Row():
        output_recipe = gr.HTML(label="Your Cocktail Recipe")
    
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