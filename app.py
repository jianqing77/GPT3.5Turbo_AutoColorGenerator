from flask import Flask, render_template, request
import openai
from dotenv import dotenv_values
import json


# set up api key using env variables
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

# flask setup
app = Flask(__name__,
            template_folder='templates',
            static_url_path="", 
            static_folder="static"
)


def response_colors(msg):
    new_content = f"Convert the following verbal description of a color palette into a list of colors: {msg}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant specializing in the creation of color palettes. "
                    "When provided with a theme, mood, or specific instructions, you will generate a color palette. "
                    "Your response should include a color palette with 2 to 8 colors, formatted as a JSON array of hexadecimal color codes with DOUBLE quote."
                    "Only give the list, no other texts"
                )
            },
            {
                "role": "user",
                "content": "Convert the following verbal description of a color palette into a list of colors: google"
            },
            {
                "role": "assistant",
                "content": '["#4285F4", "#EA4335", "#FBBC05", "#34A853", "#1A73E8"]'
            },
            {
                "role": "user",
                "content": new_content
            }
        ], 
    )
    colors = json.loads(response.choices[0].message.content) # form a python object => list
    return colors
    
# routes setup
@app.route('/palette', methods=['POST'])
def prompt_to_palette():
    # OPEN AI API COMPLETION CALL
    user_msg = request.form.get("user_msg")
    colors_res = response_colors(user_msg) # a list of colors
    return {"colors": colors_res}          # return dictionary => to write json
    

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)