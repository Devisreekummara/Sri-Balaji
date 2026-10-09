SRI BALAJI CONSTRUCTIONS - BEGINNER SETUP

1. Install Python 3 if it is not already installed.
2. Extract this ZIP file.
3. Open the extracted SriBalajiConstructions folder in VS Code.
4. Open Terminal > New Terminal.
5. Run these commands:

   python -m venv .venv

   Windows PowerShell:
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe app.py

   If you already have a working virtual environment, you can use:
   python -m pip install -r requirements.txt
   python app.py

6. Open this address in your browser:
   http://127.0.0.1:5000

PUBLIC PAGES
- Home: /
- About: /about
- Services: /services
- Projects: /projects
- Contact: /contact

DEMO ADMIN LOGIN
- URL: http://127.0.0.1:5000/login
- Username: admin
- Password: balaji123

NOTES
- Enquiries and projects are saved in construction.db.
- Sample projects are for demonstration only; replace them with real company details.
- This is a local demo. Before publishing online, change the secret key and demo password,
  add stronger authentication/CSRF protection, and deploy with production settings.
- The demo admin password is written in app.py for easy learning. Do not use it for a live site.
