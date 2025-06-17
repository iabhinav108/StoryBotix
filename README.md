# StoryBotix
## [This project is under development. Thankyou for visiting.]

**StoryBotix** is an AI-powered content automation tool that transforms trending news articles into short, engaging videos with narrated scripts, visuals, and subtitles. It leverages the latest in language models, text-to-speech, and generative image technologies to create video summaries suitable for platforms like YouTube Shorts, Instagram Reels, and TikTok.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How It Works](#how-it-works)
- [Dependencies](#dependencies)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Features

- Fetches trending tech news articles using NewsAPI.
- Automatically generates human-like scripts from article title and description.
- Uses generative AI to create relevant images from the script.
- Converts scripts into high-quality voiceovers using Google Text-to-Speech (gTTS).
- Creates short videos with:
  - Image slideshows
  - Narrated voiceovers
  - Subtitles synced with the narration
- Minimal and interactive CLI interface.

---

## Project Structure

StoryBotix/
│
├── assets/
│ ├── generated_scripts/ # Auto-saved scripts
│ ├── generated_images/ # Auto-generated image folders (per script)
│ └── generated_videos/ # Final generated videos
│
├── utils/
│ └── image_generator.py # Handles image generation from script
│
├── news_scraper.py # Fetches trending news from NewsAPI
├── script_generator.py # Generates readable script from news
├── video_generator.py # Creates video with narration and subtitles
├── main.py # Orchestrates the pipeline via CLI
├── requirements.txt # Python dependencies
└── README.md # Project documentation



---

Let me know if you want to customize this further (e.g., add a logo badge, CI setup, API keys handling with `.env`, or support for other news categories).
