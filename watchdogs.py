import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define a custom event handler class
class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            # TODO: Add your code to perform useful work on file creation
            time.sleep(5)  # Simulating useful work taking 5 seconds
            print("Useful work completed!")

# Create an observer and assign the event handler
event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)

# Start the observer
print("Waiting for file creation...")
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

# Wait until the observer completes
observer.join()