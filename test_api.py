from google import genai
from dotenv import load_dotenv

# Load the API key from your .env file
load_dotenv()

client = genai.Client()

print("Authenticating and fetching available models...\n")

try:
    # Iterate through and print the available models
    for model in client.models.list():
        print(model.name)
    print("\nAPI Key is valid and working!")
except Exception as e:
    print(f"\nAuthentication Failed. Error: {e}")