import logging
import os
from datetime import datetime
import sys

def setup_logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Create a custom formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Stream handler with custom encoding handling
    class UnicodeSafeStreamHandler(logging.StreamHandler):
        def emit(self, record):
            try:
                msg = self.format(record)
                # Replace problematic Unicode characters for console
                msg = msg.encode('ascii', errors='replace').decode('ascii')
                stream = self.stream
                stream.write(msg + self.terminator)
                stream.flush()
            except Exception:
                self.handleError(record)

    stream_handler = UnicodeSafeStreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            file_handler,
            stream_handler
        ]
    )
    
    logger = logging.getLogger("SentimentAnalysis")
    return logger