from __future__ import annotations

import io
import os
from dotenv import load_dotenv

from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from core import Frame

# Force load the environment variables directly in this file
load_dotenv()

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are playing a visual guessing game. You will receive a screenshot from a
live camera feed. Your goal is to identify what is being shown as quickly and
accurately as possible.

Rules:
- Give your best guess as a short, specific answer (1-5 words).
- If you're not confident enough yet, respond with exactly "SKIP".
- Be specific: "golden retriever" is better than "dog".
- You only get to see one frame at a time, so make it count.
"""

# ---------------------------------------------------------------------------
# Agent setup
# ---------------------------------------------------------------------------

vision_model_id = "anthropic/claude-3.5-sonnet" 

llm_api_key = os.environ.get("LLM_API_KEY")
if not llm_api_key:
    raise RuntimeError(
        "Could not find LLM_API_KEY. Please ensure your .env file is saved in the "
        "root directory and does not have a hidden .txt extension."
    )

model = OpenRouterModel(
    vision_model_id,
    provider=OpenRouterProvider(
        api_key=llm_api_key
    ),
)

agent = Agent(model, system_prompt=SYSTEM_PROMPT)

async def analyzeFrame(frame: Frame) -> str | None:
    """Analyze a single frame and return a guess, or None to skip."""
    
    # Convert PIL Image to PNG bytes for the LLM
    image_buffer = io.BytesIO()
    frame.image.save(image_buffer, format="PNG")
    image_bytes = image_buffer.getvalue()

    result_response = await agent.run(
        [
            "What do you see in this image? Give your best guess.",
            BinaryContent(data=image_bytes, media_type="image/png"),
        ],
    )
    
    answer_string = result_response.output.strip()
    return None if answer_string == "SKIP" else answer_string

# Alias to keep compatibility with __main__.py which imports 'analyze'
analyze = analyzeFrame