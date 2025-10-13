"""
THIS IS A SAMPLE SCRIPT TO SEED THE DATABASE WITH STUDENTS, PROGRAMS, AND COLLEGES.
Adjust the data and logic as needed to fit your actual database schema and requirements.
"""

import os
import sys
import random
from flask import Flask

# Fix Python path - add this at the top
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.database import execute_sql

# ========== SAMPLE DATA ==========
first_names = [
    "Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Sophia", "James", "Isabella",
    "William", "Mia", "Benjamin", "Charlotte", "Lucas", "Amelia", "Henry", "Harper", "Alexander", "Evelyn",
    "Michael", "Abigail", "Daniel", "Ella", "Matthew", "Scarlett", "Ethan", "Grace", "Joseph", "Lily",
    "Samuel", "Aria", "David", "Chloe", "Sebastian", "Madison", "Jackson", "Layla", "Aiden", "Riley",
    "John", "Zoey", "Owen", "Nora", "Luke", "Hannah", "Gabriel", "Hazel", "Anthony", "Violet",
    "Isaac", "Aurora", "Dylan", "Penelope", "Leo", "Luna", "Julian", "Stella", "Wyatt", "Ellie",
    "Nathan", "Paisley", "Caleb", "Skylar", "Ryan", "Savannah", "Adrian", "Nova", "Hunter", "Leah",
    "Christian", "Audrey", "Jaxon", "Brooklyn", "Andrew", "Bella", "Joshua", "Aaliyah", "Christopher", "Claire",
    "Theodore", "Lucy", "Thomas", "Alice", "Charles", "Maya", "Eli", "Sadie", "Landon", "Eva",
    "Connor", "Emilia", "Josiah", "Autumn", "Isaiah", "Valentina", "Jonathan", "Naomi", "Cameron", "Everly",
    "Miles", "Lillian", "Colton", "Zoe", "Aaron", "Hailey", "Adam", "Kennedy", "Easton", "Madeline",
    "Robert", "Elena", "Hudson", "Delilah", "Angel", "Piper", "Brayden", "Ariana", "Ezekiel", "Melody"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennet", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
    "Bryant", "Cunningham", "Henderson", "Fisher", "Marshall", "Elliott", "Silva", "Gordon", "Jordan", "Graham",
    "McDonald", "Montgomery", "Harrison", "Warren", "Jenkins", "Ray", "Austin", "Webb", "Medina", "Franklin"
]

programs = [
    # College of Education (CED)
    ("BTLED-HE", "Bachelor of Technology and Livelihood Education - Home Economics", "CED"),
    ("BTLED-IA", "Bachelor of Technology and Livelihood Education - Industrial Arts", "CED"),
    ("BSEd-Eng", "Bachelor of Secondary Education - English", "CED"),
    ("BSEd-Math", "Bachelor of Secondary Education - Mathematics", "CED"),
    ("BSEd-Sci", "Bachelor of Secondary Education - Science", "CED"),
    ("BSEd-Fil", "Bachelor of Secondary Education - Filipino", "CED"),
    ("BSEd-SocSci", "Bachelor of Secondary Education - Social Studies", "CED"),
    ("BSEd-PE", "Bachelor of Secondary Education - Physical Education", "CED"),
    ("BSEd-Values", "Bachelor of Secondary Education - Values Education", "CED"),
    ("BSEd-SpEd", "Bachelor of Special Education", "CED"),

    # College of Arts and Social Sciences (CASS)
    ("BS Psych", "Bachelor of Science in Psychology", "CASS"),
    ("BA SocSci", "Bachelor of Arts in Social Sciences", "CASS"),
    ("BA Comm", "Bachelor of Arts in Communication", "CASS"),
    ("BA Hist", "Bachelor of Arts in History", "CASS"),
    ("BA Phil", "Bachelor of Arts in Philosophy", "CASS"),
    ("BA Eng", "Bachelor of Arts in English", "CASS"),
    ("BA Filipino", "Bachelor of Arts in Filipino", "CASS"),
    ("BA IR", "Bachelor of Arts in International Relations", "CASS"),
    ("BA DevCom", "Bachelor of Arts in Development Communication", "CASS"),
    ("BA Journ", "Bachelor of Arts in Journalism", "CASS"),

    # College of Science and Mathematics (CSM)
    ("BS Math", "Bachelor of Science in Mathematics", "CSM"),
    ("BS Bio", "Bachelor of Science in Biology", "CSM"),
    ("BS Chem", "Bachelor of Science in Chemistry", "CSM"),
    ("BS EnvSci", "Bachelor of Science in Environmental Science", "CSM"),
    ("BS Stat", "Bachelor of Science in Statistics", "CSM"),
    ("BS Applied Physics", "Bachelor of Science in Applied Physics", "CSM"),
    ("BS Marine Bio", "Bachelor of Science in Marine Biology", "CSM"),
    ("BS Geology", "Bachelor of Science in Geology", "CSM"),
    ("BS Forensic Sci", "Bachelor of Science in Forensic Science", "CSM"),
    ("BS Biotech", "Bachelor of Science in Biotechnology", "CSM"),

    # College of Engineering (COE)
    ("BSCE", "Bachelor of Science in Civil Engineering", "COE"),
    ("BSEE", "Bachelor of Science in Electrical Engineering", "COE"),
    ("BSME", "Bachelor of Science in Mechanical Engineering", "COE"),
    ("BSChE", "Bachelor of Science in Chemical Engineering", "COE"),
    ("BSIE", "Bachelor of Science in Industrial Engineering", "COE"),
    ("BSECE", "Bachelor of Science in Electronics and Communications Engineering", "COE"),
    ("BSRE", "Bachelor of Science in Renewable Energy Engineering", "COE"),
    ("BSGE", "Bachelor of Science in Geodetic Engineering", "COE"),
    ("BS AeroEng", "Bachelor of Science in Aeronautical Engineering", "COE"),
    ("BS NavalEng", "Bachelor of Science in Naval Engineering", "COE"),

    # College of Computer Studies (CCS)
    ("BSCS", "Bachelor of Science in Computer Science", "CCS"),
    ("BSIT", "Bachelor of Science in Information Technology", "CCS"),
    ("BSIS", "Bachelor of Science in Information Systems", "CCS"),
    ("BSEMC", "Bachelor of Science in Entertainment and Multimedia Computing", "CCS"),
    ("BSDA", "Bachelor of Science in Data Analytics", "CCS"),
    ("BS CyberSec", "Bachelor of Science in Cybersecurity", "CCS"),
    ("BS AI", "Bachelor of Science in Artificial Intelligence", "CCS"),
    ("BSSE", "Bachelor of Science in Software Engineering", "CCS"),
    ("BS DataSci", "Bachelor of Science in Data Science", "CCS"),
    ("BS GameDev", "Bachelor of Science in Game Development", "CCS"),

    # College of Economics, Business, and Accountancy (CEBA)
    ("BSBA-FM", "Bachelor of Science in Business Administration - Financial Management", "CEBA"),
    ("BSBA-MM", "Bachelor of Science in Business Administration - Marketing Management", "CEBA"),
    ("BSBA-HRM", "Bachelor of Science in Business Administration - Human Resource Management", "CEBA"),
    ("BS Accountancy", "Bachelor of Science in Accountancy", "CEBA"),
    ("BS Entrepreneurship", "Bachelor of Science in Entrepreneurship", "CEBA"),
    ("BSBA-OM", "Bachelor of Science in Business Administration - Operations Management", "CEBA"),
    ("BSBA-IB", "Bachelor of Science in Business Administration - International Business", "CEBA"),
    ("BS Econ", "Bachelor of Science in Economics", "CEBA"),
    ("BS Finance", "Bachelor of Science in Finance", "CEBA"),
    ("BS Public Ad", "Bachelor of Science in Public Administration", "CEBA"),

    # College of Health Sciences (CHS)
    ("BSN", "Bachelor of Science in Nursing", "CHS"),
    ("BSPT", "Bachelor of Science in Physical Therapy", "CHS"),
    ("BSMLS", "Bachelor of Science in Medical Laboratory Science", "CHS"),
    ("BSPH", "Bachelor of Science in Public Health", "CHS"),
    ("BPharm", "Bachelor of Science in Pharmacy", "CHS"),
    ("BS Radiology", "Bachelor of Science in Radiologic Technology", "CHS"),
    ("BSOT", "Bachelor of Science in Occupational Therapy", "CHS"),
    ("BSDent", "Bachelor of Science in Dentistry", "CHS"),
    ("BSRT", "Bachelor of Science in Respiratory Therapy", "CHS"),
    ("BSN Midwifery", "Bachelor of Science in Midwifery", "CHS"),
]

colleges = {
    "CED": "College of Education",
    "CASS": "College of Arts and Social Sciences",
    "CSM": "College of Science and Mathematics",
    "COE": "College of Engineering",
    "CCS": "College of Computer Studies",
    "CEBA": "College of Economics, Business, and Accountancy",
    "CHS": "College of Health Sciences",
}


# ========== SEED FUNCTIONS ==========
def seed_colleges_and_programs():
    """Ensure colleges and programs exist."""
    for code, name in colleges.items():
        execute_sql("""
            INSERT INTO colleges (college_code, college_name)
            VALUES (:code, :name)
            ON CONFLICT (college_code) DO NOTHING
        """, {"code": code, "name": name})

    for program_code, program_name, college_code in programs:
        execute_sql("""
            INSERT INTO programs (program_code, program_name, college_code)
            VALUES (:program_code, :program_name, :college_code)
            ON CONFLICT (program_code) DO NOTHING
        """, {
            "program_code": program_code,
            "program_name": program_name,
            "college_code": college_code
        })
    print("✅ Colleges and programs verified.")


def generate_random_students(n=300):
    """Generate random student data that matches schema."""
    students = []
    for _ in range(n):
        id_number = f"{random.randint(2021, 2024)}-{random.randint(1000, 9999)}"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        year_level = random.randint(1, 5)
        gender = random.choice(["MALE", "FEMALE", "OTHER"])
        program_code, _, _ = random.choice(programs)

        students.append({
            "id_number": id_number,
            "first_name": first_name,
            "last_name": last_name,
            "year_level": year_level,
            "gender": gender,
            "program_code": program_code
        })
    return students


def insert_students(students):
    """Insert generated students using your existing execute_sql()."""
    for s in students:
        execute_sql("""
            INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code)
            VALUES (:id_number, :first_name, :last_name, :year_level, :gender, :program_code)
            ON CONFLICT (id_number) DO NOTHING
        """, s)
    print(f"✅ Inserted {len(students)} students.")


# ========== MAIN ENTRY POINT ==========
def run_seed(app: Flask):
    """Run the seeding inside Flask app context."""
    with app.app_context():
        print("🚀 Starting database seeding...")
        seed_colleges_and_programs()
        students = generate_random_students(10000)
        insert_students(students)
        print("🎓 Seeding complete.")


# ========== OPTIONAL CLI ==========
if __name__ == "__main__":
    from app import create_app
    app = create_app()
    run_seed(app)
