import os
import gradio as gr
import json
import re
from datetime import datetime
import openai
# from pyppeteer import launch
# import tempfile

user_db = { 
           os.environ["username"]: os.environ["password"],
          }

music_files = [
    "RPReplay_Final1712757356.mp3",
    "RPReplay_Final1712801927.mp3",
    "RPReplay_Final1712802362.mp3",
    "RPReplay_Final1712802406.mp3",
    "RPReplay_Final1712757356.mp3",
    "RPReplay_Final1712802448.mp3",
    "RPReplay_Final1712802599.mp3"
]

# Function to play background music
def play_music():
    """Returns the path to the music file and makes the audio player visible."""
    music_path = random.choice(music_files)
    return music_path, gr.update(visible=True)


# Main function to generate a cocktail recipe based on user preferences
def generate_cocktail(mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests):
    """Generates a cocktail recipe using OpenAI's GPT-4 based on user input."""
    client = openai.OpenAI(api_key=os.environ["API_TOKEN"])
    instruction = "Please provide a cocktail recipe given the mood and preference of the user.\n\n"
    user_prompt = f"Mood: {mood}\nTaste: Sweetness {sweetness}/10, Sour {sour}/10, Savory {savory}/10, Bitter {bitter}/10\nFlavor: {flavor_association}\nDrinking Experience: {drinking_experience}\nLevel of Soberness: {soberness_level}\nAllergies: {allergies}\nAdditional Requests: {additional_requests}\n\nMake sure to avoid all allergic ingredients.\n\n"
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
        return format_cocktail_output(name, quote, ingredients, instruction, notes), True
    except Exception as e:
        return f'<p style="color: white; font-size: 20px;">{str(e)}</p>'

# Extract information from the response generated by OpenAI
def extract_info(output_text):
    """Extracts the cocktail recipe information from the response text."""
    pattern = r"Cocktail Name:(.*?)Quote:(.*?)Ingredients:(.*?)Instruction:(.*?)Notes:(.*?)$"
    match = re.search(pattern, output_text, re.DOTALL)
    if match:
        name = match.group(1).strip()
        quote = match.group(2).strip()
        ingredients = match.group(3).strip().replace('\n', '<br>')
        instruction = match.group(4).strip().replace('\n', '<br>')
        notes = match.group(5).strip()
        return name, quote, ingredients, instruction, notes
    else:
        return None

# Format the cocktail recipe for display
def format_cocktail_output(name, quote, ingredients, instruction, notes):
    """Formats the cocktail recipe into HTML for display."""
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

# def save_as_pdf(html_content):
#     """Converts HTML content to PDF, encodes it in base64, and returns a download link."""
#     html_path = "output_recipe.html"
#     pdf_path = "output_recipe.pdf"
    
#     # Write the HTML content to a temporary file
#     with open(html_path, 'w') as f:
#         f.write(html_content)
    
#     # Convert HTML to PDF
#     pdfkit.from_file(html_path, pdf_path)
    
#     # Encode the PDF file in base64
#     with open(pdf_path, "rb") as pdf_file:
#         encoded_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
    
#     # Create a Data URL for the PDF
#     pdf_data_url = f"data:application/pdf;base64,{encoded_pdf}"
    
#     # Return HTML anchor tag for the download link
#     return f'<a href="{pdf_data_url}" download="CocktailRecipe.pdf" style="color: white; font-size: 20px;">Download PDF</a>'

# def generate_pdf_from_html(html_content):
#     browser = launch()
#     page = browser.newPage()
    
#     page.setContent(html_content)
    
#     # Create a temporary file to save the PDF
#     with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
#         pdf_path = tmp_file.name
    
#         page.pdf({'path': pdf_path, 'format': 'A4'})
    
#     # Close browser
#     browser.close()
    
#     # Generate URL for the temporary PDF file
#     pdf_url = f'file://{pdf_path}'
    
#     return pdf_url, True
        
with open('style.css', 'r') as file:
    css_styles = file.read()

# Creating the Gradio interface
with gr.Blocks(css=css_styles) as MoodShaker:
    with gr.Row():
        gr.HTML('''
        <div style="text-align: center; margin: 0;">
            <img src="https://huggingface.co/spaces/WhartonHackAIthon/MoodShaker/resolve/main/MoodShaker_Slogan.png" alt="MoodShaker Cocktail Generator" class="centered-image">
        </div>
        ''')
        
    with gr.Row():
        mood = gr.Textbox(label="How are you feeling today?", elem_classes=["custom-input"])
        flavor_association = gr.CheckboxGroup(label="Flavor", choices=["Fruity", "Herbal", "Spicy", "Floral", "Nutty", "Woody", "Earthy"], elem_classes=["custom-checkbox-group1"])
        drinking_experience = gr.CheckboxGroup(label="Drinking Experience", choices=["Refreshing", "Warming", "Comforting", "Energizing", "Relaxing"], elem_classes=["custom-checkbox-group2"])
        
    with gr.Row():
        sweetness = gr.Slider(label="Sweetness", minimum=0, maximum=10, elem_id="slider-sweetness",elem_classes=["slider-sweetness"])
        sour = gr.Slider(label="Sour", minimum=0, maximum=10, elem_id="slider-sour", elem_classes=["slider-sour"])
        savory = gr.Slider(label="Savory", minimum=0, maximum=10, elem_id="slider-savory", elem_classes=["slider-savory"])
        bitter = gr.Slider(label="Bitter", minimum=0, maximum=10, elem_id="slider-bitter", elem_classes=["slider-bitter"])
        soberness_level = gr.Slider(label="Level of Soberness", minimum=0, maximum=10, value=10, elem_id="slider-soberness_level", elem_classes=["slider-soberness_level"])

    with gr.Row():
        allergies = gr.Textbox(label="Allergies", scale=6, elem_classes=["custom-input1"])
        additional_requests = gr.Textbox(label="Anything else you would like to address", scale=6, elem_classes=["custom-input2"])
        generate_button = gr.Button("Generate Your Cocktail Recipe", scale=3, elem_classes=["generate-button"])
        clear_button = gr.Button("Clear", scale=1)

    with gr.Row():
        output_recipe = gr.HTML(label="Your Cocktail Recipe")

    play_button = gr.Button("Play Music", visible=False, elem_classes=["generate-button"], scale=1)  # Initially not visible
    background_music = gr.Audio(label="Background Music", autoplay=True, visible=False, scale=4)  # Initially not visible

    # with gr.Row():
    #     save_pdf_button = gr.Button("Download Recipe as PDF", visible=False)
    #     pdf_download_link = gr.File(label="Download Link", visible=False)  # For displaying the PDF download link

    def on_generate_click(*args):
        recipe, show_play_button = generate_cocktail(*args)
        return recipe, gr.update(visible=show_play_button), gr.update(visible=show_save_button)

    def reset():
        return "", 0, 0, 0, 0, [], [], 10, "", "", "", gr.update(visible=False), gr.update(visible=False)
        
    generate_button.click(
        fn=on_generate_click,
        inputs=[mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests],
        outputs=[output_recipe, play_button]
    )
    
    play_button.click(fn=play_music, inputs=[], outputs=[background_music, background_music])

    # save_pdf_button.click(fn=generate_pdf_from_html, inputs=[output_recipe], outputs=[pdf_download_link, pdf_download_link])
    
    clear_button.click(fn=reset, inputs=[], outputs=[mood, sweetness, sour, savory, bitter, flavor_association, drinking_experience, soberness_level, allergies, additional_requests, output_recipe, play_button, background_music])
        
if __name__ == "__main__":
    MoodShaker.launch(#enable_queue=False,
        # Creates an auth screen 
        auth=lambda u, p: user_db.get(u) == p,
        auth_message="Welcome to MoodShaker! Enter a Username and Password"
               ).queue()
