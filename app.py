# app.py
import os
import streamlit as st
from model import Text2ImageGenerator
from utils import is_prompt_allowed, add_watermark, save_image_with_metadata

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI-Powered Text-to-Image Generator",
    page_icon="🖼️",
    layout="wide"
)

# ---------- CUSTOM STYLES ----------
st.markdown(
    """
    <style>
    /* Global background */
    .stApp {
        background: radial-gradient(circle at top, #111827 0, #020617 45%, #000000 100%);
        color: #e5e7eb;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* Card style */
    .glass-card {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.55);
    }

    .glass-header {
        background: linear-gradient(135deg, #1e293b, #020617);
        border-radius: 18px;
        padding: 1.5rem 1.8rem;
        border: 1px solid rgba(148, 163, 184, 0.5);
        box-shadow: 0 25px 55px rgba(0, 0, 0, 0.75);
    }

    .section-title {
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 0.35rem;
    }

    .prompt-label {
        font-weight: 600;
        font-size: 0.95rem;
        color: #e5e7eb;
    }

    .tip-text {
        font-size: 0.85rem;
        color: #9ca3af;
    }

    .footer-text {
        font-size: 0.8rem;
        color: #6b7280;
        text-align: center;
        margin-top: 1.5rem;
    }

    /* Hide Streamlit default menu/footer/logo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- MODEL (CACHED) ----------
@st.cache_resource
def load_generator():
    return Text2ImageGenerator()

generator = load_generator()

# ---------- HEADER ----------
st.markdown(
    """
    <div class="glass-header">
        <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
            <div style="
                width: 52px;
                height: 52px;
                border-radius: 18px;
                background: radial-gradient(circle at 30% 30%, #22d3ee, #6366f1);
                display:flex;
                align-items:center;
                justify-content:center;
                font-size: 1.7rem;
            ">
                🖼️
            </div>
            <div style="flex:1; min-width:200px;">
                <h1 style="margin:0; font-size:1.9rem; color:#f9fafb; font-weight:700;">
                    AI-Powered Text-to-Image Generator
                </h1>
                <p style="margin:0.3rem 0 0; color:#9ca3af; font-size:0.9rem;">
                    Transform plain text into high-quality images using an open-source Stable Diffusion pipeline.
                </p>
            </div>
            <div style="text-align:right; min-width:170px;">
                <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.12em; color:#9ca3af;">
                    Runtime Device
                </div>
                <div style="font-weight:600; color:#e5e7eb; font-size:0.95rem;">
                    {device}
                </div>
                <div style="font-size:0.8rem; color:#6b7280;">
                    Auto-detected (GPU if available)
                </div>
            </div>
        </div>
    </div>
    """.format(device=generator.device),
    unsafe_allow_html=True
)

st.markdown("")  # spacer

# ---------- LAYOUT ----------
left_col, right_col = st.columns([1.1, 1.2])

# ========== LEFT: CONTROLS ==========
with left_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Prompt</div>', unsafe_allow_html=True)
    st.markdown('<div class="prompt-label">Describe the scene you want to generate</div>', unsafe_allow_html=True)

    prompt = st.text_area(
        label="",
        value="a futuristic city at sunset, highly detailed, 4K, cinematic lighting",
        height=110,
        placeholder="Example: a cozy study room with warm lights, cinematic, ultra detailed"
    )

    st.markdown(
        '<div class="tip-text">💡 Tip: Add mood, lighting, and style keywords for better results.</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Style & core sliders
    st.markdown('<div class="section-title">Style & Quality</div>', unsafe_allow_html=True)

    style = st.selectbox(
        "Artistic style",
        ["Photorealistic", "Artistic / Painting", "Cartoon / Anime", "Concept Art"],
        help="Choose the overall look & vibe of the output image."
    )

    c1, c2 = st.columns(2)
    with c1:
        num_images = st.slider(
            "Number of images",
            min_value=1,
            max_value=4,
            value=1,
            help="Generate multiple variations for the same prompt."
        )
    with c2:
        guidance_scale = st.slider(
            "Guidance scale",
            min_value=3.0,
            max_value=15.0,
            value=7.5,
            step=0.5,
            help="Higher values follow the text more strictly but can reduce creativity."
        )

    steps = st.slider(
        "Diffusion steps",
        min_value=10,
        max_value=50,
        value=30,
        step=5,
        help="More steps = slower but sharper & more detailed images."
    )

    with st.expander("Advanced controls", expanded=False):
        negative_prompt_input = st.text_area(
            "Negative prompt",
            value="low quality, blurry, distorted, extra limbs",
            height=80,
            help="Describe what you want to avoid in the image."
        )

        c3, c4 = st.columns(2)
        with c3:
            height = st.selectbox("Image height", [512, 640, 768], index=0)
        with c4:
            width = st.selectbox("Image width", [512, 640, 768], index=0)

    # Generate button
    st.markdown("")
    generate_button = st.button(
        "🚀 Generate Images",
        use_container_width=True,
        type="primary"
    )

    st.markdown('</div>', unsafe_allow_html=True)  # close glass-card

# ========== RIGHT: OUTPUT & STATUS ==========
with right_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Output</div>', unsafe_allow_html=True)
    status_box = st.empty()
    progress_text = st.empty()
    progress_bar = st.empty()

    output_dir = "outputs"

    # Style prompt enhancement
    def apply_style(prompt_text: str, style_choice: str) -> str:
        style_prompts = {
            "Photorealistic": "ultra realistic, 8k, professional photography, sharp focus, high dynamic range",
            "Artistic / Painting": "oil painting, brush strokes, rich texture, artstation, highly detailed",
            "Cartoon / Anime": "anime style, clean lines, cell shading, vibrant colors",
            "Concept Art": "concept art, matte painting, dramatic lighting, highly detailed, cinematic"
        }
        return f"{prompt_text}, {style_prompts.get(style_choice, '')}"

    # Handle generation
    if generate_button:
        if not prompt.strip():
            status_box.error("Prompt cannot be empty.")
        elif not is_prompt_allowed(prompt):
            status_box.error("Prompt violates content guidelines. Please enter a safer description.")
        else:
            styled_prompt = apply_style(prompt, style)

            status_box.info("Generation started. This may take some time depending on your hardware.")
            progress_bar = st.progress(0)

            if generator.device == "cuda":
                est = "a few seconds per image (GPU)"
            else:
                est = "around 30–60 seconds per image (CPU, slower)"

            progress_text.markdown(
                f"**Estimated completion:** `{est}` &nbsp;&nbsp;•&nbsp;&nbsp; "
                f"Steps: `{steps}` &nbsp;|&nbsp; Guidance: `{guidance_scale}`"
            )

            params = {
                "num_images": num_images,
                "guidance_scale": guidance_scale,
                "steps": steps,
                "height": height,
                "width": width,
                "device": generator.device,
                "style": style
            }

            progress_bar.progress(10)
            progress_text.markdown("🔧 Preparing model & pipeline...")

            images = generator.generate(
                prompt=styled_prompt,
                negative_prompt=negative_prompt_input,
                num_images=num_images,
                guidance_scale=guidance_scale,
                num_inference_steps=steps,
                height=height,
                width=width
            )

            progress_bar.progress(70)
            progress_text.markdown("✨ Post-processing: adding watermark & saving images...")

            cols = st.columns(num_images)
            saved_paths = []

            for idx, img in enumerate(images):
                wm_img = add_watermark(img)

                png_path, jpg_path, metadata_path = save_image_with_metadata(
                    wm_img,
                    base_dir=output_dir,
                    prompt=styled_prompt,
                    negative_prompt=negative_prompt_input,
                    params=params,
                    index=idx
                )
                saved_paths.append((png_path, jpg_path, metadata_path))

                with cols[idx]:
                    st.image(
                        wm_img,
                        caption=f"Variant {idx+1}",
                        use_container_width=True
                    )
                    st.download_button(
                        label="Download PNG",
                        data=open(png_path, "rb").read(),
                        file_name=os.path.basename(png_path),
                        mime="image/png",
                        key=f"png_{idx}"
                    )
                    st.download_button(
                        label="Download JPG",
                        data=open(jpg_path, "rb").read(),
                        file_name=os.path.basename(jpg_path),
                        mime="image/jpeg",
                        key=f"jpg_{idx}"
                    )

            progress_bar.progress(100)
            progress_text.markdown("✅ Generation completed.")
            status_box.success("Images generated, watermarked, and saved with metadata.")

    else:
        st.markdown(
            '<div class="tip-text">Generate an image to see results here. '
            'Use the left panel to craft your prompt and tweak quality settings.</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)  # close glass-card

# ---------- FOOTER ----------
st.markdown(
    '<div class="footer-text">Built with Stable Diffusion, Streamlit, and a slightly overworked brain.</div>',
    unsafe_allow_html=True
)
