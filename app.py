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

    st.header("Analysis Result")

    st.metric("Dominant mode", result["dominant_mode"].title())

    st.subheader("Mode timeline")
    st.write(" → ".join(mode.title() for mode in result["mode_timeline"]))

    st.subheader("Mode counts")
    st.json(result["mode_counts"])

    st.subheader("Observation")
    st.info(result["observation"])

    if result["stagnation_detected"]:
        st.warning("Possible collaboration stagnation detected.")
    else:
        st.success("No strong stagnation pattern detected.")

    st.subheader("Suggested strategy shift")
    st.write(result["suggestion"])

    st.subheader("Try asking")
    for prompt in result["example_prompts"]:
        st.markdown(f"- {prompt}")