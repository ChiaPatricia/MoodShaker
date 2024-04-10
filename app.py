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

def play_music():
    music_path = "RPReplay_Final1712757356.mp3"
    return music_path, gr.update(visible=True)
    
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
        return format_cocktail_output(name, quote, ingredients, instruction, notes),True
    except Exception as e:
        return f'<p style="color: white; font-size: 20px;">{str(e)}</p>'
    


def extract_info(output_text):
    pattern = r"Cocktail Name:(.*?)Quote:(.*?)Ingredients:(.*?)Instruction:(.*?)Notes:(.*?)$"
    match = re.search(pattern, output_text, re.DOTALL)
    if match:
        name = match.group(1)
        quote = match.group(2)
        ingredients = match.group(3).replace('\n', '<br>')
        instruction = match.group(4).replace('\n', '<br>')
        notes = match.group(5)
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
        .centered-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: -20px;
            max-width: 500px; /* Maximum width of the image */
            width: 100%;
        }
        .custom-input {
            background: yellow; /* Or any color you'd like */
            color: #333; /* Text color */
            padding: 10px; /* Padding inside the input */
            border: 2px solid #ddd; /* Border color */
            border-radius: 5px; /* Rounded corners */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            transition: all 0.3s ease; /* Smooth transition for interactions */
        } 
        .custom-input:focus {
            border-color: #F0E68C; /* Highlight color when the input is focused */
            box-shadow: 0 0 8px rgba(240, 230, 140, 0.8); /* Glow effect on focus */
        }
        .custom-checkbox-group {
            background: yellow;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .custom-checkbox-group input[type="checkbox"] + label {
            margin-right: 10px; /* Space between checkboxes */
            cursor: pointer; /* Mouse pointer changes to indicate clickable area */
        }
        .custom-checkbox-group input[type="checkbox"]:checked + label {
            color: #FF6347; /* Text color when checkbox is checked */
            font-weight: bold;
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
            outline: none; /* Removes the outline on focus for some browsers */
        }
        .generate-button:hover, .generate-button:active {
            background: linear-gradient(to right, #E0FFFF, #FF6347, #F0E68C);
            /* Combines the glow from each color in the gradient */
            box-shadow: 
              0 0 15px rgba(240, 230, 140, 0.7), 
              0 0 25px rgba(240, 230, 140, 0.7),
              0 0 15px rgba(224, 255, 255, 0.7),
              0 0 25px rgba(224, 255, 255, 0.7),
              0 0 15px rgba(255, 99, 71, 0.7),
              0 0 25px rgba(255, 99, 71, 0.7);
            transform: translateY(2px); /* Optional: Slightly push the button down on active */
        }
        .generate-button:active {
            /* You may want to add an extra inset shadow to give a sense of depth when clicked */
            box-shadow: 
              0 0 15px rgba(240, 230, 140, 0.7), 
              0 0 25px rgba(240, 230, 140, 0.7),
              0 0 15px rgba(224, 255, 255, 0.7),
              0 0 25px rgba(224, 255, 255, 0.7),
              0 0 15px rgba(255, 99, 71, 0.7),
              0 0 25px rgba(255, 99, 71, 0.7),
              0 0 20px rgba(30, 255, 255, 0.5) inset;
        }

    ''') as demo:

    with gr.Row():
        gr.HTML('''
        <div style="text-align: center; margin: 0;">
            <img src="https://huggingface.co/spaces/WhartonHackAIthon/MoodShaker/resolve/main/MoodShaker_Slogan.png" alt="MoodShaker Cocktail Generator" class="centered-image">
        </div>
        ''')
        # gr.HTML('''
        # <h2 style='text-align: center; color: white;'>MoodShaker Cocktail Generator</h2>
        # <p style='text-align: center; color: white;'>Enter your preferences and let AI create a unique cocktail recipe for you!</p>
        # ''')
        
    with gr.Row():
        # mood = gr.HTML('''
        # <div class="mood-input">
        #   <input type="text" class="gradio-textbox" label="Mood">
        #   <span></span>
        # </div>
        # ''')
        mood = gr.Textbox(label="How are you feeling today?", elem_classes=["custom-input"])
        flavor_association = gr.CheckboxGroup(label="Flavor Association", choices=["Fruity", "Herbal", "Spicy", "Floral", "Nutty", "Woody", "Earthy"], elem_classes=["custom-checkbox-group"])
        drinking_experience = gr.CheckboxGroup(label="Drinking Experience", choices=["Refreshing", "Warming", "Comforting", "Energizing", "Relaxing"], elem_classes=["custom-checkbox-group"])
        
    with gr.Row():
        sweetness = gr.Slider(label="Sweetness", minimum=0, maximum=10, elem_id="slider-sweetness")
        sour = gr.Slider(label="Sour", minimum=0, maximum=10, elem_id="slider-sour")
        savory = gr.Slider(label="Savory", minimum=0, maximum=10, elem_id="slider-savory")
        bitter = gr.Slider(label="Bitter", minimum=0, maximum=10, elem_id="slider-bitter")
        soberness_level = gr.Slider(label="Level of Soberness", minimum=0, maximum=10, value=10, elem_id="slider-soberness_level")

    # with gr.Row():
    #     flavor_association = gr.CheckboxGroup(label="Flavor Association", choices=["Fruity", "Herbal", "Spicy", "Floral", "Nutty", "Woody", "Earthy"])
    #     drinking_experience = gr.CheckboxGroup(label="Drinking Experience", choices=["Refreshing", "Warming", "Comforting", "Energizing", "Relaxing"])
    with gr.Row():
        allergies = gr.Textbox(label="Allergies", scale=2)
        additional_requests = gr.Textbox(label="Anything else you would like to address", scale=2)
        generate_button = gr.Button("Generate Your Cocktail Recipe", scale=1, elem_classes=["generate-button"])

    with gr.Row():
        output_recipe = gr.HTML(label="Your Cocktail Recipe")

    output_recipe = gr.HTML(label="Your Cocktail Recipe")


    #modified 
    # generate_button.click(
    #     fn=generate_cocktail,
    #     inputs=[mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests],
    #     outputs=[output_recipe, play_button]
    # )

    play_button = gr.Button("Play Background Music", visible=False)  # Initially not visible
    background_music = gr.Audio(label="Background Music", autoplay=True, visible=False)  # Initially not visible

    def on_generate_click(*args):
        recipe, show_play_button = generate_cocktail(*args)
        return recipe, gr.update(visible=show_play_button)
    

    generate_button.click(
        fn=on_generate_click,
        inputs=[mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests],
        outputs=[output_recipe, play_button]
    )
    
    play_button.click(fn=play_music, inputs=[], outputs=[background_music, background_music])



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