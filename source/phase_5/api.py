import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Add phase_5 src to path
phase5_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if phase5_src not in sys.path:
    sys.path.append(phase5_src)

from backend_controller import BackendController

app = FastAPI(title="Zomato AI API")

# Configure CORS for Next.js frontend
# In production, set ALLOWED_ORIGINS to your vercel URL
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = allowed_origins_env.split(",")
else:
    allowed_origins = ["*"] # Allow all for initial deployment ease

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
    "phase_2", 
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
        
        # Image pools for variety
        cuisine_pools = {
            "italian": [
                "https://images.unsplash.com/photo-1551183053-bf91a1d81141",
                "https://images.unsplash.com/photo-1546549032-9571cd6b27df",
                "https://images.unsplash.com/photo-1574071318508-1cdbad80ad38",
                "https://images.unsplash.com/photo-1516100882582-76c9a59b35e8",
                "https://images.unsplash.com/photo-1595295333158-4742f28fbd85"
            ],
            "chinese": [
                "https://images.unsplash.com/photo-1552611052-33e04de081de",
                "https://images.unsplash.com/photo-1585032226651-759b368d7246",
                "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
                "https://images.unsplash.com/photo-1541696432-82c6da8ce7bf",
                "https://images.unsplash.com/photo-1563245372-f21724e3856d"
            ],
            "north indian": [
                "https://images.unsplash.com/photo-1585937421612-70a0f2455f75",
                "https://images.unsplash.com/photo-1565557623262-b51c2513a641",
                "https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a",
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec"
            ],
            "south indian": [
                "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
                "https://images.unsplash.com/photo-1668236543090-82eba5ee5976",
                "https://images.unsplash.com/photo-1630383249896-424e482df921",
                "https://images.unsplash.com/photo-1630383249896-424e482df921",
                "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4"
            ],
            "cafe": [
                "https://images.unsplash.com/photo-1509042239860-f550ce710b93",
                "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
                "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb",
                "https://images.unsplash.com/photo-1469957761103-550217487aa7",
                "https://images.unsplash.com/photo-1554118811-1e0d58224f24"
            ],
            "desserts": [
                "https://images.unsplash.com/photo-1551024601-bec78aea704b",
                "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e",
                "https://images.unsplash.com/photo-1488477181946-6428a0291777",
                "https://images.unsplash.com/photo-1565958011703-44f9829ba187",
                "https://images.unsplash.com/photo-1576618148400-f54bed99fdfd"
            ],
            "fast food": [
                "https://images.unsplash.com/photo-1561758033-d89a9ad46330",
                "https://images.unsplash.com/photo-1513104890138-7c749659a591",
                "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                "https://images.unsplash.com/photo-1550547660-d9450f859349",
                "https://images.unsplash.com/photo-1521305916504-4a1121188589"
            ],
            "default": [
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9",
                "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0"
            ]
        }

        # Enrich recommendations with unique images
        for rec in recommendations:
            cuisine_str = str(rec.get("Cuisine", "")).lower()
            name_str = str(rec.get("Name", "restaurant"))
            # Deterministic index based on name hash
            name_hash = sum(ord(c) for c in name_str)
            
            # Find matching pool
            selected_pool = cuisine_pools["default"]
            for key in cuisine_pools:
                if key in cuisine_str:
                    selected_pool = cuisine_pools[key]
                    break
            
            # Pick a unique image from the pool
            pool_idx = name_hash % len(selected_pool)
            base_url = selected_pool[pool_idx]
            
            # Final URL with formatting
            rec["Image"] = f"{base_url}?auto=format&fit=crop&q=80&w=800"

        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
