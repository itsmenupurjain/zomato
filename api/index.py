from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Add the project root and source directories to path
import os
import sys

# Vercel's task root is /var/task
project_root = os.getcwd()
src_path = os.path.join(project_root, "source", "phase_5", "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Debug: Print path to Vercel logs
print(f"DEBUG: Project Root: {project_root}")
print(f"DEBUG: Source Path: {src_path}")
print(f"DEBUG: System Path: {sys.path}")

try:
    from backend_controller import BackendController
except ImportError as e:
    print(f"DEBUG: Failed to import backend_controller: {e}")
    # Try one more relative fallback
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "source", "phase_5", "src"))
    from backend_controller import BackendController

app = FastAPI()

# Initialize controller with the data path
data_path = os.path.join(project_root, "source", "phase_2", "data", "cleaned_restaurants.parquet")
controller = None

def get_controller():
    global controller
    if controller is None:
        filename = "vercel_restaurants.parquet"
        target_path = None
        
        # Try standard path
        p1 = os.path.join(project_root, "source", "phase_2", "data", filename)
        if os.path.exists(p1):
            target_path = p1
        
        # Deep search fallback
        if not target_path:
            for root, dirs, files in os.walk(project_root):
                if filename in files:
                    target_path = os.path.join(root, filename)
                    break
        
        if not target_path:
            raise Exception(f"Critical: Database file '{filename}' not found in project.")
            
        controller = BackendController(target_path)
    return controller

class RecommendRequest(BaseModel):
    location: Optional[str] = ""
    max_budget: Optional[float] = None
    cuisines: Optional[List[str]] = []
    min_rating: Optional[float] = 0.0
    user_query: Optional[str] = ""

@app.get("/api/locations")
def get_locations():
    try:
        ctrl = get_controller()
        locations = ctrl.search_engine.get_available_locations()
        return {"locations": ["Any"] + locations}
    except Exception as e:
        return {"locations": ["Any", "BTM", "Indiranagar", "Koramangala"], "error": str(e)}

@app.post("/api/recommend")
def get_recommendations(req: RecommendRequest):
    try:
        ctrl = get_controller()
        recommendations = ctrl.get_recommendations(
            location=req.location if req.location and req.location != "Any" else "",
            max_budget=req.max_budget,
            cuisines=req.cuisines,
            min_rating=req.min_rating,
            user_query=req.user_query
        )
        
        # Unique Image logic
        cuisine_images = {
            "italian": "https://images.unsplash.com/photo-1551183053-bf91a1d81141",
            "chinese": "https://images.unsplash.com/photo-1552611052-33e04de081de",
            "north indian": "https://images.unsplash.com/photo-1585937421612-70a0f2455f75",
            "south indian": "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
            "cafe": "https://images.unsplash.com/photo-1509042239860-f550ce710b93",
            "desserts": "https://images.unsplash.com/photo-1551024601-bec78aea704b",
            "fast food": "https://images.unsplash.com/photo-1561758033-d89a9ad46330",
            "default": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
        }

        for rec in recommendations:
            cuisine_str = str(rec.get("Cuisine", "")).lower()
            name_hash = sum(ord(c) for c in str(rec.get("Name", "")))
            
            assigned_img = cuisine_images["default"]
            for key in cuisine_images:
                if key in cuisine_str:
                    assigned_img = cuisine_images[key]
                    break
            
            rec["Image"] = f"{assigned_img}?sig={name_hash}&auto=format&fit=crop&q=80&w=800"

        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
