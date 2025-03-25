import google.generativeai as genai
import PIL.Image
import openai
import anthropic

class AIInsights:
    def __init__(self, api_key, model_choice):
        self.api_key = api_key
        self.model_choice = model_choice

        if model_choice == "Gemini":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        elif model_choice == "Claude":
            self.model = anthropic.Anthropic(api_key=self.api_key)
        elif model_choice == "OpenAI":
            openai.api_key = self.api_key

    def get_ai_insights(self, image_path, stock, market):
        image = PIL.Image.open(image_path)
        prompt = f"This is an image of stock performance for '{stock}' over the last 100 days in '{market}'. Analyze based on volume traded, closing prices, and moving averages (7 & 20-day). Should this stock be purchased or not?"

        if self.model_choice == "Gemini":
            response = self.model.generate_content([prompt, image])
            return "\n".join([part.text for candidate in response.candidates for part in candidate.content.parts])

        elif self.model_choice == "Claude":
            response = self.model.messages.create(
                model="claude-3-opus",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content

        elif self.model_choice == "OpenAI":
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512
            )
            return response["choices"][0]["message"]["content"]
