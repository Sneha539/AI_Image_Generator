# model.py
import torch
from diffusers import StableDiffusionPipeline

class Text2ImageGenerator:
    def __init__(self, model_name: str = "runwayml/stable-diffusion-v1-5"):
        # Detect device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        # Load pipeline
        dtype = torch.float16 if self.device == "cuda" else torch.float32

        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=dtype,
            safety_checker=None  # simple manual filtering will be used instead
        )

        self.pipe = self.pipe.to(self.device)

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_images: int = 1,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 30,
        height: int = 512,
        width: int = 512
    ):
        # Autocast for GPU to save memory and speed up
        if self.device == "cuda":
            with torch.autocast(self.device):
                result = self.pipe(
                    prompt=[prompt] * num_images,
                    negative_prompt=[negative_prompt] * num_images if negative_prompt else None,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    height=height,
                    width=width
                )
        else:
            result = self.pipe(
                prompt=[prompt] * num_images,
                negative_prompt=[negative_prompt] * num_images if negative_prompt else None,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                height=height,
                width=width
            )

        images = result.images
        return images
