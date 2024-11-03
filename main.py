from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import re
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Subtitle Translator API",
    description="API for translating SRT subtitle files while preserving formatting",
    version="1.0.0"
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TranslationRequest(BaseModel):
    srt_content: str
    target_language: str  # Two-letter language code

class TranslationResponse(BaseModel):
    translated_content: str

def parse_srt_chunks(srt_content: str, chunk_size: int = 5) -> List[str]:
    """
    Split SRT content into chunks of subtitles while preserving format.
    Each chunk contains chunk_size subtitle entries.
    """
    # Split content into individual subtitle entries
    entries = re.split(r'\n\n+', srt_content.strip())
    
    # Group entries into chunks
    chunks = []
    for i in range(0, len(entries), chunk_size):
        chunk = entries[i:i + chunk_size]
        chunks.append('\n\n'.join(chunk))
    
    return chunks

def translate_chunk(chunk: str, target_language: str) -> str:
    """
    Translate a chunk of SRT content using OpenAI's GPT-4 model.
    """
    system_prompt = f"""You are a professional subtitle translator. 
    Your task is to translate the provided SRT subtitle chunk to {target_language} while:
    1. Preserving all timestamp formats exactly
    2. Preserving all subtitle numbers exactly
    3. Maintaining the same line breaks
    4. Only translate the actual subtitle text
    Return only the translated SRT content without any explanations."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation service error")

@app.post("/translate", response_model=TranslationResponse)
async def translate_srt(request: TranslationRequest):
    """
    Translate SRT content to the specified target language while preserving format.
    
    Parameters:
    - srt_content: String containing the SRT file content
    - target_language: Two-letter language code (e.g., 'es' for Spanish)
    
    Returns:
    - translated_content: Translated SRT content maintaining original format
    """
    try:
        # Validate target language (basic check)
        if not re.match(r'^[a-z]{2}$', request.target_language.lower()):
            raise HTTPException(
                status_code=400, 
                detail="Invalid target language code. Please use two-letter language codes (e.g., 'es' for Spanish)"
            )

        # Split content into manageable chunks
        chunks = parse_srt_chunks(request.srt_content)
        
        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            translated_chunk = translate_chunk(chunk, request.target_language)
            translated_chunks.append(translated_chunk)
        
        # Combine translated chunks
        final_translation = '\n\n'.join(translated_chunks)
        
        return TranslationResponse(translated_content=final_translation)
    
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
