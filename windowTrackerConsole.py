import time
import os
from windowTracker import WindowTracker

class WindowTrackerConsoleApp:
    def __init__(self):
        self.tracker = WindowTracker()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self, poll_interval=5, summary_interval=5):
        print("=== Window Tracker Console ===")
        print("Press Ctrl+C to stop.\n")

        # Initial display of any existing summary
        if self.tracker.cumulative_times:
            print("Existing cumulative window time:")
            self.print_summary()

        last_summary_time = time.time()

        try:
            while True:
                self.clear_screen()
                current_title = self.tracker.get_active_window_title()
                if current_title != self.tracker.last_title:
                    log_entry = self.tracker.update_window(current_title)
                    if log_entry:
                        print(log_entry)
                    self.tracker.last_title = current_title
                    self.tracker.start_time = time.time()

                if time.time() - last_summary_time >= summary_interval:
                    self.print_summary()
                    last_summary_time = time.time()

                time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\nStopping tracking...")
            summary = self.tracker.stop()
            self.display_summary(summary)


    def print_summary(self):
        print("\n--- Live Cumulative Summary ---")
        for title, seconds in self.tracker.cumulative_times.items():
            formatted = self.tracker.format_duration(seconds)
            print(f"{title:<50} {formatted}")
        print()


    def display_summary(self, summary):
        print("\n=== Final Cumulative Time Summary ===")
        for title, seconds in summary.items():
            formatted = self.tracker.format_duration(seconds)
            print(f"{title:<50} {formatted}")


# --- Entry Point ---
if __name__ == "__main__":
    app = WindowTrackerConsoleApp()
    app.run()
