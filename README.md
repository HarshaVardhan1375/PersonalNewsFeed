# TITLE:- Personalized News Feed

# Description:-
Personalized News Feed System is an application that delivers tailored news articles to users based on their reading habits and interests. It uses NLP to analyze article content, extract topics/keywords, and build user profiles. Articles are then ranked using similarity scoring (cosine similarity of embeddings or keyword matching).
Users sign up/login.
System fetches latest news via API (e.g., NewsAPI).
NLP processes and categorizes articles.
Recommendations are generated based on user interests.
Users can like, bookmark, or dislike articles to improve personalization.

# Features:-
Content Aggregation – Collects news and updates from multiple sources.

User Profiling – Tracks user behavior to understand interests and preferences.

Content Filtering – Removes irrelevant or duplicate content.

Recommendation & Ranking – Suggests the most relevant content to the user.

Feedback & Adaptation – Learns from user interactions to improve future recommendations.


## Project Structure:-

Personlized News Feed/
|
|--src/         # core application logic
|   |--logic.py # Bussiness logic and task
operations
|   |__db.py    # Database operations
|
|--api/         # Backend API
|   |__main.py  # FastAPI endpoints
|
|--frontend/    # Frontend application
|   |__app.py   # StreamLit web interface
|
|--reqirements.txt # Python Dependencies
|
|--README.md    # Project Documentation
|
|--.env         # Python Variables 

## Quick Start

## Prequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,cloning)

### 1.Clone or Download the project 
# Option 1: clone with Git
git clone <repository-url>


### Option 2: Download and extract the ZIP file

### 2.Install Dependencies
pip install -r reuqirements.txt

### 3.Set up Supabase Database
1. Create the Tables required for project
2. Run the sql query
3. Get your credentials
### 4.Configure Environmental variables
1. create a `.env` in the project root
2. Add your supabase credentials to `.env`

### 5.Run the Application

## Streamlit Frontend
streamlit run frontend/app.py
The app will open in your browser at `http://localhost:8501`


## FastAPI Backend

cd api
python main.py
The API will be availble at `http://localhost:8000`

## How to use

## Techical Details

### Technologies Used

- **Fronted**: Streamlit(python web framework)
- **Backend**: FastAPI (Python REST API framework)
- **Database**: Supabase (PostgreSQL-based backend-as-a-service)
- **Language**: Python 3.8+

### Key Components

1. **`src/db.py1`**: Database operations 
    - Handles all CRUD operations with supabase
2. **`src/logic.py`**:Bussiness logic 
    - Task validation and processing

## Trouble Shooting

## Common Issues

## Future Enhancements


# Support

If you encounter any issues or have questions:
contact details:
Mb.no: `9392831108`
email: `vardhanreddyh18@gmail.com`

