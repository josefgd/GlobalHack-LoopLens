from collections import Counter

MODES = {
    "generation": ["implement", "generate", "create", "fix", "refactor", "write", "build"],
    "understanding": ["what does", "why", "where does", "how does", "explain", "depends on", "breaks if"],
    "planning": ["plan","step","steps","first","next","approach","roadmap","break down","sequence"],
    "verification": ["review", "edge cases", "did i miss", "validate", "check", "risk"],
    "exploration": ["alternatives", "tradeoffs", "compare", "options", "another approach"],
}


def classify_prompt(prompt: str) -> str:
    text = prompt.lower()

    scores = {}
    for mode, keywords in MODES.items():
        scores[mode] = sum(1 for keyword in keywords if keyword in text)

    max_score = max(scores.values())

    if max_score == 0:
        return "unknown"

    priority = [
        "understanding",
        "planning",
        "verification",
        "exploration",
        "generation",
    ]

    for mode in priority:
        if scores.get(mode) == max_score:
            return mode

    return "unknown"


def extract_user_prompts(conversation_log: str) -> list[str]:
    prompts = []
    current_speaker = None
    current_prompt_lines = []

    def flush_prompt():
        if current_speaker in {"user", "developer"} and current_prompt_lines:
            prompt = " ".join(current_prompt_lines).strip()
            if prompt:
                prompts.append(prompt)

    for line in conversation_log.splitlines():
        clean = line.strip()

        if clean.lower() in {"user:", "developer:", "assistant:"}:
            flush_prompt()
            current_speaker = clean[:-1].lower()
            current_prompt_lines = []
            continue

        if clean.lower().startswith("user:"):
            flush_prompt()
            current_speaker = "user"
            current_prompt_lines = [clean[5:].strip()]
            continue

        if clean.lower().startswith("developer:"):
            flush_prompt()
            current_speaker = "developer"
            current_prompt_lines = [clean[10:].strip()]
            continue

        if clean.lower().startswith("assistant:"):
            flush_prompt()
            current_speaker = "assistant"
            current_prompt_lines = []
            continue

        if clean and current_speaker in {"user", "developer"}:
            current_prompt_lines.append(clean)

    flush_prompt()

    return prompts


def detect_stagnation(task_type: str, timeline: list[str]) -> dict:
    if not timeline:
        return {
            "stagnation_detected": False,
            "reason": "No interaction data found."
        }

    counts = Counter(timeline)
    total = len(timeline)
    dominant_mode, dominant_count = counts.most_common(1)[0]
    dominance_ratio = dominant_count / total

    complex_tasks = {"refactor", "architecture", "bug", "investigation"}

    has_understanding = "understanding" in timeline
    has_verification = "verification" in timeline

    is_complex = task_type.lower() in complex_tasks

    stagnation_detected = (
        is_complex
        and dominant_mode == "generation"
        and dominance_ratio >= 0.6
        and not has_understanding
    )

    missing_modes = []
    if not has_understanding:
        missing_modes.append("understanding")
    if not has_verification:
        missing_modes.append("verification")

    return {
        "stagnation_detected": stagnation_detected,
        "dominant_mode": dominant_mode,
        "dominance_ratio": round(dominance_ratio, 2),
        "missing_modes": missing_modes,
        "reason": (
            "Generation dominated a complex task with limited understanding signals."
            if stagnation_detected
            else "No strong stagnation pattern detected."
        )
    }


def generate_suggestion(stagnation_result: dict) -> dict:
    if not stagnation_result.get("stagnation_detected"):
        return {
            "observation": "The collaboration shows a healthy balance between strategies.\n\n"
            "No dominant collaboration risk detected.",
            "suggestion": "Continue working. Consider verifying before finalizing your changes.",
            "example_prompts": [
                "What edge cases should I check?",
                "Review this solution for risks.",
                "Did I miss anything important?"
            ]
        }

    return {
        "observation": "Generation has dominated this session.\n\n"
        "For architecture and refactoring tasks, extended generation without sufficient understanding may increase the risk of rework.",
        "suggestion": "Consider switching temporarily to Understanding mode before continuing implementation.",
        "example_prompts": [
            "What does this class do?",
            "What depends on this change?",
            "What could break if I modify this?"
        ]
    }


def analyze_session(task: dict, conversation_log: str) -> dict:
    prompts = extract_user_prompts(conversation_log)

    timeline = [classify_prompt(prompt) for prompt in prompts]
    counts = Counter(timeline)

    stagnation = detect_stagnation(task.get("type", ""), timeline)
    suggestion = generate_suggestion(stagnation)

    return {
        "task": task,
        "prompts_analyzed": len(prompts),
        "mode_timeline": timeline,
        "mode_counts": dict(counts),
        "dominant_mode": stagnation.get("dominant_mode", "unknown"),
        "stagnation_detected": stagnation.get("stagnation_detected", False),
        "stagnation_reason": stagnation.get("reason"),
        "missing_modes": stagnation.get("missing_modes", []),
        "observation": suggestion["observation"],
        "suggestion": suggestion["suggestion"],
        "example_prompts": suggestion["example_prompts"],
    }