# src/logic.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import (
    create_user, get_user, update_user, delete_user,
    create_category, get_all_categories, update_category, delete_category,
    create_article, get_all_articles, update_article, delete_article,
    add_interaction, get_user_interactions_with_articles,
    add_recommendation, get_user_recommended_articles
)
from collections import Counter
from datetime import datetime

# ------------------------
# USERS
# ------------------------
class UserLogic:
    def add_user(self, username):
        if not username:
            return {"success": False, "message": "Username is required"}
        result = create_user(username)
        if result.get("status_code") == 201:
            return {"success": True, "message": "User added successfully"}
        else:
            return {"success": False, "message": "Failed to add user"}

    def get_user(self, user_id):
        return get_user(user_id)

    def update_user(self, user_id, username):
        return update_user(user_id, username)

    def delete_user(self, user_id):
        return delete_user(user_id)

# ------------------------
# CATEGORIES
# ------------------------
class CategoryLogic:
    def add_category(self, name):
        if not name:
            return {"success": False, "message": "Category name is required"}
        return create_category(name)

    def list_categories(self):
        return get_all_categories()

    def update_category(self, category_id, name):
        return update_category(category_id, name)

    def delete_category(self, category_id):
        return delete_category(category_id)

# ------------------------
# ARTICLES
# ------------------------
class ArticleLogic:
    def add_article(self, title, content, source, url, category_id, published_at):
        if not title or not content:
            return {"success": False, "message": "Title and content are required"}
        return create_article(title, content, source, url, category_id, published_at)

    def list_articles(self):
        return get_all_articles()

    def update_article(self, article_id, **kwargs):
        return update_article(article_id, **kwargs)

    def delete_article(self, article_id):
        return delete_article(article_id)

# ------------------------
# USER INTERACTIONS
# ------------------------
class InteractionLogic:
    def add_interaction(self, user_id, article_id, interaction_type):
        return add_interaction(user_id, article_id, interaction_type)

    def get_interactions(self, user_id):
        return get_user_interactions_with_articles(user_id)

# ------------------------
# RECOMMENDATIONS
# ------------------------
class RecommendationLogic:
    def add_recommendation(self, user_id, article_id, score):
        return add_recommendation(user_id, article_id, score)

    def get_recommendations(self, user_id):
        return get_user_recommended_articles(user_id)

    # ------------------------
    # PERSONALIZATION LOGIC
    # ------------------------
    def generate_recommendations(self, user_id, top_n=5):
        interactions = InteractionLogic().get_interactions(user_id)
        if not interactions.get("data"):
            return {"success": True, "recommendations": []}

        categories = [item["Articles"]["category_id"] for item in interactions["data"]]
        category_counts = Counter(categories)
        preferred_categories = [cat for cat, _ in category_counts.most_common()]

        all_articles = ArticleLogic().list_articles()
        if not all_articles.get("data"):
            return {"success": True, "recommendations": []}

        interacted_article_ids = {item["Articles"]["article_id"] for item in interactions["data"]}

        recommended = []
        for cat in preferred_categories:
            for article in all_articles["data"]:
                if article["category_id"] == cat and article["article_id"] not in interacted_article_ids:
                    recommended.append(article)
                    if len(recommended) >= top_n:
                        break
            if len(recommended) >= top_n:
                break

        # Save recommendations to DB
        for article in recommended:
            self.add_recommendation(user_id, article["article_id"], score=1.0)

        return {"success": True, "recommendations": recommended}
