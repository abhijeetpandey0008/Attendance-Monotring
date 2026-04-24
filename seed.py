from datetime import date, time, timedelta
from random import choice, randint
from src.database.database import SessionLocal
from src.core.security import hash_password

from src.models.user import User
from src.models.batch import Batch
from src.models.session import Session as SessionModel
from src.models.attendance import Attendance


db = SessionLocal()


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def create_user(name, email, password, role, institution_id=None):
    existing = db.query(User).filter(User.email == email).first()

    if existing:
        return existing

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role=role,
        institution_id=institution_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_batch(name, description):
    existing = db.query(Batch).filter(Batch.name == name).first()

    if existing:
        return existing

    batch = Batch(
        name=name,
        description=description
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)

    return batch


def create_session(batch_id, trainer_id, title, d):
    session = SessionModel(
        batch_id=batch_id,
        trainer_id=trainer_id,
        title=title,
        date=d,
        start_time=time(10, 0),
        end_time=time(11, 0)
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def create_attendance(session_id, student_id, status):

    existing = db.query(Attendance).filter(
        Attendance.session_id == session_id,
        Attendance.student_id == student_id
    ).first()

    if existing:
        return

    row = Attendance(
        session_id=session_id,
        student_id=student_id,
        status=status
    )

    db.add(row)
    db.commit()


# -------------------------------------------------
# Seed Start
# -------------------------------------------------

print("Seeding started...")


# -------------------------------------------------
# Programme Managers (3)
# -------------------------------------------------

for i in range(1, 4):
    create_user(
        f"Programme Manager {i}",
        f"manager{i}@test.com",
        "123456",
        "programme_manager"
    )


# -------------------------------------------------
# Monitoring Officers (3)
# -------------------------------------------------

for i in range(1, 4):
    create_user(
        f"Monitoring Officer {i}",
        f"officer{i}@test.com",
        "123456",
        "monitoring_officer"
    )


# -------------------------------------------------
# Trainers (10 across 5 institutions)
# -------------------------------------------------

trainers = []

for i in range(1, 11):
    trainer = create_user(
        f"Trainer {i}",
        f"trainer{i}@test.com",
        "123456",
        "trainer",
        institution_id=((i - 1) % 5) + 1
    )

    trainers.append(trainer)


# -------------------------------------------------
# Students (40 across 5 institutions)
# -------------------------------------------------

students = []

for i in range(1, 41):
    student = create_user(
        f"Student {i}",
        f"student{i}@test.com",
        "123456",
        "student",
        institution_id=((i - 1) % 5) + 1
    )

    students.append(student)


# -------------------------------------------------
# Batches (8)
# -------------------------------------------------

batch_names = [
    "Python Batch",
    "ML Batch",
    "AI Batch",
    "Web Batch",
    "Data Science Batch",
    "Cloud Batch",
    "IoT Batch",
    "Robotics Batch"
]

batches = []

for name in batch_names:
    batch = create_batch(
        name,
        f"{name} Description"
    )
    batches.append(batch)


# -------------------------------------------------
# Sessions (20)
# -------------------------------------------------

topics = [
    "Introduction",
    "Basics",
    "Advanced Concepts",
    "Hands-on Lab",
    "Project Discussion",
    "Revision",
    "Assessment",
    "Live Demo"
]

sessions = []

start_day = date(2026, 4, 1)

for i in range(20):

    batch = choice(batches)
    trainer = choice(trainers)

    session = create_session(
        batch.id,
        trainer.id,
        f"{choice(topics)} {i+1}",
        start_day + timedelta(days=i)
    )

    sessions.append(session)


# -------------------------------------------------
# Attendance
# -------------------------------------------------

statuses = ["present", "absent", "late"]

for s in sessions:

    selected_students = students[:randint(15, 25)]

    for stu in selected_students:
        create_attendance(
            s.id,
            stu.id,
            choice(statuses)
        )


print("Seeding completed successfully!")
print("Created:")
print("3 Programme Managers")
print("3 Monitoring Officers")
print("10 Trainers")
print("40 Students")
print("8 Batches")
print("20 Sessions")
print("Attendance Records Added")

db.close()