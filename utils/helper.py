from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

prompt = "Futuristic conference room with holographic screens, cinematic lighting"
image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
image.save("visual_asset.jpg")
