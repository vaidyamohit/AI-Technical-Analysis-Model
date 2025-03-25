import openai
import requests

class AIInsights:
    def __init__(self, api_key, model_choice):
        self.api_key = api_key
        self.model_choice = model_choice

    def get_analysis(self, stock_symbol):
        if self.model_choice == "Gemini":
            return self._get_gemini_analysis(stock_symbol)
        elif self.model_choice == "OpenAI":
            return self._get_openai_analysis(stock_symbol)
        elif self.model_choice == "Claude":
            return self._get_claude_analysis(stock_symbol)
    
    def _get_gemini_analysis(self, stock_symbol):
        url = "https://api.google.com/gemini/ai"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"query": f"Technical analysis of {stock_symbol}"}
        response = requests.post(url, json=payload, headers=headers)
        return response.json().get("analysis", "No analysis available.")

    def _get_openai_analysis(self, stock_symbol):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": f"Provide a technical analysis of {stock_symbol}."}]
        )
        return response["choices"][0]["message"]["content"]

    def _get_claude_analysis(self, stock_symbol):
        url = "https://api.anthropic.com/v1/complete"
        headers = {"x-api-key": self.api_key}
        payload = {"prompt": f"Technical analysis of {stock_symbol}"}
        response = requests.post(url, json=payload, headers=headers)
        return response.json().get("completion", "No analysis available.")
