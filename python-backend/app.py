from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests, os
from flask_cors import CORS
import google.generativeai as genai

# Load env
load_dotenv()

app = Flask(__name__)
CORS(app)

# API keys
news_api_key = os.getenv("NEWS_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

NEWS_API_URL = f"https://newsdata.io/api/1/latest?apikey={news_api_key}&category=technology&language=en"


@app.route("/chat-news", methods=["POST"])
def chat_news():
    try:
        user_message = request.json.get("message", "")

        # Fetch latest tech news
        resp = requests.get(NEWS_API_URL)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("results", [])[:5]

        headlines = [
            f"{i+1}. {a.get('title')} (Source: {a.get('source_name')})"
            for i, a in enumerate(articles) if a.get("title")
        ]

        # Build prompt with both news and user’s question
        prompt = (
            "Here are today’s top technology news headlines:\n\n"
            + "\n".join(headlines)
            + f"\n\nUser: {user_message}\n\n"
            "Answer as a friendly tech news assistant."+
            " Keep the answer concise and relevant to the latest news."
            " Always Answers in bulleted format if multiple points are present."
            " Limit the response to 150 words."
            " keep the sentences short and simple."
            " Always ask a new question related to technology at the end of your response."
            "If user asks other than technology, politely inform them that you can only provide information related to technology."
            
        )

        # Ask Gemini
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
