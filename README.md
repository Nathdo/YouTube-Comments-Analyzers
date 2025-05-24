# YouTube Comments Analyzer 

**Live demo**: [https://mystartup-production.up.railway.app/](https://mystartup-production.up.railway.app/)  
**Author**: [Nathan Douieb](https://github.com/Nathdo)

## Project Overview

This project is a **YouTube comments analyzer** powered by **LLMs**.  
It extracts comments from a given YouTube video and analyzes them using **OpenAI GPT-3.5** to generate:

- A sentiment summary (positive, neutral, negative)
- Key insights and feedback for the video creator
- An overview of viewers’ emotions and topics

> This is a fully working **demo** project, deployed to production with **Flask** and **Railway**.

## Why This Project?

YouTube creators receive thousands of comments, making it hard to:
- Understand what their audience really thinks
- Identify recurring feedback
- Spot ideas for future content

This tool provides creators with **quick insights** about their community.

---

## 🛠Tech Stack

| Technology | Description |
|------------|-------------|
| OpenAI GPT-3.5 | Comment analysis and summarization |
| YouTube Data API v3 | Comment extraction |
| Flask | Backend and routing |
| Railway | Production deployment |
| Regex & Prompt Engineering | Text processing and LLM optimization |

---

## Try It Online

Paste any YouTube video link in the live demo:  
👉 [https://mystartup-production.up.railway.app/](https://mystartup-production.up.railway.app/)

---

## Future Improvements

- Add multilingual support
- Visualize sentiment over time
- Provide suggestions to improve viewer engagement
- Save analysis history per user
