# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import logic classes
from src.logic import UserLogic, CategoryLogic, ArticleLogic, InteractionLogic, RecommendationLogic

# ----- APP Setup -----
app = FastAPI(title="Personalized News Feed API", version="1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # replace with frontend domains in production
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# ----- Logic Instances -----
user_logic = UserLogic()
category_logic = CategoryLogic()
article_logic = ArticleLogic()
interaction_logic = InteractionLogic()
recommendation_logic = RecommendationLogic()

# ----- Data Models -----
# Users
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    password: str = None

# Categories
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

# Articles
class ArticleCreate(BaseModel):
    title: str
    content: str
    source: str = None
    url: str = None
    category_id: int
    published_at: str  # ISO format datetime

class ArticleUpdate(BaseModel):
    title: str = None
    content: str = None
    source: str = None
    url: str = None
    category_id: int = None
    published_at: str = None

# User Interactions
class InteractionCreate(BaseModel):
    user_id: int
    article_id: int
    interaction_type: str  # click, like, share

# Recommendations
class RecommendationCreate(BaseModel):
    user_id: int
    article_id: int
    score: float

# ------------------------
# USERS CRUD
# ------------------------
@app.post("/users")
def create_user(user: UserCreate):
    res = user_logic.add_user(user.username, user.email, user.password)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.get("/users/{user_id}")
def get_user(user_id: int):
    res = user_logic.get_user(user_id)
    if res.get("success"):
        return res
    raise HTTPException(status_code=404, detail=res.get("message"))

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    res = user_logic.update_user(user_id, user.username, user.email, user.password)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    res = user_logic.delete_user(user_id)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

# ------------------------
# CATEGORIES CRUD
# ------------------------
@app.post("/categories")
def create_category(category: CategoryCreate):
    res = category_logic.add_category(category.name)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.get("/categories")
def list_categories():
    res = category_logic.list_categories()
    if res.get("success"):
        return res
    raise HTTPException(status_code=404, detail=res.get("message"))

@app.put("/categories/{category_id}")
def update_category(category_id: int, category: CategoryUpdate):
    res = category_logic.update_category(category_id, category.name)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    res = category_logic.delete_category(category_id)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

# ------------------------
# ARTICLES CRUD
# ------------------------
@app.post("/articles")
def create_article(article: ArticleCreate):
    res = article_logic.add_article(
        article.title,
        article.content,
        article.source,
        article.url,
        article.category_id,
        article.published_at
    )
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.get("/articles")
def read_articles():
    res = article_logic.list_articles()
    if res.get("success"):
        return res
    raise HTTPException(status_code=404, detail=res.get("message"))

@app.put("/articles/{article_id}")
def update_article(article_id: int, article: ArticleUpdate):
    res = article_logic.update_article(article_id, **article.dict(exclude_none=True))
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.delete("/articles/{article_id}")
def delete_article(article_id: int):
    res = article_logic.delete_article(article_id)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

# ------------------------
# USER INTERACTIONS
# ------------------------
@app.post("/interactions")
def create_interaction(interaction: InteractionCreate):
    res = interaction_logic.add_interaction(
        interaction.user_id,
        interaction.article_id,
        interaction.interaction_type
    )
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.get("/interactions/{user_id}")
def get_user_interactions(user_id: int):
    res = interaction_logic.get_interactions(user_id)
    if res.get("success"):
        return res
    raise HTTPException(status_code=404, detail=res.get("message"))

@app.delete("/interactions/")
def delete_interaction(user_id: int, article_id: int):
    res = interaction_logic.delete_interaction(user_id, article_id)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

# ------------------------
# RECOMMENDATIONS
# ------------------------
@app.post("/recommendations")
def create_recommendation(rec: RecommendationCreate):
    res = recommendation_logic.add_recommendation(rec.user_id, rec.article_id, rec.score)
    if res.get("success"):
        return res
    raise HTTPException(status_code=400, detail=res.get("message"))

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int):
    res = recommendation_logic.get_recommendations(user_id)
    if res.get("success"):
        return res
    raise HTTPException(status_code=404, detail=res.get("message"))

@app.get("/recommendations/generate/{user_id}")
def generate_recommendations(user_id: int, top_n: int = 5):
    res = recommendation_logic.generate_recommendations(user_id, top_n)
    if res.get("success"):
        return {"success": True, "data": res.get("recommendations")}
    raise HTTPException(status_code=400, detail=res.get("message"))

# ------------------------
# RUN APP
# ------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
