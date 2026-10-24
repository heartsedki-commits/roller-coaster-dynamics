# Deploying the Roller Coaster Dynamics Lab

## Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload the contents of this folder to the repository.
3. Open Streamlit Community Cloud and connect the GitHub repository.
4. Select `app.py` as the main file.
5. Deploy.

The app is already configured with `requirements.txt` and `.streamlit/config.toml`.

## Local test
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Important
This is an educational physics simulator. It is not a certified amusement-ride engineering or safety tool.
