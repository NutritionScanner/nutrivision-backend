from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import food_detection, nutrition, ai_summary

app = FastAPI(
    title="NutriVision API",
    description="Food Recognition and Nutrition Analysis"
)

# List of allowed origins
origins = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",
    "exp://192.168.1.3:8081",
    "http://10.0.2.2",
    # "*"  # Allow all origins (if needed)
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Include routers
app.include_router(food_detection.router)
app.include_router(nutrition.router)
app.include_router(ai_summary.router)

@app.get("/")
def root():
    return {"message": "Welcome to NutriVision API"}
