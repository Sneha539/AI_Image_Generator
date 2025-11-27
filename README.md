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
### 2.2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux / macOS
source venv/bin/activate

### 2.3. Install dependencies
pip install -r requirements.txt

### 2.4. Model download instructions

The application uses diffusers to load:

runwayml/stable-diffusion-v1-5

On first run, the model weights and configuration are automatically downloaded from Hugging Face and cached locally (inside the user's Hugging Face cache directory).
No manual download is required, but the first generation may take longer due to this download.

## 3. Hardware Requirements (GPU / CPU)
GPU execution (recommended)

Device: CUDA-compatible GPU

VRAM: 6–8 GB or more recommended

Precision: float16 with autocast

Performance:

Typically a few seconds per image depending on resolution and settings

CPU execution

Device: Standard CPU

Precision: float32

Performance:

Approximately 30–60 seconds per image for 512×512 at ~30 steps

Notes:

Works reliably but is considerably slower than GPU.

Best used for low image counts or experimentation.

The application automatically chooses "cuda" if a GPU is available, otherwise falls back to "cpu".
This device is shown in the UI header at runtime.

## 4. Usage Instructions
### 4.1. Run the application
streamlit run app.py


A browser window will open at http://localhost:8501.

### 4.2. Main workflow

Enter a prompt
Example:

"a futuristic city at sunset, highly detailed, cinematic lighting"

Choose a style

Photorealistic

Artistic / Painting

Cartoon / Anime

Concept Art

Set core parameters

Number of images: 1–4

Guidance scale: how strongly the model follows the text

Diffusion steps: more steps = slower but more detailed

(Optional) Advanced settings

Negative prompt: things to avoid

Image height & width: common sizes: 512, 640, 768

Click “Generate Images”.
The app will:

Show a progress bar and estimated completion time

Generate the images

Apply watermark and save them

Display them with download buttons

### 4.3. Example prompts

Photorealistic:

"a cozy study room with warm lighting, wooden desk, bookshelves, ultra realistic, 4k"

Anime / Cartoon:

"a walking almirah of brown color on a road, cartoon anime style, vibrant colors"

Concept Art:

"a colossal floating island above the ocean, dramatic lighting, concept art, highly detailed"

Artistic / Painting:

"a renaissance painting of a knight looking at the stars, oil painting, rich texture"

## 5. Technology Stack & Model Details
Tech stack

Language: Python

Frontend: Streamlit

Backend / ML:

PyTorch

Hugging Face diffusers

Image processing: Pillow

Runtime management: accelerate, safetensors

Model details

Base model: runwayml/stable-diffusion-v1-5

Type: Latent diffusion model for text-to-image generation

Pipeline: StableDiffusionPipeline from diffusers

Default parameters:

Steps: 30

Guidance scale: 7.5

Size: 512×512

Number of images: 1 (user-adjustable)

Safety & ethics:

Simple keyword-based filtering on user prompts

Visible watermark “AI GENERATED” on every output image

Recommendation to avoid harmful, illegal, or deceptive use

## 6. Prompt Engineering Tips & Best Practices

The application uses a simple prompt-engineering layer that extends user prompts based on chosen style.

### 6.1. Style-based extensions

For example:

Photorealistic adds:

"ultra realistic, 8k, professional photography, sharp focus, high dynamic range"

Artistic / Painting adds:

"oil painting, brush strokes, rich texture, artstation, highly detailed"

Cartoon / Anime adds:

"anime style, clean lines, cell shading, vibrant colors"

Concept Art adds:

"concept art, matte painting, dramatic lighting, highly detailed, cinematic"

### 6.2. General best practices

Be specific about:

Subject: "a small cabin in a snowy forest"

Style: "watercolor, studio ghibli inspired"

Lighting: "golden hour, soft light"

Camera / Composition: "wide shot, from above, depth of field"

Combine positive prompt and negative prompt:

Positive: "highly detailed, 4k, cinematic lighting"

Negative: "blurry, low quality, distorted, extra limbs"

Start with default settings (30 steps, guidance 7.5), then adjust:

Increase steps for more detail

Change guidance if image is too literal or not aligned with prompt

## 7. Limitations & Future Improvements
### 7.1. Current limitations

Generation time:

Slow on CPU-only systems, especially for higher resolutions or many steps.

Memory requirements:

GPUs with low VRAM may struggle with larger resolutions.

Safety:

The current content filter is keyword-based and may miss some edge cases.

Model scope:

Stable Diffusion v1.5 is general-purpose but not fine-tuned for very specific domains.

### 7.2. Possible future improvements

Fine-tuning on custom datasets
To specialize the model for specific styles or domains (e.g., product images, medical diagrams, company-specific branding).

Style transfer & LoRA support
Adding support for custom LoRA adapters or style transfer modules to easily switch between different visual styles.

More advanced safety tools
Integrating a stronger NSFW / unsafe-content classifier or automated output screening.

Better configuration management
Loading model and generation parameters directly from configuration files instead of hard-coding them.

Deployment
Packaging the app as a Docker image or deploying to a cloud environment for multi-user access.
