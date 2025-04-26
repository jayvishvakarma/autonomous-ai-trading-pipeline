from openai import AzureOpenAI

# Azure OpenAI Config
client = AzureOpenAI(
    azure_endpoint="add your end point",
    api_key="add your azure OpenAI/LLM key",
    api_version="2023-12-01-preview"
)

DEPLOYMENT_NAME = "gpt-35-turbo-16k"  # Your deployed model name

def get_sentiment(text):
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment analysis model. "
                        "Given a text, reply only with a real number sentiment score between -1.0 (very negative) to +1.0 (very positive). "
                        "Do not reply with any text, just the numeric score."
                    )
                },
                {
                    "role": "user",
                    "content": f"What is the sentiment score of this text: '{text}'?"
                }
            ],
            temperature=0.0
        )

        sentiment_score = float(response.choices[0].message.content.strip())
        return round(sentiment_score, 4)  # round to 4 decimal places

    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return 0.0
