# Subtitle Translator API

A FastAPI-based service that translates SRT subtitle files while preserving their original formatting. The API uses OpenAI's GPT-4 model for high-quality translations.

## Features

- Translates SRT files while maintaining timestamp formats and subtitle numbering
- Supports all language pairs through two-letter language codes
- Automatic chunking of large subtitle files for optimal processing
- Swagger documentation included
- Error handling and logging

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the API

Start the API server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Access the Swagger documentation at `http://localhost:8000/docs`

### Endpoints

#### POST /translate

Translates SRT content to the specified target language.

Request body:

```json
{
  "srt_content": "Your SRT content here",
  "target_language": "es" // Two-letter language code
}
```

Response:

```json
{
  "translated_content": "Translated SRT content"
}
```

## Example Usage

```python
import requests

api_url = "http://localhost:8000/translate"
srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:04,500 --> 00:00:06,000
How are you today?"""

response = requests.post(api_url, json={
    "srt_content": srt_content,
    "target_language": "es"
})

print(response.json()["translated_content"])
```

## Language Codes

Use standard two-letter language codes (ISO 639-1), for example:

- 'en' for English
- 'es' for Spanish
- 'fr' for French
- 'de' for German
- 'it' for Italian
- 'ja' for Japanese
- 'ko' for Korean
- 'zh' for Chinese
