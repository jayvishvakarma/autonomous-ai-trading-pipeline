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
            model=DEPLOYMENT_NAME,  # Important: use Deployment Name here, not model name
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis assistant. Reply only with 'positive', 'neutral', or 'negative'."
                },
                {
                    "role": "user",
                    "content": f"What is the sentiment of this text: '{text}'?"
                }
            ],
            temperature=0.0
        )

        sentiment = response.choices[0].message.content.strip().lower()

        # Map sentiment text to numerical compound score
        if sentiment == "positive":
            return 1.0
        elif sentiment == "neutral":
            return 0.0
        elif sentiment == "negative":
            return -1.0
        else:
            return 0.0  # fallback if unexpected output

    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return 0.0
