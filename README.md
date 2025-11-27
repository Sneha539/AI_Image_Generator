# AI-Powered Text-to-Image Generator

This project is a local text-to-image generation system built with an open-source Stable Diffusion model, a Streamlit web interface, and a PyTorch backend.  
Given a natural-language prompt, the application generates one or more images, supports multiple visual styles, and includes basic safety mechanisms such as prompt filtering and visible watermarking.

---

## 1. Project Overview & Architecture

### High-level description

- **Goal**: Allow a user to type a text prompt and generate AI-created images locally.
- **Model**: Stable Diffusion v1.5, loaded via the `diffusers` library.
- **Interface**: Streamlit web app for easy interaction.
- **Backend**: PyTorch for model execution (GPU if available, otherwise CPU).

### Architecture components

1. **Frontend (Streamlit, `app.py`)**
   - Collects user input:
     - Prompt text
     - Style (Photorealistic, Artistic / Painting, Cartoon / Anime, Concept Art)
     - Number of images
     - Guidance scale
     - Diffusion steps
     - Optional negative prompt
     - Image resolution
   - Displays:
     - Progress and estimated completion time
     - Generated images
     - Download buttons for PNG and JPEG
   - Uses a custom-styled layout with separate panels for controls and outputs.

2. **Model Layer (`model.py`)**
   - Uses `StableDiffusionPipeline` from `diffusers`.
   - Automatically detects hardware:
     - **GPU (cuda)**: uses `float16` and autocasting for performance.
     - **CPU**: uses `float32`, slower but still functional.
   - Exposes a `generate()` method that receives prompts and generation parameters and returns PIL images.

3. **Utility Layer (`utils.py`)**
   - **Content filtering**: simple keyword-based filtering for unsafe prompts.
   - **Watermarking**: adds an “AI GENERATED” label to each final image using Pillow.
   - **Saving & metadata**:
     - Saves PNG and JPEG versions into an `outputs/` directory.
     - Creates a JSON file with prompt, negative prompt, timestamp, parameters and file paths.

4. **Configuration (`config/model_config.json`)**
   - Documents:
     - Model name and framework
     - Default image size
     - Default generation parameters
     - Safety and watermarking strategy

5. **Samples (`samples/`)**
   - Contains example generated images and a `samples_metadata.json` file describing the prompts and styles used.

---

## 2. Setup & Installation

### 2.1. Prerequisites

- Python 3.9+ recommended
- Git
- (Optional but recommended) A GPU with at least 6–8 GB VRAM for faster generation