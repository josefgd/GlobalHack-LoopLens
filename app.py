import streamlit as st
from looplens.analyzer import analyze_session


st.set_page_config(page_title="LoopLens", page_icon="🔍", layout="centered")

st.title("🔍 LoopLens")
st.subheader("AI collaboration observability for engineering tasks")

st.write(
    "LoopLens analyzes an AI-agent session and detects when the collaboration "
    "may be getting stuck in a single mode."
)

task_title = st.text_input("Task title", value="Refactor payment flow")

task_type = st.selectbox(
    "Task type",
    ["Refactor", "Architecture", "Bug", "Investigation", "Simple Implementation"],
)

task_description = st.text_area(
    "Task description",
    value="Modify an existing service safely without introducing integration issues.",
    height=100,
)

conversation_log = st.text_area(
    "AI conversation log",
    value="""User: Generate the implementation.
Assistant: Sure...
User: Fix this error.
Assistant: Updated...
User: Try another approach.
Assistant: Here is another version...
User: Implement it differently.
Assistant: Done...
User: Fix the compile issue.
Assistant: Fixed...""",
    height=220,
)

if st.button("Analyze Session"):
    task = {
        "title": task_title,
        "type": task_type,
        "description": task_description,
    }

    result = analyze_session(task, conversation_log)

    st.divider()

    st.header("📊 Session Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Dominant Strategy",
            value=result["dominant_mode"].title()
        )

    with col2:
        if result["stagnation_detected"]:
            st.metric(
                label="Collaboration Risk",
                value="⚠ Detected"
            )
        else:
            st.metric(
                label="Collaboration Risk",
                value="✅ Not Detected"
            )

    st.markdown("---")

    from collections import Counter
    st.subheader("Collaboration Pattern")

    mode_counts = Counter(result["mode_timeline"])

    icons = {
        "generation": "🟠",
        "understanding": "🔵",
        "planning": "🟢",
        "verification": "🟣",
        "exploration": "🟡",
        "unknown": "⚪",
    }

    for mode, count in mode_counts.items():
        st.write(f"{icons.get(mode, '⚪')} **{mode.title()} × {count}**")

    st.subheader("AI Insight")

    with st.container(border=True):
        st.markdown(result["observation"])

        st.markdown("---")

        st.markdown("**Recommended Next Strategy**")
        st.write(result["suggestion"])

        st.markdown("---")

        st.markdown("**Suggested Questions**")
        for prompt in result["example_prompts"]:
            st.markdown(f"- {prompt}")