import hashlib
import json


class ExamEngine:
    """Handles secure quiz generation, automated scoring, and result verification."""

    def __init__(self, course_code: str):
        self.course_code = course_code
        self.questions = []

    def add_question(self, q_id: str, prompt: str, options: list, correct_option_index: int):
        """Adds a standardized multiple-choice question to the test bank."""
        self.questions.append({
            "q_id": q_id,
            "prompt": prompt,
            "options": options,
            "correct_index": correct_option_index
        })

    def evaluate_submission(self, student_id: str, answers: dict) -> dict:
        """Evaluates student submission dictionary mapping question IDs to chosen indices."""
        score = 0
        total = len(self.questions)

        for q in self.questions:
            q_id = q["q_id"]
            if answers.get(q_id) == q["correct_index"]:
                score += 1

        percentage = (score / total) * 100 if total > 0 else 0
        certificate_hash = hashlib.sha256(f"{student_id}:{percentage}:{self.course_code}".encode()).hexdigest()

        return {
            "student_id": student_id,
            "course": self.course_code,
            "score": score,
            "total_questions": total,
            "percentage": round(percentage, 2),
            "verification_hash": certificate_hash
        }


# Demonstration Run
if __name__ == "__main__":
    print("=== E-LEARNING EXAM ENGINE DEMO ===")
    exam = ExamEngine("SEN203")
    exam.add_question("Q1", "What is the primary function of SHA-256?", ["Data Encryption", "Cryptographic Hashing", "Role Access"], 1)
    exam.add_question("Q2", "Which OOP principle hides internal implementation details?", ["Encapsulation", "Polymorphism", "Inheritance"], 0)

    student_answers = {"Q1": 1, "Q2": 0}
    results = exam.evaluate_submission("STU-2026-08", student_answers)
    print(json.dumps(results, indent=2))
