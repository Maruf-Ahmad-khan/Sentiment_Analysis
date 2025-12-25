import sys
import os
import io
# Add the project root (Amazon directory) to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.pipelines.training_pipeline import TrainingPipeline
from src.logger import setup_logger

logger = setup_logger()

if __name__ == "__main__":
    try:
        logger.info("Starting main execution")
        pipeline = TrainingPipeline()
        model, history = pipeline.run_pipeline()
        logger.info("Main execution completed")
        
        # Optional: Print training summary
        final_val_accuracy = history.history['val_accuracy'][-1]
        logger.info(f"Final validation accuracy: {final_val_accuracy:.4f}")

        # Optional: Capture and log model summary as plain text
        logger.info("Model summary:")
        output = io.StringIO()
        model.summary(print_fn=lambda x: output.write(x + '\n'))
        summary_text = output.getvalue()
        output.close()
        # Log each line of the summary to avoid encoding issues
        for line in summary_text.split('\n'):
            if line.strip():
                logger.info(line.replace('\u2500', '-').replace('\u2502', '|').replace('\u2514', '+').replace('\u251c', '+'))

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise