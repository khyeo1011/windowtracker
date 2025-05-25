import time
from windowTracker import WindowTracker

class WindowTrackerConsoleApp:
    def __init__(self):
        self.tracker = WindowTracker()

    def run(self, poll_interval=1):
        print("=== Window Tracker Console ===")
        print("Press Ctrl+C to stop.\n")

        try:
            while True:
                current_title = self.tracker.get_active_window_title()
                if current_title != self.tracker.last_title:
                    log_entry = self.tracker.update_window(current_title)
                    if log_entry:
                        print(log_entry)
                    self.tracker.last_title = current_title
                    self.tracker.start_time = time.time()
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\nStopping tracking...")
            summary = self.tracker.stop()
            self.display_summary(summary)

    def display_summary(self, summary):
        print("\n=== Cumulative Time Summary ===")
        for title, seconds in summary.items():
            formatted = self.tracker.format_duration(seconds)
            print(f"{title:<50} {formatted}")


# --- Entry Point ---
if __name__ == "__main__":
    app = WindowTrackerConsoleApp()
    app.run()
