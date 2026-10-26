import json
import os
import requests
import streamlit as st

APP_NAME = "RepoSathi AI"
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

st.set_page_config(page_title=APP_NAME, page_icon="🧭", layout="wide")
st.markdown("""
<style>
:root { color-scheme: dark; }
.block-container {max-width: 1100px; padding-top: 2rem;}
.hero {padding: 1.5rem; border-radius: 18px; background: linear-gradient(125deg,#111827,#312e81); border:1px solid #4f46e5;}
.hero h1 {margin:0; font-size:2.5rem;}
.hero p {color:#dbeafe; font-size:1.05rem;}
.small-note {color:#94a3b8; font-size:.9rem;}
</style>
<div class="hero"><h1>🧭 RepoSathi AI</h1><p>Your local-first guide to understanding an open-source repository and finding a safe first contribution.</p></div>
""", unsafe_allow_html=True)
st.write("")

with st.sidebar:
    st.header("⚙️ Local AI settings")
    model = st.text_input("Ollama model", value=DEFAULT_MODEL, help="Example: qwen2.5:3b or llama3.2:3b")
    st.caption("No paid API credits. Inference runs through your local Ollama installation.")
    if st.button("Check local AI"):
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
            r.raise_for_status()
            names = [m.get("name", "") for m in r.json().get("models", [])]
            if names:
                st.success("Ollama is reachable")
                st.write("Installed models:")
                st.code("\n".join(names))
            else:
                st.warning("Ollama is running, but no models are installed yet.")
        except Exception:
            st.error("Cannot reach Ollama at localhost:11434. Install/start Ollama and pull a model first.")

st.subheader("1 · Add repository context")
st.write("Paste a repository README or a short project overview. This prototype does not upload it anywhere.")
example = """# TinyTasks\nTinyTasks is a small Python command-line task manager.\n\n## Setup\nInstall Python 3.10+. Run `python app.py`.\n\n## Structure\n- task.py: task model\n- storage.py: JSON file storage\n- cli.py: command-line interface\n\n## Tests\nRun `python -m unittest`.\n\n## Known gaps\n- No tests for invalid dates\n- Error messages are inconsistent\n- Documentation lacks examples\n"""
repo_text = st.text_area("README / project context", value=example, height=230, placeholder="Paste README content here…")
col1, col2 = st.columns([1, 1])
with col1:
    focus = st.selectbox("What do you need?", ["Find a beginner-friendly first contribution", "Explain this repository", "Create a learning path for this codebase", "Review setup and testing gaps"])
with col2:
    level = st.selectbox("Your coding level", ["Beginner", "Some basics", "Intermediate"])

SYSTEM_PROMPT = """You are RepoSathi, a careful open-source project onboarding assistant. Use only the repository context supplied by the user. Never invent file names or claim you inspected files not included. If information is missing, state what to inspect next. Give beginner-friendly, concrete advice. Return Markdown with these sections: Quick understanding; Suggested first task; Why it matters; Exact next steps; Risk/checks; Questions to ask the maintainer. Prefer small, testable, respectful contributions. Do not suggest claiming work or opening spam PRs."""

if st.button("🧠 Analyze with local open model", type="primary", use_container_width=True):
    if len(repo_text.strip()) < 40:
        st.warning("Paste a little more repository context first.")
    else:
        prompt = f"Goal: {focus}\nContributor level: {level}\n\nRepository context (may be incomplete):\n{repo_text[:14000]}\n\nCreate a grounded, practical analysis. Clearly label assumptions and do not invent repository details."
        with st.spinner(f"Asking local model {model}…"):
            try:
                response = requests.post(
                    f"{OLLAMA_URL}/api/chat",
                    json={"model": model, "stream": False, "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ], "options": {"temperature": 0.2}},
                    timeout=180,
                )
                response.raise_for_status()
                answer = response.json().get("message", {}).get("content", "").strip()
                if not answer:
                    st.error("The model returned an empty response. Try again or choose another installed model.")
                else:
                    st.session_state["answer"] = answer
                    st.session_state["used_model"] = model
            except requests.exceptions.ConnectionError:
                st.error("Ollama is not running. Start Ollama, install a model, then try again. No cloud API or paid credits are used.")
            except requests.exceptions.Timeout:
                st.error("The local model took too long. Try a smaller model such as qwen2.5:3b or llama3.2:3b.")
            except Exception as e:
                st.error(f"Request failed: {e}. Check that the model name matches an installed Ollama model.")

if st.session_state.get("answer"):
    st.divider()
    st.subheader("2 · Your repository guide")
    st.caption(f"Generated locally with: {st.session_state.get('used_model', model)}")
    st.markdown(st.session_state["answer"])
    st.download_button("Download guide as Markdown", st.session_state["answer"], file_name="reposathi-guide.md", mime="text/markdown")

st.divider()
st.markdown("**Privacy by design:** repository text is sent only to the Ollama service configured on this machine. This app has no account system, analytics, or hosted AI API.")
st.markdown('<p class="small-note">Prototype limitation: analysis is only as accurate as the README/context pasted in. Always verify suggestions against the actual repository and its contribution guide.</p>', unsafe_allow_html=True)
