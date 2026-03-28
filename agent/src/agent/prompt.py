"""System prompt and analysis logic for the guessing game agent.

=== EDIT THIS FILE ===

This is where you define your agent's strategy:
- What system prompt to use
- How to analyze each frame
- When to submit a guess vs. gather more context
"""

from __future__ import annotations

from core import Frame

# ---------------------------------------------------------------------------
# System prompt — tweak this to improve your agent's guessing ability.
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


async def analyze(frame: Frame) -> str | None:
    """Analyze a single frame and return a guess, or None to skip.

    This is the core function you should customize. The default
    implementation is a simple placeholder that always skips.

    Args:
        frame: A Frame with .image (PIL Image) and .timestamp.

    Returns:
        A text guess string, or None to skip this frame.
    """
    # -----------------------------------------------------------------
    # TODO: Replace this with your actual vision LLM call.
    #
    # Example with pydantic-ai:
    
    import io
    from pydantic_ai import Agent, BinaryContent
    from pydantic_ai.models.openrouter import OpenRouterModel
    from pydantic_ai.providers.openrouter import OpenRouterProvider
    import os
    image_stream = io.BytesIO()
    # Saving as JPEG is usually safest and most efficient for API calls
    frame.image.save(image_stream, format="JPEG") 
    image_bytes = image_stream.getvalue()

    # 2. Initialize the OpenRouter model
    model = OpenRouterModel(
        "anthropic/claude-3.5-sonnet",
        provider=OpenRouterProvider(api_key=os.getenv("OPENROUTER_API_KEY")),
    )
    agent = Agent(model)

    # 3. Send the prompt and the image bytes to Claude
    result = await agent.run(
        [
            "What do you see in this image? If there is nothing notable or useful, reply with exactly 'SKIP'.",
            BinaryContent(data=image_bytes, media_type="image/jpeg")
        ]
    )
    
    answer = result.output.strip()
    return None if answer == "SKIP" else answer