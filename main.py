import os
import re

from news_scraper import get_trending_news
from script_generator import generate_script_from_news, save_script_to_file
from utils.image_generator import process_all_scripts, generate_images_from_script
from video_generator import create_video_from_images

SCRIPT_DIR = r"E:\SynLab-InternAssignment\SynLabs-GenAI_Task1\assets\generated_scripts"
IMAGE_DIR = r"E:\SynLab-InternAssignment\SynLabs-GenAI_Task1\assets\generated_images"
VIDEO_DIR = r"E:\SynLab-InternAssignment\SynLabs-GenAI_Task1\assets\generated_videos"
image_root_folder = "assets/generated_images"

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(" ", "_")

def list_generated_scripts():
    scripts = [f for f in os.listdir(SCRIPT_DIR) if f.endswith(".txt")]
    for idx, script in enumerate(scripts, 1):
        print(f"{idx}. {script}")
    return scripts

def list_generated_folders():
    folders = [f for f in os.listdir(IMAGE_DIR) if os.path.isdir(os.path.join(IMAGE_DIR, f))]
    for idx, folder in enumerate(folders, 1):
        print(f"{idx}. {folder}")
    return folders

def delete_selected(items, base_dir, item_type):
    print(f"\nEnter the numbers of the {item_type} you want to delete (comma separated): ")
    selection = input()
    indices = [int(i.strip()) for i in selection.split(",") if i.strip().isdigit()]
    for idx in indices:
        if 1 <= idx <= len(items):
            target = os.path.join(base_dir, items[idx - 1])
            if os.path.isdir(target):
                for file in os.listdir(target):
                    os.remove(os.path.join(target, file))
                os.rmdir(target)
            elif os.path.isfile(target):
                os.remove(target)

def main():
    print("Fetching trending tech news...\n")
    news_items = get_trending_news()

    if not news_items:
        print("No news articles found. Exiting.")
        return

    print("Top Articles:\n")
    for idx, news in enumerate(news_items, 1):
        print(f"{idx}. {news['title']}")
        print(f"   {news['description']}\n")

    selected = input("Enter article numbers to use (comma separated): ")
    selected_indices = [int(i.strip()) for i in selected.split(",") if i.strip().isdigit()]

    for idx in selected_indices:
        if idx < 1 or idx > len(news_items):
            print(f"Skipping invalid index: {idx}")
            continue

        article = news_items[idx - 1]
        title = article['title']
        description = article['description']
        url = article.get('url')

        print(f"\nGenerating script for: {title}")
        script = generate_script_from_news(title, description, url)
        save_script_to_file(title, script)

        scripts = list_generated_scripts()
        if not scripts:
            print("No scripts found.")
            return

        choice = input("\nEnter the number of the script you want to turn into a video: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(scripts):
            print("Invalid selection. Exiting.")
            return

        selected_script_file = scripts[int(choice) - 1]
        script_name = os.path.splitext(selected_script_file)[0]
        sanitized_name = sanitize_filename(script_name)

        script_path = os.path.join(SCRIPT_DIR, selected_script_file)
        output_video_path = os.path.join(VIDEO_DIR, f"{sanitized_name}.mp4")

        print(f"\nGenerating images for script: {script_name}")
        generate_images_from_script(script_path, output_dir=IMAGE_DIR)

        print(f"\nCreating video from images...")
        create_video_from_images(IMAGE_DIR, script_path, output_video_path)

        print(f"\nVideo saved at: {output_video_path}")

    decision = input("\nDo you want to keep the generated scripts and images? (yes/no): ").strip().lower()

    if decision in ['yes', 'y']:
        print("Exiting.")
        return
    else:
        print("\nGenerated Scripts:")
        scripts = list_generated_scripts()
        if scripts:
            delete_selected(scripts, SCRIPT_DIR, "scripts")

        print("\nGenerated Image Folders:")
        folders = list_generated_folders()
        if folders:
            delete_selected(folders, IMAGE_DIR, "image folders")

        print("Cleanup complete. Exiting.")

if __name__ == "__main__":
    main()
