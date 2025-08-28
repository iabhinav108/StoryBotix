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
├── assets/                        # Static assets (e.g. audio templates, logos)
├── generated_scripts/            # Auto-saved scripts generated from news
├── generated_images/             # Auto-generated image folders (grouped per script)
├── generated_videos/             # Final rendered videos with narration and subtitles
├── utils/                        # Utility modules and helper functions
│   └── image_generator.py        # Generates images based on script content
├── news_scraper.py               # Fetches trending news using NewsAPI
├── script_generator.py           # Generates readable scripts from raw news
├── video_generator.py            # Creates final video with narration, images, and subtitles
├── main.py                       # CLI entry point that runs the full pipeline
├── requirements.txt              # Lists all Python dependencies
└── README.md                     # Project documentation


---

Let me know if you want to customize this further (e.g., add a logo badge, CI setup, API keys handling with `.env`, or support for other news categories).
