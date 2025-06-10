import os
import time
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# API configuration
API_URL = "https://api-inference.huggingface.co/models/jazzmacedo/fruits-and-vegetables-detector-36"

# Custom Exception for API Failures
class HuggingFaceAPIError(Exception):
    pass

def detect_fruit_or_vegetable(image_path: str, retries: int = 3, delay: int = 5) -> Dict[str, Any]:

    # Validate environment
    if not HUGGINGFACE_TOKEN:
        raise EnvironmentError("HUGGINGFACE_TOKEN not set in environment variables.")

    # Validate file existence
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    # Read image data
    try:
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
    except IOError as e:
        raise HuggingFaceAPIError(f"Failed to read image file: {e}")

    # Determine content type from file extension
    content_type = "image/jpeg"
    if image_path.endswith(".png"):
        content_type = "image/png"
    elif image_path.endswith(".bmp"):
        content_type = "image/bmp"
    elif image_path.endswith(".gif"):
        content_type = "image/gif"
    elif image_path.endswith(".webp"):
        content_type = "image/webp"

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": content_type
    }

    # Retry logic for API calls
    for attempt in range(retries):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                data=image_data,
                timeout=30
            )

            if response.status_code == 200:
                try:
                    result = response.json()

                    if isinstance(result, list) and len(result) > 0:
                        return {
                            "predictions": result,
                            "top_prediction": result[0]["label"],
                            "confidence": result[0]["score"]
                        }
                    elif isinstance(result, dict):
                        return {
                            "predictions": [result],
                            "top_prediction": result.get("label", "unknown"),
                            "confidence": result.get("score", 0.0)
                        }
                    else:
                        raise HuggingFaceAPIError("Unexpected API response format.")

                except (KeyError, ValueError) as e:
                    raise HuggingFaceAPIError(f"Failed to parse API response: {e}")

            elif response.status_code == 503:
                print(f"[INFO] Model is loading, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    time.sleep(delay)

            elif response.status_code == 400:
                try:
                    print("[DEBUG] 400 Error Response:", response.json())
                except Exception:
                    print("[DEBUG] 400 Error Response (non-JSON):", response.text)
                raise HuggingFaceAPIError("Bad request. Possibly malformed image or model input error.")

            elif response.status_code == 401:
                raise HuggingFaceAPIError("Authentication failed. Check your HUGGINGFACE_TOKEN.")

            elif response.status_code == 404:
                raise HuggingFaceAPIError("Model not found. Check the model name and availability.")

            else:
                try:
                    error_detail = response.json().get("error", response.text)
                except:
                    error_detail = response.text
                raise HuggingFaceAPIError(f"API error {response.status_code}: {error_detail}")

        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                raise HuggingFaceAPIError(f"Network error: {e}")
            print(f"[WARNING] Network error on attempt {attempt + 1}, retrying: {e}")
            time.sleep(delay)

    raise HuggingFaceAPIError("Model did not load in time. Please try again later.")
