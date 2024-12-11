import os
import streamlit as st
import google.generativeai as genai
import time

# Load environment variables from a .env file


# Configure the generative AI model with the Google API key
genai.configure(api_key='AIzaSyBXVIrsWIiis8CjoEc7H2AYSrMZE4IBp8E')

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Create a GenerativeModel instance with 'gemini-pro' as the model type
llm = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)


def match_ingredients(user_ingredients, dietary_preferences=None):
    """Matches ingredients with recipes using Gemini Pro."""
    prompt_template = f"Find a delicious recipe using these ingredients: {', '.join(user_ingredients)}."
    if dietary_preferences:
        prompt_template += f" Dietary preferences: {dietary_preferences}."

    response = llm.generate_content(prompt_template)
    return response.text


# Streamlit UI
st.markdown("<style>"
            "h1 {text-align: center; color: #4CAF50;}"
            "h3 {text-align: center; color: #333;}"
            "input {border-radius: 5px; padding: 10px; border: 1px solid #ccc; width: 80%; margin: 10px auto; display: block;}"
            "select {border-radius: 5px; padding: 10px; border: 1px solid #ccc; width: 80%; margin: 10px auto; display: block;}"
            "button {background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;}"
            "button:hover {background-color: #45a049;}"
            ".recipe-box {border: 2px solid #4CAF50; border-radius: 10px; padding: 10px; background-color: #f9f9f9; margin-top: 20px;}"
            ".error-message {color: red; text-align: center;}"
            "</style>", unsafe_allow_html=True)

st.title("🍽 Recipe Generator")
st.markdown("<h3>Generate a recipe based on the ingredients you have!</h3>", unsafe_allow_html=True)

user_ingred = st.text_input("Enter your ingredients (comma-separated):")
dietary_options = st.selectbox("Dietary Preferences (Optional):", [None, "Vegetarian", "Non-Vegan", "Gluten-Free"])
submit_button = st.button("Suggest me recipe")

if submit_button:
    if user_ingred:
        user_ingredients = [ingredient.strip().lower() for ingredient in user_ingred.split(",")]

        # Display a progress bar
        progress_bar = st.progress(0)

        # Simulate progress while waiting for the response
        for percent_complete in range(100):
            time.sleep(0.05)  # Simulate time taken for processing
            progress_bar.progress(percent_complete + 1)

        # Generate the recipe
        recipe = match_ingredients(user_ingredients, dietary_preferences=dietary_options)

        # Clear the progress bar
        progress_bar.empty()

        # Display the recipe using HTML for better formatting
        st.markdown("<h3>Here’s your recipe:</h3>", unsafe_allow_html=True)
        if recipe:
            st.markdown(f"<div class='recipe-box'><strong>Recipe:</strong> <p>{recipe}</p></div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='error-message'><strong>No Recipe Found.</strong> Please try different ingredients.</div>",
                unsafe_allow_html=True)