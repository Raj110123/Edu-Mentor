from groq import Groq
import os

# -----------------------------
# Groq API setup
# -----------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# Historical mock test data
# -----------------------------
mock_tests = [
    {"test": 1, "score": 58, "accuracy": 62, "avg_time": 60, "difficulty": "medium"},
    {"test": 2, "score": 64, "accuracy": 67, "avg_time": 58, "difficulty": "medium"},
    {"test": 3, "score": 69, "accuracy": 71, "avg_time": 55, "difficulty": "hard"},
    {"test": 4, "score": 72, "accuracy": 74, "avg_time": 53, "difficulty": "medium"},
    {"test": 5, "score": 66, "accuracy": 69, "avg_time": 57, "difficulty": "hard"},
    {"test": 6, "score": 75, "accuracy": 78, "avg_time": 50, "difficulty": "medium"},
    {"test": 7, "score": 70, "accuracy": 72, "avg_time": 52, "difficulty": "hard"},
    {"test": 8, "score": 77, "accuracy": 80, "avg_time": 49, "difficulty": "medium"},
    {"test": 9, "score": 73, "accuracy": 75, "avg_time": 51, "difficulty": "hard"},
    {"test": 10, "score": 80, "accuracy": 83, "avg_time": 47, "difficulty": "medium"},
    {"test": 11, "score": 76, "accuracy": 79, "avg_time": 48, "difficulty": "hard"},
    {"test": 12, "score": 82, "accuracy": 85, "avg_time": 46, "difficulty": "medium"},
    {"test": 13, "score": 78, "accuracy": 81, "avg_time": 47, "difficulty": "hard"},
    {"test": 14, "score": 84, "accuracy": 87, "avg_time": 45, "difficulty": "medium"},
    {"test": 15, "score": 79, "accuracy": 82, "avg_time": 46, "difficulty": "hard"},
    {"test": 16, "score": 86, "accuracy": 89, "avg_time": 44, "difficulty": "medium"},
    {"test": 17, "score": 83, "accuracy": 86, "avg_time": 45, "difficulty": "hard"},
    {"test": 18, "score": 88, "accuracy": 90, "avg_time": 43, "difficulty": "medium"},
    {"test": 19, "score": 85, "accuracy": 88, "avg_time": 44, "difficulty": "hard"},
    {"test": 20, "score": 90, "accuracy": 92, "avg_time": 42, "difficulty": "medium"}
]

target_score = 90


# ----------------------------- 
# 1 Calculate averages
# -----------------------------
avg_score = sum(t["score"] for t in mock_tests) / len(mock_tests)
avg_accuracy = sum(t["accuracy"] for t in mock_tests) / len(mock_tests)
avg_time = sum(t["avg_time"] for t in mock_tests) / len(mock_tests)


# -----------------------------
# 2 Improvement trend
# -----------------------------
improvement = mock_tests[-1]["score"] - mock_tests[0]["score"]


# -----------------------------
# 3 Difficulty analysis
# -----------------------------
hard_tests = [t for t in mock_tests if t["difficulty"] == "hard"]
hard_score = sum(t["score"] for t in hard_tests) / len(hard_tests) if hard_tests else avg_score


# -----------------------------
# 4 Predicted performance score
# -----------------------------
predicted_score = (
    0.5 * avg_score +
    0.3 * avg_accuracy +
    0.2 * improvement
)


# -----------------------------
# 5 Check if on track
# -----------------------------
status = "On Track" if predicted_score >= target_score else "Behind Target"


# -----------------------------
# 6 AI Strategy Generation (Groq)
# -----------------------------
prompt = f"""
A student has the following performance data:

Average Score: {avg_score:.2f}
Accuracy: {avg_accuracy:.2f}%
Average Time per Question: {avg_time:.2f}
Improvement Trend: {improvement}
Predicted Score: {predicted_score:.2f}
Target Score: {target_score}

Give a simple study strategy to help the student improve and reach the target score.
Return only 3 short bullet points.
"""


response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

strategy = response.choices[0].message.content


# -----------------------------
# 7 Output
# -----------------------------
print("\n===== Performance Analysis =====")

print("Average Score:", round(avg_score, 2))
print("Average Accuracy:", round(avg_accuracy, 2))
print("Average Time:", round(avg_time, 2))

print("\nImprovement Trend:", improvement)

print("\nPredicted Performance Score:", round(predicted_score, 2))
print("Target Score:", target_score)
print("Status:", status)

print("\n===== AI Strategy Recommendations =====\n")
print(strategy)