# LegalMind

A beginner-friendly, India-focused legal information prototype for a hackathon demo.

## Current features

- Looks up Part III of the Constitution of India, Articles 12–28, by Article number or matching words.
- Shows short, fixed demo summaries for Articles 14, 19, and 21.
- Scans fictional sample text for date-like text, time periods, common obligation words, and a few common topics.
- Uses no external AI service. Topic search uses exact word matching; it does not understand meaning or interpret law.

## Legal source and limitations

The included source set is Part III, Articles 12–28, from the Government of India's Constitution text dated 11 November 2025. Article 19 is the first longer provision selected for question-answering practice. See [`sources/README.md`](sources/README.md) for the official source link and scope.

This educational prototype is not legal advice and does not replace a qualified Indian lawyer. Verify the current law against authoritative sources. The included source predates this demo's preparation date and may need updating before public use. The scanner only matches simple text patterns and may miss relevant material or show irrelevant matches.

Use fictional or public sample material only. In a hosted demo, text entered into the app is sent to the hosting provider to run it. Do not enter private, identifying, client, or confidential information.

## Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `streamlit run app.py`.

No API key is needed.

## Deploy a demo

This Streamlit app can be deployed from its GitHub repository using [Streamlit Community Cloud](https://share.streamlit.io/).

1. Publish the repository to GitHub.
2. In Streamlit Community Cloud, create an app using the repository, the `main` branch, and `app.py` as the app file.
3. Use Python 3.12, the Community Cloud default, unless the deployment settings indicate otherwise.
4. Choose app visibility to match the hackathon's requirements. Copy the resulting `streamlit.app` URL into the submission form.

The app currently needs no secrets. Never commit API keys or private documents. The local `.env` and Streamlit secrets file are ignored by Git.

## Submission status

- Demo link: not deployed yet.
- GitHub repository: not published yet.
