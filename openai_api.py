import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from collections import Counter

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_comments(comments):
    prompt = (
        "Summarize the following YouTube comments strictly in English. "
        "Use professional and neutral language:\n\n"
        f"{comments}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI API Error:", e)
        return "Summary unavailable due to API error."


def extract_topics(comments):
    prompt = (
        "List the main recurring themes or trends found in the following YouTube comments. "
        "Respond in English only, even if the comments are in another language. "
        "Only include important and frequent insights. Return each theme on its own line. Do not number or bullet them.\n\n"
        "Example:\n"
        "Love and heartbreak\n"
        "Struggles with mental health\n"
        "Memories of childhood\n"
        "...\n\n"
        f"{comments}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    raw_text = response.choices[0].message.content.strip()

    lines = raw_text.splitlines()
    cleaned = [re.sub(r"^[\*\-\d\.\s]+", "", line).strip() for line in lines if line.strip()]
    return "\n".join(cleaned)




def analyze_emotions(comments):
    prompt = (
        "Analyze the following YouTube comments and extract all the emotions detected. "
        "List each emotion individually, repeating them if they occur more than once. "
        "Return only a comma-separated list in English (e.g. sadness, joy, sadness, hope). "
        "Avoid grouping or summarizing. This list will be used for statistical analysis.\n\n"
        f"{comments}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    emotions_text = response.choices[0].message.content.strip()

    emotions = re.split(r"[,\n]+", emotions_text)
    emotions = [e.strip().lower() for e in emotions if e.strip()]
    return {"counts": dict(Counter(emotions))}


def extract_emotions(emotion_dict):
    if not isinstance(emotion_dict, dict):
        return [], []

    total = sum(emotion_dict.values())
    if total == 0:
        return [], []

    sorted_emotions = sorted(emotion_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    labels = [emotion.capitalize() for emotion, _ in sorted_emotions]
    
    # Convertit les valeurs en pourcentage (arrondis à 2 chiffres après la virgule)
    values = [round((count / total) * 100, 2) for _, count in sorted_emotions]

    return labels, values

