from flask import Flask, render_template, request
from model import recommend_careers, df

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/skills")
def skills():
    all_skills = set()
    for skill_list in df["Skills"].dropna():
        for s in skill_list.split(","):
            all_skills.add(s.strip())
    return render_template("skills.html", skills=sorted(all_skills))

@app.route("/results", methods=["POST"])
def results():
    selected_skills = request.form.getlist("skills")
    recommendations = recommend_careers(selected_skills)
    return render_template("results.html", careers=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
