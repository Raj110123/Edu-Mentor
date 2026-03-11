from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
import base64
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path=".env.local")

app = FastAPI()

client = ElevenLabs(api_key="sk_b149788c0cdae82c16a93007017574ebf5e10bccb50d056c")
try:
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"Warning: Failed to initialize Groq client: {e}")
    groq_client = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    question: str
    sessionId: str = ""

@app.post("/voice-input")
async def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        return {"transcript": text}
    except sr.UnknownValueError:
        return {"error": "Could not understand audio"}
    except sr.RequestError as e:
        return {"error": str(e)}

@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    audio_response = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        text=req.question,
        voice_settings={
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    )
    audio_bytes = b"".join(audio_response)
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    return {"audio": audio_b64}

class CurrentTest(BaseModel):
    score: float
    accuracy: float
    avg_time: float
    difficulty: str = "medium"

class PerformanceRequest(BaseModel):
    target_score: float
    current_test: CurrentTest

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

@app.post("/predict-performance")
async def predict_performance(req: PerformanceRequest):
    all_tests = mock_tests.copy()
    all_tests.append({
        "test": len(all_tests) + 1,
        "score": req.current_test.score,
        "accuracy": req.current_test.accuracy,
        "avg_time": req.current_test.avg_time,
        "difficulty": req.current_test.difficulty
    })

    avg_score = sum(float(t["score"]) for t in all_tests) / len(all_tests)
    avg_accuracy = sum(float(t["accuracy"]) for t in all_tests) / len(all_tests)
    avg_time = sum(float(t["avg_time"]) for t in all_tests) / len(all_tests)

    improvement = float(all_tests[-1]["score"]) - float(all_tests[0]["score"])

    predicted_score = (
        0.5 * avg_score +
        0.3 * avg_accuracy +
        0.2 * improvement
    )

    status = "On Track" if predicted_score >= req.target_score else "Behind Target"

    prompt = f"""
A student has the following performance data:

Average Score: {avg_score:.2f}
Accuracy: {avg_accuracy:.2f}%
Average Time per Question: {avg_time:.2f}
Improvement Trend: {improvement}
Predicted Score: {predicted_score:.2f}
Target Score: {req.target_score}

Give a simple study strategy to help the student improve and reach the target score.
Return only 3 short bullet points.
"""

    try:
        if groq_client:
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            strategy = response.choices[0].message.content
        else:
            strategy = "• Review core concepts.\n• Practice more questions.\n• Manage time effectively."
    except Exception as e:
        print(f"Error fetching strategy from Groq: {e}")
        strategy = "• Review core concepts.\n• Practice more questions.\n• Manage time effectively."

    return {
        "analysis": {
            "avg_score": round(avg_score, 2),
            "avg_accuracy": round(avg_accuracy, 2),
            "avg_time": round(avg_time, 2),
            "improvement": round(improvement, 2),
            "predicted_score": round(predicted_score, 2),
            "target_score": req.target_score,
            "status": status
        },
        "strategy": strategy
    }