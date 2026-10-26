# Manual smoke-test checklist

- [ ] `pip install -r requirements.txt` succeeds in a clean virtual environment.
- [ ] `streamlit run app.py` opens the UI.
- [ ] Sidebar **Check local AI** reports a missing service/model clearly when Ollama is unavailable.
- [ ] With Ollama running and the chosen model installed, model check lists installed models.
- [ ] The sample TinyTasks README produces a Markdown response.
- [ ] Download guide saves a `.md` file.
- [ ] Stopping Ollama shows a connection error and does not crash the app.
- [ ] README installation commands match the actual app.
