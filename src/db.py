# db.py
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# ------------------------
# USERS
# ------------------------
def create_user(username):
    return supabase.table("Users").insert({
        "username": username
    }).execute()

def get_user(user_id):
    return supabase.table("Users").select("*").eq("user_id", user_id).execute()

def update_user(user_id, username):
    return supabase.table("Users").update({
        "username": username
    }).eq("user_id", user_id).execute()

def delete_user(user_id):
    return supabase.table("Users").delete().eq("user_id", user_id).execute()


# ------------------------
# CATEGORIES
# ------------------------
def create_category(name):
    return supabase.table("Categories").insert({
        "name": name
    }).execute()

def get_all_categories():
    return supabase.table("Categories").select("*").execute()

def update_category(category_id, name):
    return supabase.table("Categories").update({
        "name": name
    }).eq("category_id", category_id).execute()

def delete_category(category_id):
    return supabase.table("Categories").delete().eq("category_id", category_id).execute()


# ------------------------
# ARTICLES
# ------------------------
def create_article(title, content, source, url, category_id, published_at):
    return supabase.table("Articles").insert({
        "title": title,
        "content": content,
        "source": source,
        "url": url,
        "category_id": category_id,
        "published_at": published_at
    }).execute()

def get_all_articles():
    return supabase.table("Articles").select("*").execute()

def update_article(article_id, **kwargs):
    # kwargs = {title, content, source, url, category_id, published_at}
    return supabase.table("Articles").update(kwargs).eq("article_id", article_id).execute()

def delete_article(article_id):
    return supabase.table("Articles").delete().eq("article_id", article_id).execute()


# ------------------------
# USER INTERACTIONS
# ------------------------
def add_interaction(user_id, article_id, interaction_type):
    return supabase.table("User_Interactions").insert({
        "user_id": user_id,
        "article_id": article_id,
        "interaction_type": interaction_type
    }).execute()

def get_user_interactions(user_id):
    return supabase.table("User_Interactions").select("*").eq("user_id", user_id).execute()

def update_interaction(interaction_id, interaction_type):
    return supabase.table("User_Interactions").update({
        "interaction_type": interaction_type
    }).eq("interaction_id", interaction_id).execute()

def delete_interaction(interaction_id):
    return supabase.table("User_Interactions").delete().eq("interaction_id", interaction_id).execute()


# ------------------------
# RECOMMENDATIONS
# ------------------------
def add_recommendation(user_id, article_id, score):
    return supabase.table("Recommendations").insert({
        "user_id": user_id,
        "article_id": article_id,
        "score": score
    }).execute()

def get_recommendations(user_id):
    return supabase.table("Recommendations").select("*").eq("user_id", user_id).execute()

def update_recommendation(recommendation_id, score):
    return supabase.table("Recommendations").update({
        "score": score
    }).eq("recommendation_id", recommendation_id).execute()

def delete_recommendation(recommendation_id):
    return supabase.table("Recommendations").delete().eq("recommendation_id", recommendation_id).execute()


# ------------------------
# HELPER FUNCTIONS
# ------------------------
def get_user_recommended_articles(user_id):
    """
    Fetch recommended articles for a user with full article details
    """
    return (
        supabase.table("Recommendations")
        .select("score, recommended_at, Articles(*)")
        .eq("user_id", user_id)
        .execute()
    )

def get_user_interactions_with_articles(user_id):
    """
    Fetch user interactions along with full article details
    """
    return (
        supabase.table("User_Interactions")
        .select("interaction_type, interaction_time, Articles(*)")
        .eq("user_id", user_id)
        .execute()
    )
