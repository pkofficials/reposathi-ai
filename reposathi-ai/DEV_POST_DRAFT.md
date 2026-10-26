# RepoSathi AI: helping first-time contributors find a safe first step

Starting in open source can feel harder than writing the code itself. A newcomer opens a repository, sees unfamiliar folders and setup instructions, and may not know which contribution is small enough to attempt.

I built **RepoSathi AI**, a local-first onboarding assistant. A contributor pastes a repository README or short project overview, selects a goal and their experience level, and gets a grounded explanation, a suggested first task, concrete next steps, risks to check, and questions to ask the maintainer.

## Why open-source AI?
RepoSathi uses an open-weight model served locally by Ollama instead of requiring a paid hosted AI API. This keeps inference costs at zero after the model is downloaded and allows pasted repository context to remain on the user's machine. The selected model's own license and hardware needs still apply.

## How it works
1. Streamlit collects a README/context and contributor level.
2. A prompt asks the model to stay grounded in supplied context and label missing information.
3. Ollama runs the chosen open-weight model locally.
4. The app renders a Markdown guide that can be downloaded.

## Demo
[Add your tested demo video or screenshots here.]

## Try it
[Add your public GitHub repository URL here.]

## Limitations and next steps
The prototype only analyzes text pasted into the app; it does not yet crawl the full repository. Model suggestions can be wrong, so users should verify tasks against actual files and contribution guidelines. Next, I want to add safe GitHub repository import, tests for prompt construction, and evaluation on a small set of repositories.

This is a new prototype built for the Hacktoberfest Week 4 challenge. I used AI tools as development assistance, but the project’s core analysis depends on an open-weight model running locally.

#hacktoberfest #hf26challenge #opensource #ai
