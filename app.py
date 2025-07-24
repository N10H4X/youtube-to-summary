#!/usr/bin/env python3
"""
Flask REST API for YouTube to Summary Pipeline
Provides a web API interface to convert YouTube videos to summary reports
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime
import traceback
from youtube_to_summary import YouTubeToSummaryPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "YouTube to Summary API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/summarize', methods=['POST'])
def summarize_youtube():
    """
    Main endpoint to process YouTube video and generate summary
    
    Expected JSON payload:
    {
        "youtube_url": "https://www.youtube.com/watch?v=...",
        "api_key": "optional_custom_api_key"
    }
    
    Returns:
    {
        "success": true/false,
        "data": {
            "content": "summary report content"
        },
        "error": "error message if failed",
        "processing_time": "time taken in seconds",
        "timestamp": "ISO timestamp"
    }
    """
    start_time = datetime.now()
    
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if not data or 'youtube_url' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field 'youtube_url'",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        youtube_url = data['youtube_url'].strip()
        
        # Basic URL validation
        if not youtube_url:
            return jsonify({
                "success": False,
                "error": "YouTube URL cannot be empty",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
            return jsonify({
                "success": False,
                "error": "Invalid YouTube URL. Must be a valid YouTube link.",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Get API key (optional, will use default if not provided)
        api_key = data.get('api_key', "YWYwNTc0ZjUtOGE3NS00ZTM1LTk1NWUtMmRhYzVhOWYzZjNk")
        
        logger.info(f"Processing YouTube URL: {youtube_url}")
        
        # Initialize and run pipeline
        pipeline = YouTubeToSummaryPipeline(api_key=api_key)
        result = pipeline.process_youtube_url(youtube_url)
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Check if pipeline was successful
        if 'error' in result:
            logger.error(f"Pipeline failed: {result['error']}")
            return jsonify({
                "success": False,
                "error": result['error'],
                "processing_time": processing_time,
                "timestamp": end_time.isoformat()
            }), 500
        
        # Success response
        logger.info(f"Successfully processed YouTube video in {processing_time:.2f} seconds")
        return jsonify({
            "success": True,
            "data": result,
            "processing_time": processing_time,
            "timestamp": end_time.isoformat()
        })
    
    except Exception as e:
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        error_message = str(e)
        
        logger.error(f"Unexpected error: {error_message}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return jsonify({
            "success": False,
            "error": f"Internal server error: {error_message}",
            "processing_time": processing_time,
            "timestamp": end_time.isoformat()
        }), 500

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    """Get API status and information"""
    return jsonify({
        "service": "YouTube to Summary API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "GET /": "Health check",
            "POST /api/v1/summarize": "Process YouTube video and generate summary",
            "GET /api/v1/status": "Get API status"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "success": False,
        "error": "Method not allowed",
        "timestamp": datetime.now().isoformat()
    }), 405

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle 413 errors"""
    return jsonify({
        "success": False,
        "error": "Request entity too large",
        "timestamp": datetime.now().isoformat()
    }), 413

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting YouTube to Summary API Server")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print("=" * 60)
    print("Available endpoints:")
    print("GET  /                    - Health check")
    print("POST /api/v1/summarize   - Process YouTube video")
    print("GET  /api/v1/status      - API status")
    print("=" * 60)
    
    app.run(host=host, port=port, debug=debug)
