import os
import json
import time
import threading
import tkinter as tk
import customtkinter as ctk

class TimerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Streamers' Best Friend - Timer")
        self.root.geometry("500x600")
        ctk.set_appearance_mode("dark")
        
        self.app_data = os.path.join(os.getenv('LOCALAPPDATA'), "Streamers' Best Friend")
        if not os.path.exists(self.app_data):
            os.makedirs(self.app_data)
        
        self.timers_file = os.path.join(self.app_data, "timers.json")
        self.timers = self.load_timers()
        self.active_timers = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        header = ctk.CTkLabel(self.main_frame, text="Timer Management", font=("Arial", 20))
        header.pack(pady=10)
        
        add_btn = ctk.CTkButton(self.main_frame, text="+", command=self.create_timer, width=40, height=40)
        add_btn.pack(pady=5)
        
        self.timer_list = ctk.CTkScrollableFrame(self.main_frame)
        self.timer_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.update_timer_list()
    
    def create_timer(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("New Timer")
        settings_window.geometry("300x600")  # Made taller for new message fields
        
        # Timer name input
        name_frame = ctk.CTkFrame(settings_window)
        name_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(name_frame, text="Timer Name:").pack()
        name_entry = ctk.CTkEntry(name_frame)
        name_entry.pack(pady=5)
        
        # Starting Message Frame
        start_message_frame = ctk.CTkFrame(settings_window)
        start_message_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(start_message_frame, text="Starting Message:").pack()
        start_message_entry = ctk.CTkEntry(start_message_frame)
        start_message_entry.pack(pady=5)
        start_message_entry.insert(0, "Timer: {timer}")
        
        # Ending Message Frame
        end_message_frame = ctk.CTkFrame(settings_window)
        end_message_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(end_message_frame, text="Ending Message:").pack()
        end_message_entry = ctk.CTkEntry(end_message_frame)
        end_message_entry.pack(pady=5)
        end_message_entry.insert(0, "Timer Complete!")
        
        # Timer type selection
        type_frame = ctk.CTkFrame(settings_window)
        type_frame.pack(pady=10, padx=10, fill="x")
        
        timer_type = tk.StringVar(value="countdown")
        ctk.CTkRadioButton(type_frame, text="Countdown", variable=timer_type, value="countdown").pack(pady=5)
        ctk.CTkRadioButton(type_frame, text="Countup", variable=timer_type, value="countup").pack(pady=5)
        
        # Time settings
        time_frame = ctk.CTkFrame(settings_window)
        time_frame.pack(pady=10, padx=10, fill="x")
        
        hours = tk.IntVar(value=0)
        minutes = tk.IntVar(value=0)
        seconds = tk.IntVar(value=0)
        
        # Hours controls
        hour_frame = ctk.CTkFrame(time_frame)
        hour_frame.pack(pady=5)
        ctk.CTkLabel(hour_frame, text="Hours").pack()
        ctk.CTkButton(hour_frame, text="+", command=lambda: hours.set(hours.get() + 1)).pack(side="left", padx=5)
        ctk.CTkLabel(hour_frame, textvariable=hours).pack(side="left", padx=10)
        ctk.CTkButton(hour_frame, text="-", command=lambda: hours.set(max(0, hours.get() - 1))).pack(side="left", padx=5)
        
        # Minutes controls
        minute_frame = ctk.CTkFrame(time_frame)
        minute_frame.pack(pady=5)
        ctk.CTkLabel(minute_frame, text="Minutes").pack()
        ctk.CTkButton(minute_frame, text="+", command=lambda: minutes.set(min(59, minutes.get() + 1))).pack(side="left", padx=5)
        ctk.CTkLabel(minute_frame, textvariable=minutes).pack(side="left", padx=10)
        ctk.CTkButton(minute_frame, text="-", command=lambda: minutes.set(max(0, minutes.get() - 1))).pack(side="left", padx=5)
        
        # Seconds controls
        second_frame = ctk.CTkFrame(time_frame)
        second_frame.pack(pady=5)
        ctk.CTkLabel(second_frame, text="Seconds").pack()
        ctk.CTkButton(second_frame, text="+", command=lambda: seconds.set(min(59, seconds.get() + 1))).pack(side="left", padx=5)
        ctk.CTkLabel(second_frame, textvariable=seconds).pack(side="left", padx=10)
        ctk.CTkButton(second_frame, text="-", command=lambda: seconds.set(max(0, seconds.get() - 1))).pack(side="left", padx=5)
        
        # Button Frame
        button_frame = ctk.CTkFrame(settings_window)
        button_frame.pack(pady=20, padx=10, fill="x")
        
        def save_timer():
            timer_name = name_entry.get()
            if timer_name:
                total_seconds = hours.get() * 3600 + minutes.get() * 60 + seconds.get()
                timer_data = {
                    'name': timer_name,
                    'type': timer_type.get(),
                    'start_value': total_seconds,
                    'start_message': start_message_entry.get(),
                    'end_message': end_message_entry.get(),
                    'file_path': os.path.join(self.app_data, f"{timer_name}.txt")
                }
                
                self.timers.append(timer_data)
                with open(self.timers_file, 'w') as f:
                    json.dump(self.timers, f)
                
                with open(timer_data['file_path'], 'w') as f:
                    f.write(timer_data['start_message'].replace('{timer}', "00:00:00"))
                
                self.update_timer_list()
                settings_window.destroy()
        
        ctk.CTkButton(button_frame, text="Done", command=save_timer, width=120).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel", command=settings_window.destroy, width=120).pack(side="right", padx=5)
    
    def edit_timer(self, timer):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title(f"Edit Timer - {timer['name']}")
        settings_window.geometry("300x600")
        
        # Create all the same UI elements as create_timer
        # But populate them with existing timer data
        
        def update_timer():
            timer['name'] = name_entry.get()
            timer['type'] = timer_type.get()
            timer['start_message'] = start_message_entry.get()
            timer['end_message'] = end_message_entry.get()
            timer['start_value'] = hours.get() * 3600 + minutes.get() * 60 + seconds.get()
            
            with open(self.timers_file, 'w') as f:
                json.dump(self.timers, f)
            
            self.update_timer_list()
            settings_window.destroy()
    
    def load_timers(self):
        if os.path.exists(self.timers_file):
            with open(self.timers_file, 'r') as f:
                return json.load(f)
        return []
    
    def update_timer_list(self):
        for widget in self.timer_list.winfo_children():
            widget.destroy()
        
        for i, timer in enumerate(self.timers[:6]):
            self.create_timer_widget(timer, i)
        
        if len(self.timers) > 6:
            more_btn = ctk.CTkButton(self.timer_list, text="...", 
                                    command=self.show_more_timers)
            more_btn.pack(pady=5)
    
    def create_timer_widget(self, timer, index):
        frame = ctk.CTkFrame(self.timer_list)
        frame.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(frame, text=timer['name']).pack(side="left", padx=5)
        
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(side="right", padx=5)
        
        ctk.CTkButton(button_frame, text="Edit", 
                     command=lambda: self.edit_timer(timer),
                     width=60).pack(side="left", padx=2)
        
        ctk.CTkButton(button_frame, text="Start", 
                     command=lambda: self.start_timer(timer),
                     width=60).pack(side="left", padx=2)
        
        ctk.CTkButton(button_frame, text="Stop", 
                     command=lambda: self.stop_timer(timer),
                     width=60).pack(side="left", padx=2)
    
    def start_timer(self, timer):
        if timer['name'] not in self.active_timers:
            self.active_timers[timer['name']] = {
                'running': True,
                'thread': threading.Thread(target=self.run_timer, args=(timer,))
            }
            self.active_timers[timer['name']]['thread'].start()
    
    def stop_timer(self, timer):
        if timer['name'] in self.active_timers:
            self.active_timers[timer['name']]['running'] = False
            self.active_timers[timer['name']]['thread'].join()
            del self.active_timers[timer['name']]
    
    def run_timer(self, timer):
        current_value = timer['start_value']
        while self.active_timers[timer['name']]['running']:
            with open(timer['file_path'], 'w') as f:
                if timer['type'] == 'countdown':
                    current_value = max(0, current_value - 1)
                else:
                    current_value += 1
                
                hours = current_value // 3600
                minutes = (current_value % 3600) // 60
                seconds = current_value % 60
                
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                if current_value == 0 and timer['type'] == 'countdown':
                    output = timer.get('end_message', 'Timer Complete!')
                else:
                    message_template = timer.get('start_message', 'Timer: {timer}')
                    output = message_template.replace('{timer}', time_str)
                
                f.write(output)
            
            time.sleep(1)
    
    def show_more_timers(self):
        more_window = ctk.CTkToplevel(self.root)
        more_window.title("Additional Timers")
        more_window.geometry("400x300")
        
        scroll_frame = ctk.CTkScrollableFrame(more_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for i, timer in enumerate(self.timers[6:]):
            self.create_timer_widget(timer, i + 6)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimerApp()
    app.run()
