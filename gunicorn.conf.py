# Gunicorn configuration file for YouTube to Summary API
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('WORKERS', '4'))
worker_class = "sync"
worker_connections = 1000
timeout = int(os.getenv('TIMEOUT', '600'))  # 10 minutes for video processing
keepalive = 2
max_requests = int(os.getenv('MAX_REQUESTS', '1000'))
max_requests_jitter = int(os.getenv('MAX_REQUESTS_JITTER', '100'))

# Restart workers after this many requests, with up to max_requests_jitter
# added randomness to prevent all workers from restarting at the same time
preload_app = True

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'youtube-summary-api'

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment and configure for HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
