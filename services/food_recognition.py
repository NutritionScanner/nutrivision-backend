import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# API config
API_URL = "https://api-inference.huggingface.co/models/nateraw/food"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

# Custom Exception for API errors
class HuggingFaceAPIError(Exception):
    pass

def detect_food(image_path: str, retries: int = 3, delay: int = 5) -> str:
    """
    Detects food category from image using Hugging Face API and the 'nateraw/food' model.

    Args:
        image_path (str): Path to the image file.
        retries (int): Number of times to retry if model is still loading.
        delay (int): Delay between retries (seconds).

    Returns:
        str: Predicted food label.

    Raises:
        HuggingFaceAPIError: If the API fails to respond properly.
    """
    if not HUGGINGFACE_TOKEN:
        raise EnvironmentError("HUGGINGFACE_TOKEN not found in environment.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    for attempt in range(retries):
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0]["label"]  # Top prediction
            else:
                raise HuggingFaceAPIError("API returned empty results.")

        elif response.status_code == 503:
            print(f"[INFO] Model is loading... Retrying in {delay}s (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        else:
            raise HuggingFaceAPIError(f"API Error {response.status_code}: {response.text}")

    raise HuggingFaceAPIError("Model failed to load after multiple retries.")
