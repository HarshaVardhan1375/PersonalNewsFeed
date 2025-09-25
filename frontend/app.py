# app.py (Streamlit frontend)
import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change to your FastAPI URL when deployed

st.set_page_config(page_title="Personalized News Feed", layout="wide")

st.title("📰 Personalized News Feed Frontend")

menu = st.sidebar.selectbox(
    "Choose Section",
    ["Users", "Categories", "Articles", "Interactions", "Recommendations"]
)

# ------------------ USERS ------------------
if menu == "Users":
    st.header("User Operations")

    action = st.radio("Action", ["Create", "Get", "Update", "Delete"])

    if action == "Create":
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Create User"):
            res = requests.post(f"{API_URL}/users", json={
                "username": username, "email": email, "password": password
            })
            st.json(res.json())

    elif action == "Get":
        user_id = st.number_input("User ID", min_value=1, step=1)
        if st.button("Fetch User"):
            res = requests.get(f"{API_URL}/users/{user_id}")
            st.json(res.json())

    elif action == "Update":
        user_id = st.number_input("User ID", min_value=1, step=1)
        username = st.text_input("New Username (optional)")
        email = st.text_input("New Email (optional)")
        password = st.text_input("New Password (optional)", type="password")
        if st.button("Update User"):
            res = requests.put(f"{API_URL}/users/{user_id}", json={
                "username": username or None,
                "email": email or None,
                "password": password or None
            })
            st.json(res.json())

    elif action == "Delete":
        user_id = st.number_input("User ID", min_value=1, step=1)
        if st.button("Delete User"):
            res = requests.delete(f"{API_URL}/users/{user_id}")
            st.json(res.json())

# ------------------ CATEGORIES ------------------
elif menu == "Categories":
    st.header("Category Operations")
    action = st.radio("Action", ["Create", "List", "Update", "Delete"])

    if action == "Create":
        name = st.text_input("Category Name")
        if st.button("Create Category"):
            res = requests.post(f"{API_URL}/categories", json={"name": name})
            st.json(res.json())

    elif action == "List":
        if st.button("Get Categories"):
            res = requests.get(f"{API_URL}/categories")
            st.json(res.json())

    elif action == "Update":
        category_id = st.number_input("Category ID", min_value=1, step=1)
        name = st.text_input("New Category Name")
        if st.button("Update Category"):
            res = requests.put(f"{API_URL}/categories/{category_id}", json={"name": name})
            st.json(res.json())

    elif action == "Delete":
        category_id = st.number_input("Category ID", min_value=1, step=1)
        if st.button("Delete Category"):
            res = requests.delete(f"{API_URL}/categories/{category_id}")
            st.json(res.json())

# ------------------ ARTICLES ------------------
elif menu == "Articles":
    st.header("Article Operations")
    action = st.radio("Action", ["Create", "List", "Update", "Delete"])

    if action == "Create":
        title = st.text_input("Title")
        content = st.text_area("Content")
        source = st.text_input("Source (optional)")
        url = st.text_input("URL (optional)")
        category_id = st.number_input("Category ID", min_value=1, step=1)
        published_at = st.text_input("Published At (YYYY-MM-DD)")
        if st.button("Create Article"):
            res = requests.post(f"{API_URL}/articles", json={
                "title": title, "content": content,
                "source": source or None, "url": url or None,
                "category_id": category_id, "published_at": published_at
            })
            st.json(res.json())

    elif action == "List":
        if st.button("Get Articles"):
            res = requests.get(f"{API_URL}/articles")
            st.json(res.json())

    elif action == "Update":
        article_id = st.number_input("Article ID", min_value=1, step=1)
        title = st.text_input("New Title (optional)")
        content = st.text_area("New Content (optional)")
        source = st.text_input("New Source (optional)")
        url = st.text_input("New URL (optional)")
        category_id = st.number_input("New Category ID (optional)", min_value=0, step=1)
        published_at = st.text_input("New Published At (YYYY-MM-DD)", value="")
        if st.button("Update Article"):
            res = requests.put(f"{API_URL}/articles/{article_id}", json={
                "title": title or None,
                "content": content or None,
                "source": source or None,
                "url": url or None,
                "category_id": category_id or None,
                "published_at": published_at or None
            })
            st.json(res.json())

    elif action == "Delete":
        article_id = st.number_input("Article ID", min_value=1, step=1)
        if st.button("Delete Article"):
            res = requests.delete(f"{API_URL}/articles/{article_id}")
            st.json(res.json())

# ------------------ INTERACTIONS ------------------
elif menu == "Interactions":
    st.header("User Interactions")
    action = st.radio("Action", ["Create", "Get", "Delete"])

    if action == "Create":
        user_id = st.number_input("User ID", min_value=1, step=1)
        article_id = st.number_input("Article ID", min_value=1, step=1)
        interaction_type = st.selectbox("Interaction Type", ["click", "like", "share"])
        if st.button("Add Interaction"):
            res = requests.post(f"{API_URL}/interactions", json={
                "user_id": user_id, "article_id": article_id, "interaction_type": interaction_type
            })
            st.json(res.json())

    elif action == "Get":
        user_id = st.number_input("User ID", min_value=1, step=1)
        if st.button("Get User Interactions"):
            res = requests.get(f"{API_URL}/interactions/{user_id}")
            st.json(res.json())

    elif action == "Delete":
        user_id = st.number_input("User ID", min_value=1, step=1)
        article_id = st.number_input("Article ID", min_value=1, step=1)
        if st.button("Delete Interaction"):
            res = requests.delete(f"{API_URL}/interactions", params={
                "user_id": user_id, "article_id": article_id
            })
            st.json(res.json())

# ------------------ RECOMMENDATIONS ------------------
elif menu == "Recommendations":
    st.header("Recommendations")
    action = st.radio("Action", ["Create", "Get", "Generate"])

    if action == "Create":
        user_id = st.number_input("User ID", min_value=1, step=1)
        article_id = st.number_input("Article ID", min_value=1, step=1)
        score = st.number_input("Score", min_value=0.0, step=0.1)
        if st.button("Add Recommendation"):
            res = requests.post(f"{API_URL}/recommendations", json={
                "user_id": user_id, "article_id": article_id, "score": score
            })
            st.json(res.json())

    elif action == "Get":
        user_id = st.number_input("User ID", min_value=1, step=1)
        if st.button("Get Recommendations"):
            res = requests.get(f"{API_URL}/recommendations/{user_id}")
            st.json(res.json())

    elif action == "Generate":
        user_id = st.number_input("User ID", min_value=1, step=1)
        top_n = st.slider("Top N", 1, 20, 5)
        if st.button("Generate Recommendations"):
            res = requests.get(f"{API_URL}/recommendations/generate/{user_id}", params={"top_n": top_n})
            st.json(res.json())
