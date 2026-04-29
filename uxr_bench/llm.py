"""
Optional LLM evaluation backend.

Requires: pip install uxr-bench[openai|anthropic|gemini]
Triggered only when --llm-backend is passed to the CLI.
No API calls are made in rule-based / baseline mode.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import BenchmarkTask

try:
    import litellm

    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

BACKEND_MODELS: dict[str, str] = {
    "openai": "openai/gpt-4o-mini",
    "anthropic": "anthropic/claude-haiku-4-5-20251001",
    "gemini": "gemini/gemini-2.0-flash",
}


def get_llm_response(prompt: str, backend: str) -> str:
    """
    Send a prompt to the specified LLM backend and return the raw text response.

    Args:
        prompt:  The fully-rendered task prompt.
        backend: One of 'openai', 'anthropic', 'gemini'.

    Returns:
        The model's response text, stripped of leading/trailing whitespace.

    Raises:
        ImportError:  If ``litellm`` is not installed.
        ValueError:   If ``backend`` is not recognised.
    """
    if not HAS_LITELLM:
        raise ImportError(
            "litellm is required for LLM evaluation. "
            "Install with: pip install 'uxr-bench[openai]'  (or anthropic / gemini)"
        )
    model = BACKEND_MODELS.get(backend)
    if not model:
        raise ValueError(
            f"Unknown backend '{backend}'. Choose from: {list(BACKEND_MODELS)}"
        )

    response = litellm.completion(  # type: ignore[attr-defined]
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=256,
    )
    return response.choices[0].message.content.strip()


def make_llm_response_fn(backend: str) -> Callable[[BenchmarkTask], str]:
    """
    Return a response function compatible with :meth:`BenchmarkEvaluator.run_task`.

    The returned callable accepts a :class:`BenchmarkTask`, renders its prompt,
    and calls the specified LLM backend.
    """

    def response_fn(task: BenchmarkTask) -> str:
        prompt = task.render_prompt()
        return get_llm_response(prompt, backend)

    return response_fn
