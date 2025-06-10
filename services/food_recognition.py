import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# API config
API_URL = "https://api-inference.huggingface.co/models/nateraw/food"

# Custom Exception for API errors
class HuggingFaceAPIError(Exception):
    pass

def detect_food(image_path: str, retries: int = 3, delay: int = 5) -> str:
    """
    Detects food category from image using Hugging Face API and the 'nateraw/food' model.

    Args:
        image_path (str): Path to the image file.
        retries (int): Number of retries if the model is still loading.
        delay (int): Delay between retries in seconds.

    Returns:
        str: Top predicted food label.

    Raises:
        HuggingFaceAPIError: If the API fails to respond properly.
    """
    if not HUGGINGFACE_TOKEN:
        raise EnvironmentError("HUGGINGFACE_TOKEN not found in environment.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    # Read image
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    except IOError as e:
        raise HuggingFaceAPIError(f"Failed to read image: {e}")

    # Determine content type
    content_type = "image/jpeg"
    if image_path.endswith(".png"):
        content_type = "image/png"
    elif image_path.endswith(".bmp"):
        content_type = "image/bmp"
    elif image_path.endswith(".webp"):
        content_type = "image/webp"

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": content_type
    }

    # Retry loop
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, data=image_bytes, timeout=30)

            if response.status_code == 200:
                try:
                    result = response.json()
                    if isinstance(result, list) and result:
                        return result[0]["label"]
                    else:
                        raise HuggingFaceAPIError("API returned no predictions.")
                except (KeyError, ValueError) as e:
                    raise HuggingFaceAPIError(f"Invalid API response format: {e}")

            elif response.status_code == 503:
                print(f"[INFO] Model is loading... Retrying in {delay}s (Attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    time.sleep(delay)

            elif response.status_code == 401:
                raise HuggingFaceAPIError("Unauthorized: Check your HUGGINGFACE_TOKEN.")

            elif response.status_code == 404:
                raise HuggingFaceAPIError("Model not found. Verify the model name and URL.")

            else:
                try:
                    error_detail = response.json().get("error", response.text)
                except Exception:
                    error_detail = response.text
                raise HuggingFaceAPIError(f"API Error {response.status_code}: {error_detail}")

        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                raise HuggingFaceAPIError(f"Network error: {e}")
            print(f"[WARNING] Network error on attempt {attempt + 1}, retrying: {e}")
            time.sleep(delay)

    raise HuggingFaceAPIError("Model failed to load after multiple retries.")
