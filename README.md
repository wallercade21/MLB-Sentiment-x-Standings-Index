# Starscape Dashboard

A simple Flask webapp that queries the Starscape API and displays:
- Sentiment over time (line chart)
- Top topics (bar list)
- Total post count

## Setup

1. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

2. **Add your API token**
   Open `.env` and replace `your_token_here` with your actual Starscape token:
   ```
   STARSCAPE_TOKEN=your_token_here
   ```

3. **Run the app**
   ```
   python app.py
   ```

4. **Open in browser**
   Go to: http://127.0.0.1:5000

## Project Structure

```
starscape-dashboard/
├── app.py              # Flask backend + Starscape API calls
├── requirements.txt    # Python dependencies
├── .env                # Your API token (never commit this!)
└── templates/
    └── index.html      # Frontend UI with Chart.js
```
