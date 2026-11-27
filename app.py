import os
import time
import streamlit as st

st.set_page_config(
    page_title="Ruang Aneh AI Video Generator",
    page_icon="👁️",
    layout="wide"
)

# ============================================================
# CONFIG
# ============================================================

DEFAULT_NEGATIVE = """
low quality, blurry, cartoon, anime, illustration, 3d render,
unrealistic CGI, distorted face, deformed hands, extra fingers,
duplicate characters, extra people, inconsistent character,
different clothes, different hairstyle, bad anatomy,
text overlay, watermark, logo, poster, thumbnail,
blood, gore, graphic violence, excessive monster effects,
extreme jumpscare, overexposed, oversaturated
"""

# ============================================================
# STYLE
# ============================================================

st.title("👁️ RUANG ANEH — AI HORROR VIDEO GENERATOR")
st.caption("Realistic Indonesian horror short-film workflow")

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("⚙️ Pengaturan")

    model = st.selectbox(
        "Model Video",
        [
            "veo-3.1-fast-generate-001",
            "veo-3.1-generate-001"
        ]
    )

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["9:16", "16:9"]
    )

    duration = st.selectbox(
        "Durasi setiap scene",
        [4, 6, 8],
        index=2
    )

    st.divider()

    st.info(
        "Video AI membutuhkan akses/API Google Cloud "
        "dan dapat dikenakan biaya."
    )

# ============================================================
# INPUT CERITA
# ============================================================

st.subheader("🎬 Cerita")

story = st.text_area(
    "Masukkan cerita horror",
    height=180,
    placeholder=(
        "Contoh:\n"
        "Dimas naik bus terakhir pukul 23:47. "
        "Di dalam bus ada seorang perempuan misterius. "
        "Ketika Dimas bertanya kepada sopir, sopir mengatakan "
        "bahwa Dimas naik sendirian."
    )
)

character = st.text_area(
    "Deskripsi karakter utama",
    height=120,
    value=(
        "Dimas, young Indonesian man, messy black hair, "
        "black hoodie, dark pants, small black backpack, "
        "realistic human appearance, natural facial expressions."
    )
)

visual_style = st.text_area(
    "Gaya visual",
    height=100,
    value=(
        "Photorealistic cinematic Indonesian horror, "
        "realistic human actors, natural lighting, "
        "cold blue night lighting, realistic camera movement, "
        "subtle psychological horror, cinematic film look."
    )
)

negative_prompt = st.text_area(
    "Negative prompt",
    height=150,
    value=DEFAULT_NEGATIVE.strip()
)

# ============================================================
# SCENE GENERATOR
# ============================================================

def create_scenes(story, character, visual_style):
    """
    Membuat template 8 scene.
    Untuk tahap awal, scene dibagi berdasarkan struktur
    film pendek horror.
    """

    return [
        {
            "title": "Scene 1 — Pembuka",
            "prompt": f"""
Create the opening scene of a realistic Indonesian horror short film.

Story:
{story}

Character:
{character}

The scene must establish the location, time and atmosphere.
Use realistic human acting, cinematic camera movement and
natural environmental details.

Visual style:
{visual_style}

Start directly with the live-action scene.
Do not show a poster, thumbnail, title card or reference image.
"""
        },

        {
            "title": "Scene 2 — Kejanggalan",
            "prompt": f"""
Continue directly from the previous scene.

Story:
{story}

Character:
{character}

Introduce the first strange event naturally.
Keep the character's face, hairstyle, clothing and physical
appearance exactly consistent with the previous scene.

Visual style:
{visual_style}

No exaggerated supernatural effects.
"""
        },

        {
            "title": "Scene 3 — Pertemuan",
            "prompt": f"""
Continue directly from the previous scene.

Story:
{story}

Character:
{character}

Show the main character encountering the mysterious element
of the story.

Use subtle psychological horror.
Natural Indonesian environment.
Realistic human movement and facial expressions.

Visual style:
{visual_style}
"""
        },

        {
            "title": "Scene 4 — Kejanggalan Semakin Jelas",
            "prompt": f"""
Continue directly from the previous scene.

Story:
{story}

Character:
{character}

The supernatural mystery becomes more obvious,
but keep everything realistic and restrained.

Maintain exact character continuity.

Visual style:
{visual_style}
"""
        },

        {
            "title": "Scene 5 — Kebenaran",
            "prompt": f"""
Continue directly from the previous scene.

Story:
{story}

Character:
{character}

The main character discovers information that contradicts
what he previously believed.

Build tension through acting, camera movement and sound
rather than gore or excessive effects.

Visual style:
{visual_style}
"""
        },

        {
            "title": "Scene 6 — Pengungkapan",
            "prompt": f"""
Continue directly from the previous scene.

Story:
{story}

Character:
{character}

Reveal an important supernatural clue.
The audience should understand that something impossible
is happening.

Keep the horror realistic and cinematic.

Visual style:
{visual_style}
"""
        },

        {
            "title": "Scene 7 — Puncak",
            "prompt": f"""
Continue directly from the previous scene.

Story:
{story}

Character:
{character}

Create the strongest suspense moment of the film.
The main character realizes that he may be trapped
inside the supernatural situation.

Keep the character visually consistent.

Visual style:
{visual_style}
"""
        },

        {
            "title": "Scene 8 — Twist Ending",
            "prompt": f"""
Continue directly from the previous scene.

Story:
{story}

Character:
{character}

Create a disturbing but non-graphic final twist.
End with an unanswered mystery that makes the audience
want to watch the story again.

No explanation after the final reveal.

Visual style:
{visual_style}
"""
        }
    ]


# ============================================================
# GENERATE SCENES
# ============================================================

if st.button("🧠 BUAT 8 SCENE", use_container_width=True):

    if not story.strip():
        st.error("Masukkan cerita terlebih dahulu.")
    else:
        scenes = create_scenes(
            story,
            character,
            visual_style
        )

        st.session_state["scenes"] = scenes

        st.success("8 scene berhasil dibuat!")

# ============================================================
# SHOW SCENES
# ============================================================

if "scenes" in st.session_state:

    st.divider()
    st.subheader("🎞️ Storyboard")

    for index, scene in enumerate(
        st.session_state["scenes"],
        start=1
    ):

        with st.expander(
            f"{index}. {scene['title']}",
            expanded=False
        ):

            st.text_area(
                "Prompt",
                scene["prompt"].strip(),
                height=280,
                key=f"prompt_{index}"
            )

            st.text_area(
                "Negative Prompt",
                negative_prompt,
                height=120,
                key=f"negative_{index}"
            )

            st.caption(
                f"Durasi target: {duration} detik • "
                f"Format: {aspect_ratio}"
            )

# ============================================================
# VIDEO GENERATION
# ============================================================

st.divider()
st.subheader("🎥 Generate Video")

st.warning(
    "Bagian ini membutuhkan Google Cloud / Vertex AI "
    "yang sudah memiliki akses ke model video."
)

if st.button(
    "🎬 GENERATE SCENE 1",
    use_container_width=True
):

    if "scenes" not in st.session_state:
        st.error("Buat 8 scene terlebih dahulu.")
    else:

        try:
            from google import genai
            from google.genai.types import GenerateVideosConfig

            project_id = os.environ.get(
                "GOOGLE_CLOUD_PROJECT"
            )

            location = os.environ.get(
                "GOOGLE_CLOUD_LOCATION",
                "global"
            )

            if not project_id:
                st.error(
                    "GOOGLE_CLOUD_PROJECT belum diatur."
                )
                st.stop()

            client = genai.Client(
                vertexai=True,
                project=project_id,
                location=location
            )

            scene_prompt = (
                st.session_state["scenes"][0]["prompt"]
                + "\n\nNEGATIVE PROMPT:\n"
                + negative_prompt
            )

            with st.spinner(
                "Mengirim Scene 1 ke model video..."
            ):

                operation = client.models.generate_videos(
                    model=model,
                    prompt=scene_prompt,
                    config=GenerateVideosConfig(
                        aspect_ratio=aspect_ratio,
                        duration_seconds=duration
                    )
                )

                while not operation.done:
                    time.sleep(15)
                    operation = client.operations.get(
                        operation
                    )

            if operation.response:

                generated_video = (
                    operation.response
                    .generated_videos[0]
                    .video
                )

                output_path = "scene_01.mp4"

                generated_video.save(
                    output_path
                )

                st.success(
                    "Scene 1 berhasil dibuat!"
                )

                st.video(output_path)

                with open(
                    output_path,
                    "rb"
                ) as video_file:

                    st.download_button(
                        "⬇️ Download Scene 1",
                        video_file,
                        file_name="scene_01.mp4",
                        mime="video/mp4"
                    )

            else:
                st.error(
                    "Video tidak berhasil dibuat."
                )

        except ImportError:
            st.error(
                "Library google-genai belum terpasang. "
                "Nanti kita masukkan ke requirements.txt."
            )

        except Exception as e:
            st.error(
                f"Terjadi error: {e}"
            )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RUANG ANEH • Realistic AI Horror Short Film Generator"
                 )
