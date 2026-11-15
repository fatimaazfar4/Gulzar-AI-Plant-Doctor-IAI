# Gulzar-AI Plant Doctor

A Streamlit plant-care diagnosis app for Pakistani home gardens.

## Contributors

- [Fatima Azfar](https://github.com/fatimaazfar4)

## Run locally

1. Install Python 3.10 or later.
2. From this folder, install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

## Deploy with Streamlit Community Cloud

1. Push this project to a GitHub repository. Include `app.py`, `engine.py`,
   `knowledge_base.py`, `treatments.py`, and `requirements.txt`.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with
   GitHub and grant access to the repository.
3. Choose **Create app**, select the repository and branch, and set the main
   file path to `app.py`.
4. Choose **Deploy**. Community Cloud will install the packages from
   `requirements.txt` and start the app.

This project does not currently require API keys or Streamlit secrets. Do not
commit passwords, tokens, or other credentials to the repository.
