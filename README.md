# LoopLens

AI collaboration observability for engineering tasks.

LoopLens is a lightweight prototype that analyzes an AI-agent conversation and identifies collaboration patterns that may indicate when an engineering session is becoming repetitive or unbalanced.

## What it does

LoopLens looks at the interaction between an engineer and an AI agent.

It does not analyze proprietary code.
It does not judge developer performance.
It does not replace engineering judgment.

Instead, it detects observable collaboration patterns such as:

- generation-dominated sessions
- understanding-oriented sessions
- planning signals
- verification signals
- balanced collaboration patterns

Based on those patterns, LoopLens provides a simple insight and suggests a possible next collaboration strategy.

## Why it matters

AI can help engineers move faster, but speed alone does not guarantee better decisions.

Sometimes an engineer may keep asking an AI agent to generate, fix, and regenerate code without pausing to understand the system, validate assumptions, or review risks.

LoopLens helps make that collaboration pattern visible.

## MVP scope

This Round 1 prototype includes:

- a Streamlit UI
- conversation input
- task context input
- lightweight strategy classification
- collaboration pattern detection
- AI insight generation
- suggested next strategy
- suggested questions

## Responsible AI

LoopLens is designed to support engineers, not evaluate them.

It does not measure productivity.
It does not score people.
It does not determine whether a technical decision is correct.

The goal is to increase awareness and help humans collaborate with AI more intentionally.

## Setup

### Create a virtual environment

```bash
python3 -m venv .venv