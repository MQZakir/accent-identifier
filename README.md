# English Accent Identifier

This tool analyzes a public video URL (YouTube, Loom, direct MP4, etc.), extracts the audio, and classifies the speaker's English accent (e.g., British, American, Australian, etc.) with a confidence score.

## Features
- Paste a video URL and get instant accent analysis
- Supports major English accents
- Simple, user-friendly Streamlit interface

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   (Requires Python 3.11 to run and download all dependencies or else sentencepiece will not be downloaded which is crucial)
   You also need `ffmpeg` and `yt-dlp` installed on your system:
   - [FFmpeg install guide](https://ffmpeg.org/download.html)
   - [yt-dlp install guide](https://github.com/yt-dlp/yt-dlp#installation)

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the Streamlit app in your browser.
2. Paste a public video URL (YouTube, Loom, or direct MP4 link).
3. Click **Analyze**.
4. View the detected accent, confidence score, and a short explanation.

## Notes
- Only English accents are supported.
- For best results, use clear audio with a single speaker.
- No fine-tuning required; uses a pre-trained HuggingFace model.
- **Multiple Accents:** If there are multiple accents in the video, the model will identify the most prominent (most heard) accent within the analyzed audio segment (default: 1 minute, or more if specified in the code).
- **More Audio = Better Results:** The more audio the model receives (by increasing the extraction duration), the better and more reliable the accent classification will be, but the processing time will be even longer.

## Model Information

- **Accent Classifier Model:** This app uses the [bookbot/english-accent-classifier](https://huggingface.co/bookbot/english-accent-classifier) model from Hugging Face for English accent identification. You can view the model details, supported accents, and documentation at the link above.

## Testing

- The app was tested using YouTube news reports and public videos representing different English accents. This approach helps validate the model's predictions and demonstrates its real-world performance across a variety of authentic speech samples.

## License
MIT 

## Deployment on Streamlit Cloud

1. **Fork or clone this repository.**
2. **Ensure the following files are present in your repo root:**
   - `app.py` (main app)
   - `requirements.txt` (Python dependencies)
   - `packages.txt` (system packages, e.g., ffmpeg)
   - `custom_interface.py` (needed for the model)
3. **Deploy to [Streamlit Cloud](https://streamlit.io/cloud):**
   - Click "New app" and select your repo and `app.py` as the main file.
   - Streamlit Cloud will automatically install all dependencies.
4. **First run:**
   - The app will download the model and cache it. This may take a few minutes.
   - After that, all users will benefit from the cached model and fast startup.
5. **No need to install ffmpeg or yt-dlp manually**—these are handled by the deployment files.

**Note:**
- The first run may take longer due to model download.
- If you change the model or restart the app, it may re-download.

### Directory Structure Example

```
/your-repo
  |-- app.py
  |-- requirements.txt
  |-- packages.txt
  |-- README.md
  |-- custom_interface.py
```

--- 
