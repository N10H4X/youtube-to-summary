#!/usr/bin/env python3
"""
YouTube to Summary Pipeline
Complete workflow: YouTube URL -> Video Download -> Audio Conversion -> Speech-to-Text -> Summary -> Report
"""

import os
import sys
import json
import glob
import shutil
import requests
import yt_dlp
import moviepy.editor as mp
from typing import Dict, Optional

class YouTubeToSummaryPipeline:
    """Main pipeline class that handles the entire workflow"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the pipeline with API configuration
        
        Args:
            api_key (str): API key for the Rev21Labs AI services
        """
        self.api_key = api_key or os.getenv('API_KEY', "YWYwNTc0ZjUtOGE3NS00ZTM1LTk1NWUtMmRhYzVhOWYzZjNk")
        # Use /tmp directory for Vercel serverless functions
        self.temp_dir = "/tmp/temp_outputs" if os.path.exists("/tmp") else "temp_outputs"
        self.video_filename = "video.mp4"
        self.audio_filename = "audio.mp3"
        
        # API endpoints
        self.speech_to_text_url = "https://ai-tools.rev21labs.com/api/v1/speech/speech-to-text"
        self.summarize_url = "https://ai-tools.rev21labs.com/api/v1/ai/summarize"
        self.text_generation_url = "https://ai-tools.rev21labs.com/api/v1/ai/text-generation"
        
        # Create temp directory
        self._setup_temp_directory()
    
    def _setup_temp_directory(self):
        """Create and clean the temporary directory"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir, exist_ok=True)
        print(f"✓ Created temporary directory: {self.temp_dir}")
    
    def download_youtube_video(self, url: str) -> bool:
        """
        Download YouTube video at minimum quality
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            bool: Success status
        """
        print(f"📥 Starting YouTube video download from: {url}")
        
        # Configure yt-dlp options for minimum quality
        video_path = os.path.join(self.temp_dir, self.video_filename)
        ydl_opts = {
            'format': 'worst[ext=mp4]/worst',
            'outtmpl': video_path,
            'noplaylist': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                
                print(f"  Title: {video_title}")
                print(f"  Duration: {duration // 60}:{duration % 60:02d}")
                
                # Download the video
                ydl.download([url])
                print(f"✓ Video downloaded successfully: {self.video_filename}")
                return True
                
        except Exception as e:
            print(f"❌ Video download failed: {e}")
            return False
    
    def convert_video_to_audio(self) -> bool:
        """
        Convert downloaded video to MP3 audio
        
        Returns:
            bool: Success status
        """
        print("🎵 Converting video to audio...")
        
        video_path = os.path.join(self.temp_dir, self.video_filename)
        audio_path = os.path.join(self.temp_dir, self.audio_filename)
        
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return False
        
        try:
            # Load video and extract audio
            clip = mp.VideoFileClip(video_path)
            clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
            clip.close()
            
            print(f"✓ Audio conversion completed: {self.audio_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Audio conversion failed: {e}")
            return False
    
    def speech_to_text(self) -> Optional[str]:
        """
        Convert audio to text using speech-to-text API
        
        Returns:
            Optional[str]: Transcribed text or None if failed
        """
        print("🎤 Converting speech to text...")
        
        audio_path = os.path.join(self.temp_dir, self.audio_filename)
        
        if not os.path.exists(audio_path):
            print(f"❌ Audio file not found: {audio_path}")
            return None
        
        headers = {"x-api-key": self.api_key}
        
        try:
            with open(audio_path, 'rb') as audio_file:
                files = {'file': ('audio.mp3', audio_file, 'audio/mpeg')}
                
                response = requests.post(
                    url=self.speech_to_text_url,
                    headers=headers,
                    files=files,
                    timeout=120  # Extended timeout for speech processing
                )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract text from response (adjust based on actual API response format)
            if 'content' in result:
                transcription = result['content']
            elif 'text' in result:
                transcription = result['text']
            elif 'transcription' in result:
                transcription = result['transcription']
            else:
                # If response format is different, try to get the first string value
                transcription = str(result)
            
            print("✓ Speech-to-text conversion completed")
            return transcription
            
        except Exception as e:
            print(f"❌ Speech-to-text conversion failed: {e}")
            return None
    
    def summarize_text(self, text: str) -> Optional[str]:
        """
        Summarize text using AI summarization API
        
        Args:
            text (str): Text to summarize
            
        Returns:
            Optional[str]: Summary or None if failed
        """
        print("📝 Generating text summary...")
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        
        data = {"content": text}
        
        try:
            response = requests.post(
                url=self.summarize_url,
                headers=headers,
                json=data,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract summary from response
            if 'content' in result:
                summary = result['content']
            elif 'summary' in result:
                summary = result['summary']
            elif 'text' in result:
                summary = result['text']
            else:
                summary = str(result)
            
            print("✓ Text summarization completed")
            return summary
            
        except Exception as e:
            print(f"❌ Text summarization failed: {e}")
            return None
    
    def generate_report(self, summary: str) -> Optional[str]:
        """
        Generate comprehensive bullet-point report from summary
        
        Args:
            summary (str): Summary text to expand
            
        Returns:
            Optional[str]: Generated report or None if failed
        """
        print("📊 Generating comprehensive report...")
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        
        data = {
            "type": "report",  # Changed from "news" to "report" for better output
            "topic": summary
        }
        
        try:
            response = requests.post(
                url=self.text_generation_url,
                headers=headers,
                json=data,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract generated content from response
            if 'content' in result:
                report = result['content']
            elif 'text' in result:
                report = result['text']
            elif 'generated_text' in result:
                report = result['generated_text']
            else:
                report = str(result)
            
            print("✓ Report generation completed")
            return report
            
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            return None
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"✓ Cleaned up temporary directory: {self.temp_dir}")
    
    def process_youtube_url(self, youtube_url: str) -> Dict:
        """
        Complete pipeline: YouTube URL to summary report
        
        Args:
            youtube_url (str): YouTube video URL
            
        Returns:
            Dict: Final result with content or error message
        """
        print("🚀 Starting YouTube to Summary Pipeline")
        print("=" * 60)
        
        try:
            # Step 1: Download YouTube video
            if not self.download_youtube_video(youtube_url):
                return {"error": "Failed to download YouTube video"}
            
            # Step 2: Convert video to audio
            if not self.convert_video_to_audio():
                return {"error": "Failed to convert video to audio"}
            
            # Step 3: Convert speech to text
            transcription = self.speech_to_text()
            if not transcription:
                return {"error": "Failed to convert speech to text"}
            
            # Step 4: Summarize text
            summary = self.summarize_text(transcription)
            if not summary:
                return {"error": "Failed to generate summary"}
            
            # Step 5: Generate comprehensive report
            report = self.generate_report(summary)
            if not report:
                return {"error": "Failed to generate report"}
            
            print("🎉 Pipeline completed successfully!")
            return {"content": report}
            
        except Exception as e:
            return {"error": f"Pipeline failed with unexpected error: {str(e)}"}
        
        finally:
            # Always clean up temporary files
            self.cleanup()


def main():
    """Main function to run the pipeline"""
    print("🎥 YouTube to Summary Pipeline")
    print("=" * 60)
    
    # Get YouTube URL from command line argument or user input
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
    else:
        youtube_url = input("Enter YouTube video URL: ").strip()
    
    if not youtube_url:
        print("❌ No URL provided!")
        return
    
    # Basic URL validation
    if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
        print("❌ Invalid YouTube URL! Please provide a valid YouTube link.")
        return
    
    # Optional: Custom API key
    api_key = input("Enter API key (press Enter to use default): ").strip()
    if not api_key:
        api_key = "YWYwNTc0ZjUtOGE3NS00ZTM1LTk1NWUtMmRhYzVhOWYzZjNk"
    
    # Initialize and run pipeline
    pipeline = YouTubeToSummaryPipeline(api_key=api_key)
    result = pipeline.process_youtube_url(youtube_url)
    
    # Display result
    print("\n" + "=" * 60)
    print("FINAL RESULT:")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    
    # Save result to file
    output_file = "summary_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Result saved to: {output_file}")


if __name__ == "__main__":
    main()
