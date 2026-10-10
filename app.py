from pathlib import Path
import csv

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_FILE = Path(__file__).parent / "q-fastapi.csv"


@app.get("/api")
def get_students(
    classes: list[str] | None = Query(default=None, alias="class")
):
    try:
        with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            students = [
                {
                    "studentId": int(row["studentId"]),
                    "class": row["class"],
                }
                for row in reader
            ]

        if classes:
            selected = set(classes)
            students = [
                student for student in students
                if student["class"] in selected
            ]

        return {"students": students}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="CSV file not found")
    except (ValueError, KeyError):
        raise HTTPException(status_code=500, detail="Invalid CSV data")
