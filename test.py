import requests

def test_translation():
    # Sample SRT content
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:04,500 --> 00:00:06,000
How are you today?

3
00:00:06,500 --> 00:00:09,000
This is a test subtitle file.
With multiple lines.
"""

    # API endpoint
    url = "http://localhost:8000/translate"
    
    # Request payload
    payload = {
        "srt_content": srt_content,
        "target_language": "es"  # Spanish
    }

    try:
        # Send POST request
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Print translated content
        print("Original Content:")
        print("-" * 40)
        print(srt_content)
        print("\nTranslated Content:")
        print("-" * 40)
        print(response.json()["translated_content"])
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_translation()
