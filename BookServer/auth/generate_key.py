from uuid import uuid4
from dotenv import load_dotenv, set_key
import os

def generate_and_save_api_key():
    # Load existing environment variables from .env file
    load_dotenv()

    # Generate a new API key using UUID4
    api_key = str(uuid4())

    # Save the new API key to the .env file
    env_file = '.env'
    set_key(env_file, 'API_KEY', api_key)

    print(f"New API key generated and saved to {env_file}")

    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = os.path.join(root_directory, env_file)

    if not os.path.isfile(env_file):
        open(env_file, 'w').close()

    existing_key = os.getenv('API_KEY', "")

    if existing_key:
        existing_key = existing_key.strip(',')
        new_key = f"{existing_key},{api_key}" if existing_key else api_key
    else:
        new_key = api_key

    set_key(env_file, 'API_KEY', new_key)
    print(f"API keys updated in {env_file}")

if __name__ == "__main__":
    generate_and_save_api_key()