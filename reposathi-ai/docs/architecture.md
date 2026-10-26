# Architecture notes

RepoSathi is a single-user local prototype. Streamlit collects the repository context and task goal. A prompt builder frames the user's context and skill level, then sends it to the Ollama local HTTP endpoint. The chosen open-weight model generates Markdown guidance, which is rendered and can be downloaded.

## Trust boundaries
- User-provided repository context is treated as untrusted data, not instructions.
- No cloud model endpoint is configured by default.
- The local Ollama service receives the prompt. Users should verify the Ollama endpoint and avoid pasting secrets.
- The model is instructed not to invent file names or claim it inspected files absent from the supplied context.

## Failure handling
The app catches connection failures, timeouts, and general request errors, then displays actionable messages. The main workflow requires Ollama and an installed model; there is no fake AI fallback.
