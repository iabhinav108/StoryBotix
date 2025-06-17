import os
import re
import torch
from transformers import pipeline
from diffusers import StableDiffusionPipeline
from PIL import Image

print("Loading FLAN-T5 for prompt generation...")
prompt_extractor = pipeline("text2text-generation", model="google/flan-t5-base")

print("Loading Stable Diffusion model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
sd_pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
sd_pipe.to(device)

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(" ", "_")

def clean_script_text(script_text):
    return re.sub(r'https?://\S+', '', script_text)

def extract_prompts(script_text, min_prompts=8, max_prompts=10):
    cleaned_text = clean_script_text(script_text)

    input_prompt = (
        f"Extract {min_prompts} to {max_prompts} visual scene descriptions from this news script "
        f"that can be turned into images:\n\n{cleaned_text}\n\n"
        f"Return one scene description per line."
    )

    response = prompt_extractor(input_prompt, max_new_tokens=300)[0]['generated_text']
    prompts = [line.strip("-•.1234567890 ").strip() for line in response.split("\n") if len(line.strip()) > 3]

    while len(prompts) < min_prompts:
        prompts.append(prompts[-1])

    return prompts[:max_prompts]

def generate_images_from_script(script_path, output_dir="assets/generated_images"):
    raw_name = os.path.splitext(os.path.basename(script_path))[0]
    script_name = sanitize_filename(raw_name)

    
    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    print(f"Processing script: {script_name}")
    prompts = extract_prompts(script_text)

    if not prompts:
        print(f"No prompts extracted from: {script_name}")
        return

    script_output_folder = os.path.join(output_dir, script_name)
    os.makedirs(script_output_folder, exist_ok=True)

    for idx, prompt in enumerate(prompts, start=1):
        print(f"Generating image {idx}/{len(prompts)}: {prompt}")
        try:
            image = sd_pipe(prompt, num_inference_steps=40, guidance_scale=7.5, height=512, width=512).images[0]
            image.save(os.path.join(script_output_folder, f"scene_{idx:02d}.jpg"))
        except Exception as e:
            print(f"Failed to generate image for prompt {idx}: {e}")

    print(f"{len(prompts)} images saved for script: {script_name}")



def process_all_scripts(script_folder="assets/generated_scripts"):
    # load_models()
    for filename in os.listdir(script_folder):
        if filename.endswith(".txt"):
            script_path = os.path.join(script_folder, filename)
            generate_images_from_script(script_path)