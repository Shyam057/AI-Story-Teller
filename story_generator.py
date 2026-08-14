import ollama


def generate_story(
    caption,
    story_style="Adventure",
    story_length="Medium",
    custom_instruction=""
):

    prompt = f"""
Create a {story_style} story based on this image description:

{caption}

Story length: {story_length}

Additional instruction:
{custom_instruction}

Requirements:
- Make the story creative and engaging.
- Give the story a suitable title.
"""

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]