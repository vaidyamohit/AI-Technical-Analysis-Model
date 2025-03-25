import google.generativeai as genai
import PIL.Image
import openai
import anthropic

class AIInsights:
    def __init__(self, api_key, model_choice):
        self.api_key = api_key
        self.model_choice = model_choice
'''
        if model_choice == "Gemini":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        elif model_choice == "Claude":
            self.model = anthropic.Anthropic(api_key=self.api_key)
        elif model_choice == "OpenAI":
            openai.api_key = self.api_key
'''
        if model_choice == "Gemini":
            ai_insights_obj = AIInsights(AIzaSyAVi1v80vt41mTjZED6BaMs5-74HKFkSk0, model_choice)
        elif model_choice == "OpenAI":
            ai_insights_obj = AIInsights(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, model_choice)
        elif model_choice == "Claude":
            ai_insights_obj = AIInsights(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, model_choice)


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
