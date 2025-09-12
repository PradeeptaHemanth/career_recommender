import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("IT_Job_Roles_Skills.csv", encoding="latin1")

# Fill NaNs
df["Skills"] = df["Skills"].fillna("")
df["Job Description"] = df["Job Description"].fillna("")

# Vectorize skills
vectorizer = TfidfVectorizer(stop_words="english")
skill_matrix = vectorizer.fit_transform(df["Skills"])

def recommend_careers(user_skills, top_n=5):
    user_text = " ".join(user_skills)
    user_vector = vectorizer.transform([user_text])
    similarity = cosine_similarity(user_vector, skill_matrix).flatten()
    
    top_indices = similarity.argsort()[::-1][:top_n]
    
    recommendations = []
    for i in top_indices:
        job_title = df.iloc[i]["Job Title"]
        google_jobs_url = f"https://www.google.com/search?q={job_title.replace(' ', '+')}+jobs"
        recommendations.append({
            "title": job_title,
            "description": df.iloc[i]["Job Description"],
            "link": google_jobs_url
        })
    return recommendations
