import os
import gradio as gr
import google.generativeai as genai
import random

# ✅ Securely get API key from environment variables
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("""
    ⚠️ ERROR: Gemini API Key is missing!
    Set your API key in environment variables using:
    export GEMINI_API_KEY='your-api-key-here'
    """)

# ✅ Configure Gemini API
genai.configure(api_key=gemini_api_key)

def get_joke(language):
    """Get a joke in the selected language (English or Hinglish)"""
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash-lite")

        # ✅ Random funny words for more variety
        random_word = random.choice([
            "banana", "robot", "pirate", "spaceship", "wizard", "penguin",
            "vampire", "dinosaur", "detective", "ninja", "zombie", "alien",
            "astronaut", "time traveler", "cowboy", "unicorn", "octopus",
            "squirrel", "chicken", "ghost", "superhero", "scientist",
            "teacher", "doctor", "chef", "dog", "cat", "hamster", "elephant",
            "monkey", "koala", "turtle", "cactus", "caveman", "jellyfish",
            "kangaroo", "mermaid", "gnome", "fairy", "dragon", "owl",
            "skeleton", "t-rex", "werewolf", "bigfoot", "genie", "goldfish",
            "duck", "giraffe", "parrot", "sloth", "teddy bear", "panda",
            "penguin", "robot", "unicorn", "vampire", "zombie", "alien"
        ])
        
        # ✅ Language-based prompt selection
        if language == "English":
            prompt = f"Tell me a funny, unique joke about {random_word}. Keep it in simple, clear English."
        else:  # Hinglish (Mix of Hindi & English)
            prompt = f"Ek funny joke sunao {random_word} ke baare mein, jo thoda Hindi aur thoda English mila ho. Thoda desi touch ho!"

        response = model.generate_content(
            prompt, 
            generation_config={
                "temperature": 1.2,  # More creativity
                "top_p": 0.9,  # Diverse responses
                "max_output_tokens": 100  # Limit response length
            }
        )
        
        return response.text if response and hasattr(response, 'text') else "⚠️ No joke found."
    
    except Exception as e:
        return f"⚠️ Error generating joke: {str(e)}"


def rate_joke(feedback):
    """Handle user feedback"""
    return f"Thanks for your feedback! You rated: {feedback}"

# ✅ Improved Gradio UI with a dark striped background
with gr.Blocks(css=""" 
    body {
        background-color: #000000;  /* Changed to Black */
    }
    h1, h3 {
        font-family: Arial, sans-serif;
        text-align: center;
        color: white;
    }
    #joke-box {
        background-color: #D3D3D3;
        color: white;
        border-radius: 10px;
        font-size: 32px;  /* Increased size */
        font-weight: bold;  /* Bold text */
        font-family: 'Comic Sans MS', cursive;  /* Fun font */
        padding: 20px;
    }
    #joke-button {
        background: #8A2BE2;  /* Purple */
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        border-radius: 10px;
        padding: 10px;
    }
    #feedback-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    .funny-button {
        background-color: #00C853;  /* Bright Green */
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        border-radius: 10px;
        padding: 10px;
    }
    .not-funny-button {
        background-color: #D32F2F;  /* Deep Red */
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        border-radius: 10px;
        padding: 10px;
    }
""") as app:

    gr.Markdown("""
    <div style="text-align: center; font-family: Arial, sans-serif;">
        <h1 style="font-size: 2.8em; font-weight: bold;">
            🤣 AI'S GOT LATENT 🤣
        </h1>
        <h3 style="font-size: 2em;">
            Don't worry only family friendly jokes!😉
        </h3>
    </div>
    """)

    with gr.Column(elem_id="main-container", scale=1, min_width=1000):
        
        # ✅ Language selection dropdown
        language_dropdown = gr.Dropdown(
            choices=["English", "Hinglish"], 
            value="English", 
            label="Select Joke Language"
        )

        # ✅ Output box
        joke_output = gr.Textbox(
            placeholder="Your joke will appear here...",
            interactive=False,
            lines=5,
            show_label=False,
            elem_id="joke-box"
        )

        # ✅ Joke button (Purple)
        joke_button = gr.Button(
            "🎲 Generate a Joke", variant="primary",
            elem_id="joke-button"
        )

    gr.Markdown("""
    <div style="text-align: center; font-size: 2em; margin-top: 20px; color: white;">
        <strong>Did you like this joke?</strong>
    </div>
    """)

    with gr.Row(elem_id="feedback-buttons", equal_height=True):
        thumbs_up = gr.Button("👍 Funny!", elem_classes=["funny-button"])  # Green
        thumbs_down = gr.Button("👎 Not Funny", elem_classes=["not-funny-button"])  # Red

    feedback_output = gr.Textbox(
        label="Feedback",
        interactive=False,
        visible=True,
        elem_id="feedback-box"
    )

    # ✅ Button click now includes language selection
    joke_button.click(get_joke, inputs=language_dropdown, outputs=joke_output)
    thumbs_up.click(lambda: rate_joke("👍 Funny!"), outputs=feedback_output)
    thumbs_down.click(lambda: rate_joke("👎 Not Funny"), outputs=feedback_output)



# ✅ Secure launch configuration
if __name__ == "__main__":
    app.launch(
        share=True,
        debug=False
    )