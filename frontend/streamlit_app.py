import json
import requests
import streamlit as st
import plotly.graph_objects as go

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SmartHire AI",
    page_icon="🧠",
    layout="wide",
)

BACKEND_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# SIDEBAR – UPLOAD RESUME
# --------------------------------------------------
st.sidebar.title("📄 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF resume file",
    type=["pdf"],
    help="Upload a single PDF resume to analyze against the job description.",
)

if uploaded_file is not None:
    with st.spinner("Uploading & processing resume..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            res = requests.post(f"{BACKEND_URL}/analyze_resume", files=files, timeout=120)
            if res.status_code == 200:
                payload = res.json()
                if payload.get("status") == "success":
                    st.sidebar.success(f"✅ Uploaded: {payload.get('file_name', uploaded_file.name)}")
                    st.sidebar.caption(
                        f"Text length: {payload.get('text_length', 'N/A')} chars"
                    )
                else:
                    st.sidebar.error(f"❌ Upload failed: {payload.get('error', 'Unknown error')}")
            else:
                st.sidebar.error(f"❌ Upload failed (HTTP {res.status_code})")
        except Exception as e:
            st.sidebar.error(f"❌ Upload failed: {e}")

# --------------------------------------------------
# MAIN LAYOUT
# --------------------------------------------------
st.title("🧠 SmartHire AI — Intelligent Resume Analyzer (Single Resume Mode)")

st.markdown(
    "Upload a resume on the left, paste a job description below, "
    "and SmartHire AI will analyze **how well this single resume matches the role**, "
    "combining vector similarity, keyword overlap, and LLM reasoning."
)

job_description = st.text_area(
    "Paste the job description below:",
    height=260,
    placeholder=(
        "Example:\n"
        "We are looking for an AI / ML Engineer with strong Python skills, experience with "
        "LangChain or other agent frameworks, and exposure to AWS (Bedrock, Lambda, S3)..."
    ),
)

analyze_button = st.button("🔍 Analyze Match", use_container_width=True)

# --------------------------------------------------
# HELPER – SAFE JSON PARSE
# --------------------------------------------------
def try_parse_json(text: str):
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


# --------------------------------------------------
# ANALYZE BUTTON CLICK
# --------------------------------------------------
if analyze_button:
    if uploaded_file is None:
        st.warning("Please upload a resume first on the left panel.")
    elif not job_description.strip():
        st.warning("Please enter a job description to analyze.")
    else:
        with st.spinner("Analyzing resume vs job description..."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/analyze_match",
                    data={"job_description": job_description},
                    timeout=300,
                )
                data = resp.json()
            except Exception as e:
                st.error(f"❌ Failed to contact backend: {e}")
                data = None

        if not data:
            st.stop()

        if data.get("status") != "success":
            st.error(f"❌ Job match failed: {data.get('error', 'Unknown error')}")
            st.stop()

        # --------------------------------------------------
        # SUCCESS MESSAGE
        # --------------------------------------------------
        elapsed = data.get("elapsed_time_sec")
        if elapsed is not None:
            st.success(f"✅ Analysis complete in {elapsed} seconds!")
        else:
            st.success("✅ Analysis complete!")

        # --------------------------------------------------
        # JOB DESCRIPTION ANALYSIS (LLM OUTPUT)
        # --------------------------------------------------
        st.markdown("### 🧾 Job Description Analysis (LLM Output)")

        raw_job_analysis = data.get("job_analysis", "")
        parsed_job = try_parse_json(raw_job_analysis)

        if parsed_job:
            # Nicely formatted summary
            col_left, col_right = st.columns([1, 1])

            with col_left:
                title = parsed_job.get("JobTitle") or parsed_job.get("Title")
                if title:
                    st.markdown(f"**Job Title:** {title}")

                required = parsed_job.get("RequiredSkills") or parsed_job.get("Required Skills")
                if isinstance(required, list) and required:
                    st.markdown("**Required Skills:**")
                    for skill in required:
                        st.markdown(f"- {skill}")

                preferred = parsed_job.get("PreferredSkills") or parsed_job.get("Preferred Skills")
                if isinstance(preferred, list) and preferred:
                    st.markdown("**Preferred Skills:**")
                    for skill in preferred:
                        st.markdown(f"- {skill}")

            with col_right:
                exp_level = parsed_job.get("ExperienceLevel") or parsed_job.get("Experience Level")
                if exp_level:
                    st.markdown(f"**Experience Level:** {exp_level}")

                tools = (
                    parsed_job.get("Technologies")
                    or parsed_job.get("ToolsOrTechnologies")
                    or parsed_job.get("Tools")
                )
                if isinstance(tools, list) and tools:
                    st.markdown("**Tools / Technologies:**")
                    for t in tools:
                        st.markdown(f"- {t}")

                summary = parsed_job.get("ShortSummary") or parsed_job.get("Summary")
                if summary:
                    st.markdown("**Summary:**")
                    st.write(summary)

            # Raw JSON for debugging
            with st.expander("🔍 View raw LLM JSON output for job description"):
                st.json(parsed_job)
        else:
            # Not JSON – just show text
            st.write(raw_job_analysis or "_No job analysis returned._")

        st.markdown("---")

        # --------------------------------------------------
        # MATCH RESULTS (SINGLE RESUME)
        # --------------------------------------------------
        st.markdown("### 📊 Overall Match Results")

        matches_container = data.get("match_results", {})
        matches = matches_container.get("matches", []) if isinstance(matches_container, dict) else []

        if not matches:
            st.warning("No match results returned from the backend.")
        else:
            # In single-resume mode, we just use the first / only match
            match = matches[0]

            faiss_sim = float(match.get("faiss_similarity", 0.0))
            keyword_overlap = float(match.get("keyword_overlap", 0.0))
            llm_score = float(match.get("llm_score", 0.0))
            final_score = float(match.get("final_match_percentage", 0.0))

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Vector Similarity", f"{faiss_sim:.2f}%")
            col2.metric("Keyword Overlap", f"{keyword_overlap:.2f}%")
            col3.metric("LLM Match Score", f"{llm_score:.2f}%")
            col4.metric("Final Match", f"{final_score:.2f}%")

            # Bar chart for score comparison
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=["Vector Similarity", "Keyword Overlap", "LLM Score"],
                    y=[faiss_sim, keyword_overlap, llm_score],
                    text=[f"{faiss_sim:.1f}%", f"{keyword_overlap:.1f}%", f"{llm_score:.1f}%"],
                    textposition="auto",
                    marker_color=["#636EFA", "#00CC96", "#AB63FA"],
                )
            )
            fig.update_layout(
                title="Score Contribution Comparison",
                yaxis=dict(title="Percentage (%)", range=[0, 100]),
                xaxis=dict(title="Components"),
                height=380,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

            # --------------------------------------------------
            # AI REASONING BREAKDOWN
            # --------------------------------------------------
            st.markdown("### 🤖 AI Reasoning Breakdown")

            # ai_reasoning might already be a dict, or a JSON string
            reasoning_raw = match.get("ai_reasoning", {})
            if isinstance(reasoning_raw, str):
                parsed_reasoning = try_parse_json(reasoning_raw) or {}
            elif isinstance(reasoning_raw, dict):
                parsed_reasoning = reasoning_raw
            else:
                parsed_reasoning = {}

            match_summary = parsed_reasoning.get("MatchSummary") or parsed_reasoning.get(
                "Summary", ""
            )
            if match_summary:
                st.markdown(f"**Match Summary:** {match_summary}")

            tech_skills = parsed_reasoning.get("TechnicalSkills", [])
            soft_skills = parsed_reasoning.get("SoftSkills", [])
            missing_skills = parsed_reasoning.get("MissingSkills", [])
            experience_alignment = parsed_reasoning.get("ExperienceAlignment", "")

            colA, colB = st.columns(2)

            with colA:
                st.markdown("#### ⚙️ Technical Skills Match")
                if tech_skills:
                    st.write(", ".join(tech_skills))
                else:
                    st.write("_No technical skills identified._")

                st.markdown("#### 💬 Soft Skills")
                if soft_skills:
                    st.write(", ".join(soft_skills))
                else:
                    st.write("_No soft skills explicitly identified._")

            with colB:
                st.markdown("#### 🚫 Missing Skills / Gaps")
                if missing_skills:
                    st.error(", ".join(missing_skills))
                else:
                    st.success("No major skill gaps detected by the model.")

                st.markdown("#### 📈 Experience Alignment")
                if experience_alignment:
                    st.write(experience_alignment)
                else:
                    st.write("_Experience alignment not specifically mentioned._")

            # Optional raw reasoning JSON for debugging
            if parsed_reasoning:
                with st.expander("🔍 View raw AI reasoning JSON"):
                    st.json(parsed_reasoning)

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------
        st.markdown("---")
        st.caption(
            "🚀 SmartHire AI v3.5 | Single-Resume Matching • FAISS + Keyword + GPT Reasoning | by G D Hruthik"
        )
