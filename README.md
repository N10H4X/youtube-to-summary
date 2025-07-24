# YouTube to Summary API

A Flask REST API that converts YouTube videos into comprehensive summary reports. This API wraps the existing YouTube-to-Summary pipeline and provides a web interface for video processing.

## Features

- **YouTube Video Processing**: Download and process YouTube videos
- **Speech-to-Text Conversion**: Extract audio and convert to text
- **AI-Powered Summarization**: Generate intelligent summaries
- **Comprehensive Reports**: Create detailed bullet-point reports
- **REST API Interface**: Easy-to-use HTTP endpoints
- **Error Handling**: Robust error handling and logging
- **CORS Support**: Cross-origin resource sharing enabled

## Original Pipeline Workflow

The underlying pipeline follows these steps:
1. **Download YouTube Video** - Downloads the video at minimum quality and saves as `video.mp4`
2. **Convert to Audio** - Converts the video to MP3 format as `audio.mp3`
3. **Speech-to-Text** - Transcribes the audio using Rev21Labs API
4. **Text Summarization** - Summarizes the transcription to extract main points
5. **Report Generation** - Creates a comprehensive bullet-point report

## API Endpoints

### Health Check
```
GET /
```
Returns basic health status of the API.

### Process YouTube Video
```
POST /api/v1/summarize
```
**Request Body:**
```json
{
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "api_key": "optional_custom_api_key"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "content": "Comprehensive summary report..."
    },
    "processing_time": 45.67,
    "timestamp": "2025-07-25T10:30:00"
}
```

### API Status
```
GET /api/v1/status
```
Returns API status and available endpoints.

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. API Key Requirements

The API uses Rev21Labs AI Tools APIs which require an API key:

- **Speech-to-Text API**: `https://ai-tools.rev21labs.com/api/v1/speech/speech-to-text`
- **Summarization API**: `https://ai-tools.rev21labs.com/api/v1/ai/summarize`
- **Text Generation API**: `https://ai-tools.rev21labs.com/api/v1/ai/text-generation`

#### Getting an API Key:

1. Visit [Rev21Labs](https://ai-tools.rev21labs.com/) or the appropriate registration page
2. Sign up for an account
3. Navigate to API section or dashboard
4. Generate an API key
5. Copy the API key for use in requests

**Note**: The project includes a default API key, but you should obtain your own for production use.

### 3. Additional System Requirements

- **FFmpeg**: Required by moviepy for video processing
  - Windows: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

## Local Development

### 1. Start the API Server
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

### 2. Test the API
```bash
# Run basic tests
python test_api.py

# Interactive testing
python test_api.py interactive
```

### 3. Manual Testing with curl
```bash
# Health check
curl http://localhost:5000/

# Process a YouTube video
curl -X POST http://localhost:5000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
  }'
```

## Production Deployment

### Local Production Server
```bash
# Install and run with gunicorn
pip install gunicorn
gunicorn -c gunicorn.conf.py app:app
```

### Cloud Hosting Options

#### 1. Heroku
```bash
# Create Procfile with: web: gunicorn -c gunicorn.conf.py app:app
heroku create your-app-name
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add heroku/python
git push heroku main
```

#### 2. Railway
1. Visit [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy automatically

#### 3. Render
1. Visit [Render.com](https://render.com)
2. Create new Web Service
3. Set start command: `gunicorn -c gunicorn.conf.py app:app`

## Original Command Line Usage (Still Available)

The original `youtube_to_summary.py` script can still be used directly:

```bash
# With command line argument
python youtube_to_summary.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Interactive mode
python youtube_to_summary.py
```

## File Structure

```
YT2Summary - trueflask/
├── app.py                 # Flask API application
├── youtube_to_summary.py  # Original pipeline (unchanged)
├── test_api.py           # API testing client
├── requirements.txt      # Python dependencies
├── gunicorn.conf.py     # Production server config
├── .env.example         # Environment variables template
├── example_usage.py      # Original example usage
└── README.md            # This file
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in PATH
   - Test with: `ffmpeg -version`

2. **API key errors**
   - Get your own API key from Rev21Labs
   - Check if the default API key has usage limits

3. **Video download fails**
   - Some videos may be restricted or private
   - Try with a different YouTube video

4. **Timeout errors**
   - Video processing can take time
   - Consider using shorter videos for testing

## Contributing

1. Keep the original `youtube_to_summary.py` unchanged
2. Add new features to `app.py` or separate modules
3. Test thoroughly before deployment

## License

This project is provided as-is for educational and development purposes.

```bash
python youtube_to_summary.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Interactive Usage

```bash
python youtube_to_summary.py
```

Then enter the YouTube URL when prompted.

### Custom API Key

You can provide your own API key when prompted, or modify the default in the script.

## Output

The script outputs a JSON object with the final result:

```json
{
  "content": "• Main point 1\n• Main point 2\n• Key insight 3\n..."
}
```

Results are also saved to `summary_result.json` in the same directory.

## Error Handling

If any step fails, the script will return an error message:

```json
{
  "error": "Description of what went wrong"
}
```

## Temporary Files

The script creates a `temp_outputs` directory for intermediate files:
- `video.mp4` - Downloaded video
- `audio.mp3` - Converted audio

These files are automatically cleaned up after processing.

## Troubleshooting

### Common Issues:

1. **"No module named 'yt_dlp'"**: Install dependencies with `pip install -r requirements.txt`

2. **FFmpeg not found**: Install FFmpeg on your system (see setup instructions above)

3. **API key invalid**: Obtain a valid API key from Rev21Labs

4. **Network timeout**: Check internet connection and API service status

5. **Video download fails**: Ensure the YouTube URL is valid and accessible

### API Registration Requirements:

- Valid email address for account creation
- Possible verification process
- May require credit card for premium features
- Check Rev21Labs terms of service for usage limits

## File Structure

```
├── youtube_to_summary.py    # Main pipeline script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── temp_outputs/           # Temporary files (auto-created/cleaned)
└── summary_result.json     # Output result file
```

## License

This project is for educational and research purposes. Please respect YouTube's Terms of Service and API usage guidelines.
