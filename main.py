from flask import Flask, render_template, request

app = Flask(__name__)

grade_point_map = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'RA': 0, 'U': 0, 'AB': 0}

# Static subjects for 8 semesters
subjects = {
    "Semester I": [
        ("BS3171", "Physics and Chemistry Lab", 2),
        ("CY3151", "Engineering Chemistry", 3),
        ("GE3151", "Problem Solving and Python Programming", 3),
        ("GE3152", "Heritage of Tamils", 1),
        ("GE3171", "Python Programming Lab", 2),
        ("GE3172", "English Lab", 1),
        ("HS3152", "Professional English - I", 3),
        ("MA3151", "Matrices and Calculus", 4),
        ("PH3151", "Engineering Physics", 3)
    ],
    "Semester II": [
        ("AD3251", "Data Structures Design", 3),
        ("AD3271", "DS Lab", 2),
        ("BE3251", "Basic Electrical and Electronics Engineering", 3),
        ("GE3251", "Engineering Graphics", 4),
        ("GE3252", "Tamils and Technology", 1),
        ("GE3271", "Engineering Practices Lab", 2),
        ("GE3272", "Communication Lab / Foreign Language", 2),
        ("HS3252", "Professional English - II", 2),
        ("MA3251", "Statistics and Numerical Methods", 4),
        ("PH3256", "Physics for Information Science", 3)
    ],
    "Semester III": [
        ("AD3301", "Data Exploration & Visualization", 4),
        ("AD3311", "AI Lab", 1.5),
        ("AD3351", "Design & Analysis of Algorithms", 4),
        ("AD3381", "DBMS Lab", 1.5),
        ("AD3391", "Database Design and Management", 3),
        ("AL3391", "Artificial Intelligence", 3),
        ("CS3351", "Digital Principles & CO", 4),
        ("GE3361", "Professional Development", 1),
        ("MA3354", "Discrete Mathematics", 4)
    ],
    "Semester IV": [
        ("AD3411", "DSA Lab", 2),
        ("AD3461", "ML Lab", 2),
        ("AD3491", "Data Science and Analytics", 3),
        ("AL3451", "Machine Learning", 3),
        ("AL3452", "Operating Systems", 4),
        ("CS3591", "Computer Networks", 4),
        ("GE3451", "Env. Science & Sustainability", 2),
        ("MA3391", "Probability & Statistics", 4)
    ],
    "Semester V": [
        ("AD3501", "Deep Learning", 3),
        ("AD3511", "Deep Learning Lab", 2),
        ("AD3512", "Summer Internship", 2),
        ("CCS334", "Big Data Analytics", 3),
        ("CCS335", "Cloud Computing", 3),
        ("CCW331", "Business Analytics", 3),
        ("CS3551", "Distributed Computing", 3),
        ("CW3551", "Data and Info Security", 3)
    ],
    "Semester VI": [
        ("CS3691", "Embedded Systems and IoT", 4),
        ("CCS370", "UI and UX Design", 3),
        ("CCS360", "Recommender Systems", 3),
        ("CCS365", "Software Defined Networks", 3),
        ("CCS363", "Social Network  Security", 3),
    ],
    "Semester VII": [
        ("OME354", "Applied Design Thinking", 3),
        ("GE3751", "Principles of Management", 3),
        ("AI3021", "IT in Agricultural System", 3),
        ("GE3791", "Human Values & Ethics", 2),
    ],
    "Semester VIII": [
        ("AD3811", "Project / Internship", 10)
    ]
}

# ---------------------------
# Route: Add Subjects Page
# ---------------------------
@app.route("/add-subjects")
def add_subjects():
    available_subjects = [
        {"semester": "Semester V", "code": "AD3002", "name": "Health Care & Analytics", "credits": 3},
        {"semester": "Semester V", "code": "CCS345", "name": "Ethics and AI", "credits": 3},
        {"semester": "Semester V", "code": "MX3084", "name": "Disaster Risk Reduction and Management", "credits": 0},
        {"semester": "Semester IV", "code": "NM1022", "name": "Experience-Based Project Learning", "credits": 3},
        {"semester": "Semester V", "code": "NM1028", "name": "AWS Cloud Practitioner", "credits": 3},
        {"semester": "Semester VI", "code": "CCS366", "name": "Software Testing and Automation", "credits": 3},

    ]

    # Group by semester
    grouped_subjects = {}
    for sub in available_subjects:
        sem = sub["semester"]
        if sem not in grouped_subjects:
            grouped_subjects[sem] = []
        grouped_subjects[sem].append((sub["code"], sub["name"], sub["credits"]))

    return render_template("add_subjects.html", subjects=grouped_subjects)

# ---------------------------
# Route: Main GPA / CGPA Page
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    cgpa = None
    total_credits = 0
    result = []
    semester_gpas = {}

    if request.method == "POST":
        form_type = request.form.get("form_type")
        total_points = 0

        if form_type == "cgpa":
            for semester, subject_list in subjects.items():
                sem_points = 0
                sem_credits = 0
                for code, name, credits in subject_list:
                    if credits == 0:
                        continue
                    grade = request.form.get(code)
                    grade_point = grade_point_map.get(grade.upper(), None)
                    if grade_point is not None:
                        total_credits += credits
                        total_points += credits * grade_point
                        sem_credits += credits
                        sem_points += credits * grade_point
                        result.append((semester, code, name, credits, grade.upper(), grade_point))
                semester_gpas[semester] = round(sem_points / sem_credits, 2) if sem_credits > 0 else 0

            cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0

        elif form_type.startswith("gpa_"):
            sem_key = form_type.split("gpa_")[1].replace("_", " ")
            if sem_key in subjects:
                sem_points = 0
                sem_credits = 0
                for code, name, credits in subjects[sem_key]:
                    if credits == 0:
                        continue
                    grade = request.form.get(code)
                    grade_point = grade_point_map.get(grade.upper(), None)
                    if grade_point is not None:
                        sem_credits += credits
                        sem_points += credits * grade_point
                        result.append((sem_key, code, name, credits, grade.upper(), grade_point))
                semester_gpas[sem_key] = round(sem_points / sem_credits, 2) if sem_credits > 0 else 0

    return render_template("index.html", subjects=subjects, cgpa=cgpa, result=result, semester_gpas=semester_gpas)

# ---------------------------
# Start the Flask App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
