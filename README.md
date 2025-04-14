# NutriVision Backend

NutriVision is a mobile application designed to provide nutritional insights, calorie tracking, and food detection using AI. The backend of the app is built using **FastAPI** and leverages multiple third-party APIs, including **OpenFoodFacts** and **Gemini AI**, to fetch and analyze food-related data.

## Project Structure

```
nutrivision-backend/
│── main.py                # FastAPI entry point
│── requirements.txt       # Dependencies
│── .env                   # Store API keys (Gemini, OpenFoodFacts)
│── routers/               # API endpoints
│   ├── food_detection.py  # Handles image-based food detection
│   ├── nutrition.py       # Fetches nutrition data from OpenFoodFacts
│   ├── ai_summary.py      # Generates AI-based nutrition summaries
│── services/              # Helper functions (API calls, processing)
│   ├── food_recognition.py   # Hugging Face Model logic
│   ├── openfoodfacts.py      # OpenFoodFacts API logic
│   ├── gemini.py             # Gemini AI API logic
│── models/                # Pydantic models
│   ├── food.py            # Food-related request models
│── config.py              # Load environment variables
│── static/                # Store test images (optional)
│── README.md              # Project documentation
```

## Features

- **Food Detection**: Detect fruits, vegetables, and general food items using machine learning models from Hugging Face.
- **Nutrition Data**: Fetch nutrition information for packaged food via the OpenFoodFacts API.
- **AI-based Nutrition Summaries**: Generate nutritional summaries of foods using the Gemini AI API.
- **Calorie Tracking**: Track calories and nutritional values based on food detection and summaries.

## Endpoints

### `/nutrition/{barcode}`
- **Method**: `GET`
- **Description**: Fetches nutrition information for packaged food using its barcode from OpenFoodFacts.

### `/food-detection/fruit-vegetable`
- **Method**: `POST`
- **Description**: Detects fruits and vegetables in an uploaded image using the Hugging Face food recognition model.

### `/food-detection/food-item`
- **Method**: `POST`
- **Description**: Detects general food items in an uploaded image using the Hugging Face food recognition model.

### `/ai-summary`
- **Method**: `POST`
- **Description**: Provides an AI-generated nutrition summary for a given food item using the Gemini AI API.

## Setup Instructions

### Prerequisites

Ensure you have Python 3.8+ installed.

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/nutrivision-backend.git
   cd nutrivision-backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   OPENFOODFACTS_API_KEY=your_openfoodfacts_api_key
   ```

### Running the Backend

To start the FastAPI server:

```bash
uvicorn main:app --reload
```

The app will be accessible at `http://127.0.0.1:8000`.

## Project Details

### `main.py`

The entry point for the FastAPI application. It includes the routing configuration and initialization of the app.

### `routers/`

- **food_detection.py**: Handles image uploads and detection of food items (fruits, vegetables, etc.).
- **nutrition.py**: Fetches nutrition data for food items using OpenFoodFacts.
- **ai_summary.py**: Uses Gemini AI to generate nutrition summaries for the detected food.

### `services/`

- **food_recognition.py**: Contains logic to interact with the Hugging Face food recognition models.
- **openfoodfacts.py**: Contains helper functions to interact with the OpenFoodFacts API.
- **gemini.py**: Contains functions to interact with the Gemini AI API for generating nutrition summaries.

### `models/`

- **food.py**: Contains Pydantic models for validating food-related request data.

### `config.py`

Contains the configuration for loading environment variables like API keys.

### `static/`

(Optional) Store test images for local testing.

## Dependencies

The backend relies on the following Python packages:

- **FastAPI**: Framework to build APIs quickly.
- **Uvicorn**: ASGI server for running FastAPI applications.
- **Pydantic**: Data validation and settings management.
- **Requests**: For making HTTP requests to external APIs.
- **Hugging Face Transformers**: For using food recognition models.
- **Gemini API**: AI-powered nutrition insights.

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## Testing

To test the API endpoints, you can use tools like **Postman** or **cURL** to send requests to the backend.

### Example:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/food-detection/fruit-vegetable' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path_to_your_image'
```


## Acknowledgments

- **Hugging Face**: For providing pre-trained models for food detection.
- **OpenFoodFacts**: For providing nutritional data of packaged foods.
- **Gemini AI**: For providing AI-based nutrition summaries.
