from test_redis_worker_1 import add
import time

print("1. Sending task to Redis broker...")

# .delay() is the shortcut to send a task to the queue
result = add.delay(4, 4)

print(f"2. Task ID: {result.id}")
print("3. Waiting for result (Make sure your worker is running!)...")

try:
    # Wait for the result (blocks until the worker processes it)
    # timeout=10 prevents it from hanging forever if no worker is active
    output = result.get(timeout=10) 
    print(f"Success! The result is: {output}")
    print("   (This confirms Redis is working as both Broker and Result Backend)")

except Exception as e:
    print("Error or Timeout.")
    print(f"   Details: {e}")
    print("\n   TROUBLESHOOTING:")
    print("   - Did you start the Celery worker in a separate terminal?")
    print("   - Is the Redis password correct in tasks.py?")
    print("   - Is the Security Group allowing your IP?")