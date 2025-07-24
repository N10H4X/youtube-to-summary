#!/usr/bin/env python3
"""
Example usage of the YouTube to Summary Pipeline
"""

from youtube_to_summary import YouTubeToSummaryPipeline
import json

def example_usage():
    """Example of how to use the pipeline programmatically"""
    
    # Example YouTube URL (replace with actual URL)
    youtube_url = "https://www.youtube.com/watch?v=xXirbnUB3NU"
    
    # Initialize pipeline with default API key
    #pipeline = YouTubeToSummaryPipeline()
    
    # Or initialize with custom API key:
    pipeline = YouTubeToSummaryPipeline(api_key="YWYwNTc0ZjUtOGE3NS00ZTM1LTk1NWUtMmRhYzVhOWYzZjNk")
    
    print("Processing YouTube video...")
    result = pipeline.process_youtube_url(youtube_url)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    if "content" in result:
        print("\n✓ Success! Summary generated.")
    else:
        print("\n❌ Failed to process video.")

if __name__ == "__main__":
    example_usage()
