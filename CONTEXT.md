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
    