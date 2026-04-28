import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Add Phase 5 src to path
phase5_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if phase5_src not in sys.path:
    sys.path.append(phase5_src)

from backend_controller import BackendController

app = FastAPI(title="Zomato AI API")

# Configure CORS for Next.js frontend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize backend controller
data_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "phase 2", 
    "data", 
    "cleaned_restaurants.parquet"
)

try:
    controller = BackendController(data_path)
except Exception as e:
    print(f"Failed to initialize backend: {e}")
    controller = None

class RecommendRequest(BaseModel):
    location: Optional[str] = ""
    max_budget: Optional[float] = None
    cuisines: Optional[List[str]] = []
    min_rating: Optional[float] = 0.0
    user_query: Optional[str] = ""

@app.get("/api/locations")
def get_locations():
    if not controller:
        raise HTTPException(status_code=500, detail="Backend not initialized")
    try:
        locations = controller.search_engine.get_available_locations()
        return {"locations": ["Any"] + locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommend")
def get_recommendations(req: RecommendRequest):
    if not controller:
        raise HTTPException(status_code=500, detail="Backend not initialized")
    try:
        recommendations = controller.get_recommendations(
            location=req.location if req.location and req.location != "Any" else "",
            max_budget=req.max_budget,
            cuisines=req.cuisines,
            min_rating=req.min_rating,
            user_query=req.user_query
        )
        
        # Image mapping based on cuisine
        cuisine_images = {
            "italian": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&q=80&w=800",
            "chinese": "https://images.unsplash.com/photo-1552611052-33e04de081de?auto=format&fit=crop&q=80&w=800",
            "north indian": "https://images.unsplash.com/photo-1585937421612-70a0f2455f75?auto=format&fit=crop&q=80&w=800",
            "south indian": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&q=80&w=800",
            "cafe": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&q=80&w=800",
            "desserts": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&q=80&w=800",
            "fast food": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?auto=format&fit=crop&q=80&w=800",
            "continental": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&q=80&w=800",
            "default": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&q=80&w=800"
        }

        # Enrich recommendations with images
        for rec in recommendations:
            cuisine_str = str(rec.get("Cuisine", "")).lower()
            assigned_img = cuisine_images["default"]
            
            for key in cuisine_images:
                if key in cuisine_str:
                    assigned_img = cuisine_images[key]
                    break
            
            rec["Image"] = assigned_img

        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
