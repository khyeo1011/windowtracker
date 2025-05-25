import time
import csv
import win32gui
from datetime import datetime, timedelta

class WindowTracker:
    def __init__(self, log_file="window_log.txt", csv_file="window_summary.csv"):
        self.last_title = None
        self.start_time = time.time()
        self.cumulative_times = {}
        self.log_file = log_file
        self.csv_file = csv_file

    def get_active_window_title(self):
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)

    def log_to_file(self, entry):
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(entry + "\n")

    def format_duration(self, seconds):
        return str(timedelta(seconds=int(seconds)))

    def write_csv_summary(self):
        with open(self.csv_file, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Window Title", "Total Time (seconds)", "Formatted Time"])
            for title, total_sec in self.cumulative_times.items():
                writer.writerow([title, f"{total_sec:.2f}", self.format_duration(total_sec)])

    def update_window(self, current_title):
        now = time.time()
        if self.last_title:
            duration = now - self.start_time
            self.cumulative_times[self.last_title] = self.cumulative_times.get(self.last_title, 0) + duration
            log_entry = (
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Switched from: '{self.last_title}' "
                f"(Spent: {duration:.2f}s, Total: {self.cumulative_times[self.last_title]:.2f}s)"
            )
            self.log_to_file(log_entry)
            return log_entry

        self.start_time = now
        return None

    def stop(self):
        if self.last_title:
            now = time.time()
            duration = now - self.start_time
            self.cumulative_times[self.last_title] = self.cumulative_times.get(self.last_title, 0) + duration
            final_log = (
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Final window: '{self.last_title}' "
                f"(Spent: {duration:.2f}s, Total: {self.cumulative_times[self.last_title]:.2f}s)"
            )
            self.log_to_file(final_log)

        self.log_to_file("\n--- Cumulative Time Summary ---")
        for title, total in self.cumulative_times.items():
            self.log_to_file(f"'{title}': {total:.2f} seconds")

        self.write_csv_summary()
        return self.cumulative_times
