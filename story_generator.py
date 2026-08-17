import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load environment variables

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN not found. Please check your .env file."
    )


# Hugging Face client

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="nscale"
)


# Story generation function

def generate_story(
    caption,
    story_style="Adventure",
    story_length="Medium",
    custom_instruction=""
):

    # Story length

    if story_length == "Short":
        min_words = 50
        max_words = 80

    elif story_length == "Medium":
        min_words = 100
        max_words = 150

    else:
        min_words = 180
        max_words = 250


    # detailed Story styles

    style_instructions = {

        "Adventure": """
Include exploration, discovery, excitement,
or a small challenge.

The character should experience something
adventurous.
""",

        "Funny": """
Include humor, funny situations,
or unexpected moments.

Make the story entertaining and playful.
""",

        "Emotional": """
Focus on feelings, relationships,
memories, or a meaningful moment.

Make the story touching and heartfelt.
""",

        "Mystery": """
Include a mystery, strange clue,
hidden secret, or unanswered question.

Create curiosity and suspense.
""",

        "Cinematic": """
Write like a movie scene.

Use vivid scenes, atmosphere,
visual details, and dramatic moments.
"""
    }


    selected_style = style_instructions.get(
        story_style,
        style_instructions["Adventure"]
    )


    # Prompt writing here
    prompt = f"""
You are a creative story writer.

Create a short fictional story based on
the following image description.

IMAGE DESCRIPTION:
{caption}

SELECTED STORY STYLE:
{story_style}

STYLE INSTRUCTIONS:
{selected_style}

STORY LENGTH:
The story must contain approximately
{min_words} to {max_words} words.

ADDITIONAL USER INSTRUCTION:
{custom_instruction}

IMPORTANT RULES:

1. Write ONLY the story.
2. Give the story a short creative title.
3. Follow the selected story style strongly.
4. Make the story creative and engaging.
5. Use the image description as the main inspiration.
6. Do NOT explain the image.
7. Do NOT provide a separate image description.
8. Do NOT provide analysis.
9. Do NOT provide a summary.
10. Do NOT write "Explanation of the Picture".
11. Do NOT mention these instructions.
12. Keep the complete response around
    {min_words}-{max_words} words.
"""


    # Streaming response

    stream = client.chat_completion(

        model="Qwen/Qwen3-4B-Instruct-2507",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        max_tokens=max_words + 40,

        temperature=0.7,

        stream=True
    )

    for chunk in stream:
        if chunk.choices:
            text = chunk.choices[0].delta.content
            if text:
                yield text