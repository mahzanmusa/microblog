from celery import shared_task
import time

# Use @shared_task so it doesn't need the specific app instance attached immediately
@shared_task
def example_background_task(seconds):
    print(f"Starting task for {seconds} seconds...")
    time.sleep(seconds)
    print("Task complete!")
    return "Done"