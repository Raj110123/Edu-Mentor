# weak_topic_detection.py

# Simulated test results (later this will come from database)
test_results = [
    {"topic": "SQL", "correct": 4, "wrong": 1, "skipped": 0, "time": 30},
    {"topic": "Python", "correct": 1, "wrong": 4, "skipped": 1, "time": 80},
    {"topic": "Machine Learning", "correct": 0, "wrong": 5, "skipped": 1, "time": 90}
]

weak_topics = []

print("\nStudent Test Analysis\n")

for test in test_results:
    topic = test["topic"]
    correct = test["correct"]
    wrong = test["wrong"]
    skipped = test["skipped"]
    time_spent = test["time"]

    total = correct + wrong
    accuracy = (correct / total) * 100 if total > 0 else 0

    print(f"Topic: {topic}")
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"Wrong Answers: {wrong}")
    print(f"Skipped: {skipped}")
    print(f"Time Spent: {time_spent} sec\n")

    # Weak topic conditions
    if accuracy < 50 or wrong > 3 or time_spent > 60:
        weak_topics.append(topic)

print("Detected Weak Topics:")
for topic in weak_topics:
    print("-", topic)

print("\nRecommendations:")
for topic in weak_topics:
    print(f"Practice more questions on {topic}")




# #from pymongo import MongoClient

# # -----------------------------
# # STEP 1: CONNECT TO MONGODB
# # -----------------------------
# client = MongoClient("mongodb://localhost:27017/")
# db = client["learning_platform"]
# collection = db["test_results"]

# # -----------------------------
# # STEP 2: FETCH STUDENT RESULTS
# # -----------------------------
# student_id = 1
# results = collection.find({"student_id": student_id})

# weak_topics = []

# # -----------------------------
# # STEP 3: WEAK TOPIC DETECTION
# # -----------------------------
# for r in results:

#     topic = r["topic"]
#     correct = r["correct"]
#     wrong = r["wrong"]
#     skipped = r["skipped"]
#     time_spent = r["time"]

#     total = correct + wrong
#     accuracy = (correct / total) * 100 if total > 0 else 0

#     print("\nTopic:", topic)
#     print("Accuracy:", round(accuracy, 2), "%")
#     print("Wrong:", wrong)
#     print("Skipped:", skipped)
#     print("Time Spent:", time_spent)

#     if accuracy < 50 or wrong > 3 or time_spent > 60:
#         weak_topics.append(topic)

# # -----------------------------
# # STEP 4: SHOW WEAK TOPICS
# # -----------------------------
# print("\nWeak Topics Detected:")
# for topic in weak_topics:
#     print("-", topic)

# # -----------------------------
# # STEP 5: RAG RECOMMENDATION
# # -----------------------------
# def rag_query(topic):
#     # Replace this with your real RAG pipeline later
#     return f"Recommended study material for {topic}: Review concepts and practice questions."

# print("\nAI Study Recommendations:\n")

# for topic in weak_topics:
#     recommendation = rag_query(topic)
#     print(recommendation)