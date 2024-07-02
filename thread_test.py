import threading
import time

def worker(thread_id):
    print(f"Thread {thread_id} starting.")
    time.sleep(2)  # Simulate some work
    print(f"Thread {thread_id} finished.")

# threads = []

# Create and start threads
for i in range(5):
    thread = threading.Thread(target=worker, args=(i,))
    # threads.append(thread)
    thread.start()
    thread.join()

# Wait for each thread to finish
# for thread in threads:
#     thread.join()
#     print(f"{thread.name} has terminated.")

print("All threads have terminated.")
