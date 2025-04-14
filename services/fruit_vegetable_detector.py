import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# API configuration
API_URL = "https://api-inference.huggingface.co/models/jazzmacedo/fruits-and-vegetables-detector-36"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

# Custom Exception for API Failures
class HuggingFaceAPIError(Exception):
    pass

def detect_fruit_or_vegetable(image_path: str, retries: int = 3, delay: int = 5) -> str:
    """
    Detects whether the uploaded image is a fruit or vegetable using Hugging Face Inference API.

    Args:
        image_path (str): Path to the image.
        retries (int): Number of retries if model is loading.
        delay (int): Delay between retries in seconds.

    Returns:
        str: Predicted label.

    Raises:
        HuggingFaceAPIError: If API returns an error.
    """
    if not HUGGINGFACE_TOKEN:
        raise EnvironmentError("HUGGINGFACE_TOKEN not set in environment variables.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    for attempt in range(retries):
        response = requests.post(API_URL, headers=HEADERS, data=image_data)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0]["label"]  # Most confident prediction
            else:
                raise HuggingFaceAPIError("Empty prediction result from API.")

        elif response.status_code == 503:
            print(f"[INFO] Model is loading, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        else:
            raise HuggingFaceAPIError(f"API error {response.status_code}: {response.text}")

    raise HuggingFaceAPIError("Model did not load in time. Please try again later.")
