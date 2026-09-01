import json
import logging
from typing import Any, Dict
from groq import AsyncGroq
import groq
from app.config import settings

logger = logging.getLogger(__name__)

class AgentGenerationError(Exception):
    """Exception raised when an agent fails to generate a valid response."""
    pass

class GroqClient:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY is not set. Groq client will fail on calls.")
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY, max_retries=2)

    async def chat_json(
        self, system_prompt: str, user_payload: dict, response_schema: dict, model: str
    ) -> dict:
        """
        Calls the Groq API enforcing a JSON return format.
        """
        # Append schema description to system prompt for guaranteed adherence
        enhanced_system_prompt = (
            f"{system_prompt}\n\n"
            f"You MUST respond ONLY with a JSON object matching this schema:\n"
            f"{json.dumps(response_schema, indent=2)}"
        )

        messages = [
            {"role": "system", "content": enhanced_system_prompt},
            {"role": "user", "content": json.dumps(user_payload)},
        ]

        # First attempt with json_object mode (universal support across all Groq models)
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.2,
                response_format={"type": "json_object"},
                timeout=60.0
            )
            response_content = chat_completion.choices[0].message.content
            return json.loads(response_content)

        except groq.APIConnectionError as e:
            logger.error(f"Groq API connection error: {e}")
            raise AgentGenerationError("Failed to connect to the LLM service.") from e
        except groq.RateLimitError as e:
            logger.error(f"Groq API rate limit error: {e}")
            raise AgentGenerationError("Rate limit exceeded. Please try again later.") from e
        except groq.APIStatusError as e:
            logger.error(f"Groq API status error: {e.status_code} - {e.response}")
            raise AgentGenerationError(f"LLM service returned an error: {e.status_code}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response as JSON: {e}")
            raise AgentGenerationError("Agent returned invalid JSON.") from e
        except Exception as e:
            logger.error(f"Unexpected error in Groq client: {e}")
            raise AgentGenerationError(f"Generation error: {str(e)}") from e

groq_client = GroqClient()
