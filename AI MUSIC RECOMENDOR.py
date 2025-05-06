import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import json
import re
import math
# Removed PIL dependency
# Removed requests and BytesIO imports as they were only needed with PIL
# import requests
# from io import BytesIO
import webbrowser
from datetime import datetime
import threading
import time

class MelodicMuse:
    def __init__(self, root):
        self.root = root
        self.root.title("Melodic Muse")
        self.root.geometry("1000x700")
        self.root.configure(bg="#121212")
        self.root.resizable(True, True)
        
        # Custom font setup
        self.custom_font = font.Font(family="Helvetica", size=11)
        self.header_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        
        # Initialize databases
        self.load_music_database()
        
        # User preferences
        self.user_preferences = {
            "genres": [],
            "moods": [],
            "artists": [],
            "energy_level": 5,
            "discovery_level": 5,
            "history": []
        }
        
        # Create UI
        self.create_ui()
        
        # Start animation for accent elements
        self.start_accent_animation()
        
        # Dictionary to store song links and their associated tags
        self.song_links = {}
        
    def load_music_database(self):
        # In a real application, this would load from an actual database
        # For this demo, we'll create a sample music library
        self.music_database = {
            "songs": [
                {"id": 1, "title": "Moonlight Sonata", "artist": "Ludwig van Beethoven", "album": "Classical Essentials", 
                 "genre": ["classical"], "mood": ["reflective", "calm"], "year": 1801, "energy": 3,
                 "link": "https://www.youtube.com/watch?v=4Tr0otuiQuU"},
                {"id": 2, "title": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", 
                 "genre": ["rock"], "mood": ["epic", "dramatic"], "year": 1975, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"},
                {"id": 3, "title": "Take Five", "artist": "Dave Brubeck", "album": "Time Out", 
                 "genre": ["jazz"], "mood": ["smooth", "sophisticated"], "year": 1959, "energy": 5,
                 "link": "https://www.youtube.com/watch?v=vmDDOFXSgAs"},
                {"id": 4, "title": "Billie Jean", "artist": "Michael Jackson", "album": "Thriller", 
                 "genre": ["pop"], "mood": ["energetic", "groovy"], "year": 1982, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"},
                {"id": 5, "title": "Gymnopedie No.1", "artist": "Erik Satie", "album": "Piano Works", 
                 "genre": ["classical"], "mood": ["peaceful", "melancholic"], "year": 1888, "energy": 2,
                 "link": "https://www.youtube.com/watch?v=S-Xm7s9eGxU"},
                {"id": 6, "title": "Take Me Home, Country Roads", "artist": "John Denver", "album": "Poems, Prayers & Promises", 
                 "genre": ["country", "folk"], "mood": ["nostalgic", "uplifting"], "year": 1971, "energy": 6,
                 "link": "https://www.youtube.com/watch?v=1vrEljMfXYo"},
                {"id": 7, "title": "Giant Steps", "artist": "John Coltrane", "album": "Giant Steps", 
                 "genre": ["jazz"], "mood": ["complex", "energetic"], "year": 1960, "energy": 7,
                 "link": "https://www.youtube.com/watch?v=KwIC6B_dvW4"},
                {"id": 8, "title": "Yesterday", "artist": "The Beatles", "album": "Help!", 
                 "genre": ["rock", "pop"], "mood": ["melancholic", "reflective"], "year": 1965, "energy": 4,
                 "link": "https://www.youtube.com/watch?v=NrgmdOz227I"},
                {"id": 9, "title": "Danza Kuduro", "artist": "Don Omar ft. Lucenzo", "album": "Meet the Orphans", 
                 "genre": ["reggaeton", "latin"], "mood": ["energetic", "party"], "year": 2010, "energy": 9,
                 "link": "https://www.youtube.com/watch?v=7zp1TbLFPp8"},
                {"id": 10, "title": "Hurt", "artist": "Johnny Cash", "album": "American IV", 
                 "genre": ["country", "folk"], "mood": ["sad", "reflective"], "year": 2002, "energy": 4,
                 "link": "https://www.youtube.com/watch?v=8AHCfZTRGiI"},
                {"id": 11, "title": "Africa", "artist": "Toto", "album": "Toto IV", 
                 "genre": ["rock", "pop"], "mood": ["nostalgic", "uplifting"], "year": 1982, "energy": 7,
                 "link": "https://www.youtube.com/watch?v=FTQbiNvZqaY"},
                {"id": 12, "title": "Imagine", "artist": "John Lennon", "album": "Imagine", 
                 "genre": ["rock", "pop"], "mood": ["peaceful", "thoughtful"], "year": 1971, "energy": 4,
                 "link": "https://www.youtube.com/watch?v=YkgkThdzX-8"},
                {"id": 13, "title": "Dancing Queen", "artist": "ABBA", "album": "Arrival", 
                 "genre": ["pop", "disco"], "mood": ["happy", "energetic"], "year": 1976, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=xFrGuyw1V8s"},
                {"id": 14, "title": "Hotel California", "artist": "Eagles", "album": "Hotel California", 
                 "genre": ["rock"], "mood": ["mysterious", "nostalgic"], "year": 1977, "energy": 6,
                 "link": "https://www.youtube.com/watch?v=BciS5krYL80"},
                {"id": 15, "title": "Enter Sandman", "artist": "Metallica", "album": "Metallica", 
                 "genre": ["metal", "rock"], "mood": ["intense", "dark"], "year": 1991, "energy": 9,
                 "link": "https://www.youtube.com/watch?v=CD-E-LDc384"},
                {"id": 16, "title": "The Four Seasons", "artist": "Antonio Vivaldi", "album": "Classical Masterpieces", 
                 "genre": ["classical"], "mood": ["dramatic", "joyful"], "year": 1725, "energy": 6,
                 "link": "https://www.youtube.com/watch?v=GRxofEmo3HA"},
                {"id": 17, "title": "In Da Club", "artist": "50 Cent", "album": "Get Rich or Die Tryin'", 
                 "genre": ["hip-hop", "rap"], "mood": ["confident", "energetic"], "year": 2003, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=5qm8PH4xAss"},
                {"id": 18, "title": "Despacito", "artist": "Luis Fonsi ft. Daddy Yankee", "album": "Vida", 
                 "genre": ["reggaeton", "latin"], "mood": ["sensual", "party"], "year": 2017, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=kJQP7kiw5Fk"},
                {"id": 19, "title": "Nothing Else Matters", "artist": "Metallica", "album": "Metallica", 
                 "genre": ["metal", "rock"], "mood": ["emotional", "intense"], "year": 1991, "energy": 5,
                 "link": "https://www.youtube.com/watch?v=tAGnKpE4NCI"},
                {"id": 20, "title": "Like a Rolling Stone", "artist": "Bob Dylan", "album": "Highway 61 Revisited", 
                 "genre": ["rock", "folk"], "mood": ["rebellious", "provocative"], "year": 1965, "energy": 7,
                 "link": "https://www.youtube.com/watch?v=IwOfCgkyEj0"},
                {"id": 21, "title": "Toxic", "artist": "Britney Spears", "album": "In the Zone", 
                 "genre": ["pop"], "mood": ["energetic", "sensual"], "year": 2003, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=LOZuxwVk7TU"},
                {"id": 22, "title": "Lose Yourself", "artist": "Eminem", "album": "8 Mile Soundtrack", 
                 "genre": ["hip-hop", "rap"], "mood": ["motivational", "intense"], "year": 2002, "energy": 9,
                 "link": "https://www.youtube.com/watch?v=_Yhyp-_hX2s"},
                {"id": 23, "title": "Für Elise", "artist": "Ludwig van Beethoven", "album": "Piano Classics", 
                 "genre": ["classical"], "mood": ["gentle", "melancholic"], "year": 1810, "energy": 3,
                 "link": "https://www.youtube.com/watch?v=_mVW8tgGY_w"},
                {"id": 24, "title": "Smooth", "artist": "Santana ft. Rob Thomas", "album": "Supernatural", 
                 "genre": ["rock", "latin"], "mood": ["smooth", "groovy"], "year": 1999, "energy": 7,
                 "link": "https://www.youtube.com/watch?v=6Whgn_iE5uc"},
                {"id": 25, "title": "Symphony No. 9", "artist": "Ludwig van Beethoven", "album": "Classical Masterworks", 
                 "genre": ["classical"], "mood": ["triumphant", "epic"], "year": 1824, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=t3217H8JppI"},
                {"id": 26, "title": "So What", "artist": "Miles Davis", "album": "Kind of Blue", 
                 "genre": ["jazz"], "mood": ["cool", "sophisticated"], "year": 1959, "energy": 5,
                 "link": "https://www.youtube.com/watch?v=zqNTltOGh5c"},
                {"id": 27, "title": "Jolene", "artist": "Dolly Parton", "album": "Jolene", 
                 "genre": ["country"], "mood": ["heartbreak", "emotional"], "year": 1973, "energy": 5,
                 "link": "https://www.youtube.com/watch?v=Ixrje2rXLMA"},
                {"id": 28, "title": "Thriller", "artist": "Michael Jackson", "album": "Thriller", 
                 "genre": ["pop", "funk"], "mood": ["mysterious", "exciting"], "year": 1982, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=sOnqjkJTMaA"},
                {"id": 29, "title": "Smells Like Teen Spirit", "artist": "Nirvana", "album": "Nevermind", 
                 "genre": ["rock", "grunge"], "mood": ["rebellious", "angry"], "year": 1991, "energy": 9,
                 "link": "https://www.youtube.com/watch?v=hTWKbfoikeg"},
                {"id": 30, "title": "Take On Me", "artist": "a-ha", "album": "Hunting High and Low", 
                 "genre": ["pop", "synthpop"], "mood": ["uplifting", "nostalgic"], "year": 1984, "energy": 8,
                 "link": "https://www.youtube.com/watch?v=djV11Xbc914"},
                # More songs would be added in a real application
            ]
        }
        
        # Extract all genres, moods, and artists for filtering
        self.all_genres = sorted(list(set([genre for song in self.music_database["songs"] for genre in song["genre"]])))
        self.all_moods = sorted(list(set([mood for song in self.music_database["songs"] for mood in song["mood"]])))
        self.all_artists = sorted(list(set([song["artist"] for song in self.music_database["songs"]])))
    
    def create_ui(self):
        # Main frame container
        self.main_frame = tk.Frame(self.root, bg="#121212")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title bar with logo
        self.title_bar = tk.Frame(self.main_frame, bg="#1DB954", height=60)
        self.title_bar.pack(fill=tk.X, pady=(0, 20))
        
        # App title
        title_label = tk.Label(self.title_bar, text="Melodic Muse", font=self.title_font, 
                              bg="#1DB954", fg="#FFFFFF")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Tagline
        tagline_label = tk.Label(self.title_bar, text="Your Personal Music Connoisseur", 
                                font=self.custom_font, bg="#1DB954", fg="#FFFFFF")
        tagline_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Split the main area into left and right panels
        self.content_frame = tk.Frame(self.main_frame, bg="#121212")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for filters and preferences
        self.left_panel = tk.Frame(self.content_frame, bg="#181818", width=300)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Make the left panel maintain its width
        self.left_panel.pack_propagate(False)
        
        # Right panel for chat and recommendations
        self.right_panel = tk.Frame(self.content_frame, bg="#181818")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)
        
        # Create the content for each panel
        self.create_filter_panel()
        self.create_chat_panel()
        
        # Status bar
        self.status_bar = tk.Frame(self.main_frame, bg="#282828", height=30)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Now playing info
        self.now_playing_label = tk.Label(self.status_bar, text="Ready to discover new music", 
                                         font=("Helvetica", 9), bg="#282828", fg="#B3B3B3")
        self.now_playing_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Add animated accent elements
        self.create_accent_elements()
    
    def create_filter_panel(self):
        # Header
        filter_header = tk.Label(self.left_panel, text="Personalize Your Experience", 
                                font=self.header_font, bg="#181818", fg="#FFFFFF")
        filter_header.pack(fill=tk.X, padx=10, pady=10)
        
        # Create scrollable area for filters
        canvas = tk.Canvas(self.left_panel, bg="#181818", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.left_panel, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#181818")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Genre selection
        genre_label = tk.Label(scrollable_frame, text="Genres", font=self.custom_font, 
                              bg="#181818", fg="#FFFFFF")
        genre_label.pack(fill=tk.X, padx=10, pady=(10, 5), anchor="w")
        
        self.genre_vars = {}
        genres_frame = tk.Frame(scrollable_frame, bg="#181818")
        genres_frame.pack(fill=tk.X, padx=20)
        
        for i, genre in enumerate(self.all_genres):
            var = tk.BooleanVar(value=False)
            self.genre_vars[genre] = var
            cb = ttk.Checkbutton(genres_frame, text=genre.capitalize(), variable=var, 
                                 style="Switch.TCheckbutton")
            cb.grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
        
        # Mood selection
        mood_label = tk.Label(scrollable_frame, text="Moods", font=self.custom_font, 
                             bg="#181818", fg="#FFFFFF")
        mood_label.pack(fill=tk.X, padx=10, pady=(15, 5), anchor="w")
        
        self.mood_vars = {}
        moods_frame = tk.Frame(scrollable_frame, bg="#181818")
        moods_frame.pack(fill=tk.X, padx=20)
        
        for i, mood in enumerate(self.all_moods):
            var = tk.BooleanVar(value=False)
            self.mood_vars[mood] = var
            cb = ttk.Checkbutton(moods_frame, text=mood.capitalize(), variable=var, 
                                 style="Switch.TCheckbutton")
            cb.grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
        
        # Energy level slider
        energy_label = tk.Label(scrollable_frame, text="Energy Level", font=self.custom_font, 
                               bg="#181818", fg="#FFFFFF")
        energy_label.pack(fill=tk.X, padx=10, pady=(15, 5), anchor="w")
        
        self.energy_var = tk.IntVar(value=5)
        energy_slider = ttk.Scale(scrollable_frame, from_=1, to=10, orient="horizontal", 
                                  variable=self.energy_var, style="Horizontal.TScale")
        energy_slider.pack(fill=tk.X, padx=20, pady=5)
        
        energy_value_frame = tk.Frame(scrollable_frame, bg="#181818")
        energy_value_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(energy_value_frame, text="Calm", bg="#181818", fg="#B3B3B3", 
                font=("Helvetica", 9)).pack(side=tk.LEFT)
        tk.Label(energy_value_frame, text="Energetic", bg="#181818", fg="#B3B3B3", 
                font=("Helvetica", 9)).pack(side=tk.RIGHT)
        
        # Discovery level slider
        discovery_label = tk.Label(scrollable_frame, text="Discovery Level", font=self.custom_font, 
                                  bg="#181818", fg="#FFFFFF")
        discovery_label.pack(fill=tk.X, padx=10, pady=(15, 5), anchor="w")
        
        self.discovery_var = tk.IntVar(value=5)
        discovery_slider = ttk.Scale(scrollable_frame, from_=1, to=10, orient="horizontal", 
                                     variable=self.discovery_var, style="Horizontal.TScale")
        discovery_slider.pack(fill=tk.X, padx=20, pady=5)
        
        discovery_value_frame = tk.Frame(scrollable_frame, bg="#181818")
        discovery_value_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(discovery_value_frame, text="Familiar", bg="#181818", fg="#B3B3B3", 
                font=("Helvetica", 9)).pack(side=tk.LEFT)
        tk.Label(discovery_value_frame, text="Adventurous", bg="#181818", fg="#B3B3B3", 
                font=("Helvetica", 9)).pack(side=tk.RIGHT)
        
        # Update button
        update_button = tk.Button(scrollable_frame, text="Update Preferences", 
                                 font=self.custom_font, bg="#1DB954", fg="#FFFFFF",
                                 activebackground="#18A64B", activeforeground="#FFFFFF",
                                 command=self.update_preferences)
        update_button.pack(fill=tk.X, padx=20, pady=20)
        
        # Configure style for checkbuttons and scales
        style = ttk.Style()
        style.configure("Switch.TCheckbutton", background="#181818", foreground="#FFFFFF")
        style.map("Switch.TCheckbutton",
                 background=[("active", "#181818")],
                 foreground=[("active", "#1DB954")])
        
        style.configure("Horizontal.TScale", background="#181818", troughcolor="#333333")
    
    def create_chat_panel(self):
        # Chat display area
        self.chat_frame = tk.Frame(self.right_panel, bg="#181818")
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat header
        chat_header = tk.Label(self.chat_frame, text="Melodic Muse Assistant", 
                              font=self.header_font, bg="#181818", fg="#FFFFFF")
        chat_header.pack(fill=tk.X, pady=10)
        
        # Create the chat display
        self.chat_display = tk.Text(self.chat_frame, bg="#282828", fg="#FFFFFF", 
                                   font=self.custom_font, wrap=tk.WORD, state=tk.DISABLED,
                                   padx=10, pady=10)
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Configure hyperlink behavior
        self.chat_display.tag_configure("link", foreground="#1DB954", underline=1)
        self.chat_display.tag_bind("link", "<Enter>", self._on_link_enter)
        self.chat_display.tag_bind("link", "<Leave>", self._on_link_leave)
        self.chat_display.tag_bind("link", "<Button-1>", self._on_link_click)
        
        # Chat input area
        input_frame = tk.Frame(self.chat_frame, bg="#181818")
        input_frame.pack(fill=tk.X, pady=5)
        
        self.chat_input = tk.Entry(input_frame, bg="#282828", fg="#FFFFFF", 
                                  font=self.custom_font, insertbackground="#FFFFFF")
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.chat_input.bind("<Return>", self.send_message)
        
        send_button = tk.Button(input_frame, text="Send", font=self.custom_font, 
                               bg="#1DB954", fg="#FFFFFF", command=self.send_message,
                               activebackground="#18A64B", activeforeground="#FFFFFF")
        send_button.pack(side=tk.RIGHT)
        
        # Add initial welcome message
        self.update_chat("Melodic Muse", "Welcome to Melodic Muse! I'm your personal music assistant. "
                        "Tell me what you're in the mood for, or ask for recommendations based on your preferences. "
                        "You can also update your preferences in the panel on the left.")
        
        # Set app icon (text-based since we removed PIL)
        try:
            self.root.iconbitmap(default="")  # Empty default to avoid system icon
        except:
            pass  # Ignore if iconbitmap fails
            
    def _on_link_enter(self, event):
        """Change cursor when hovering over a link"""
        self.chat_display.config(cursor="hand2")
        
    def _on_link_leave(self, event):
        """Change cursor back when leaving a link"""
        self.chat_display.config(cursor="")
        
    def _on_link_click(self, event):
        """Open the link when clicked"""
        for tag_name in self.chat_display.tag_names(tk.CURRENT):
            if tag_name in self.song_links:
                webbrowser.open_new_tab(self.song_links[tag_name])
                break
    
    def create_accent_elements(self):
        # Create a canvas for accent elements (music notes, waves, etc.)
        self.accent_canvas = tk.Canvas(self.main_frame, bg="#121212", 
                                      highlightthickness=0, height=0)
        self.accent_canvas.place(relx=1, rely=0.2, anchor="e", width=150, height=400)
        
        # Add decorative accent elements
        self.accent_elements = []
        colors = ["#1DB954", "#1ED760", "#FFFFFF"]
        
        for i in range(12):
            x = random.randint(0, 150)
            y = random.randint(0, 400)
            size = random.randint(3, 10)
            color = random.choice(colors)
            opacity = random.uniform(0.3, 0.8)
            
            # Create particle effect
            element = self.accent_canvas.create_oval(x, y, x+size, y+size, 
                                                   fill=color, outline="", 
                                                   stipple="gray50")
            
            self.accent_elements.append({
                "id": element,
                "x": x,
                "y": y,
                "size": size,
                "color": color,
                "speed": random.uniform(0.5, 2),
                "direction": random.uniform(0, 2 * math.pi)
            })
    
    def start_accent_animation(self):
        def animate():
            for element in self.accent_elements:
                # Move element
                dx = math.cos(element["direction"]) * element["speed"]
                dy = math.sin(element["direction"]) * element["speed"]
                
                self.accent_canvas.move(element["id"], dx, dy)
                
                # Update position
                element["x"] += dx
                element["y"] += dy
                
                # Bounce off walls
                if element["x"] < 0 or element["x"] > 150:
                    element["direction"] = math.pi - element["direction"]
                
                if element["y"] < 0 or element["y"] > 400:
                    element["direction"] = -element["direction"]
            
            # Continue animation
            self.root.after(50, animate)
        
        # Start animation
        animate()
    
    def update_preferences(self):
        # Update user preferences based on UI selections
        self.user_preferences["genres"] = [genre for genre, var in self.genre_vars.items() if var.get()]
        self.user_preferences["moods"] = [mood for mood, var in self.mood_vars.items() if var.get()]
        self.user_preferences["energy_level"] = self.energy_var.get()
        self.user_preferences["discovery_level"] = self.discovery_var.get()
        
        # Provide feedback
        self.update_chat("Melodic Muse", "Your preferences have been updated! Here's what I understand:\n" +
                        f"Genres: {', '.join(self.user_preferences['genres']) if self.user_preferences['genres'] else 'Any'}\n" +
                        f"Moods: {', '.join(self.user_preferences['moods']) if self.user_preferences['moods'] else 'Any'}\n" +
                        f"Energy Level: {self.user_preferences['energy_level']}/10\n" +
                        f"Discovery Level: {self.user_preferences['discovery_level']}/10\n\n" +
                        "How can I help you discover music today?")
    
    def send_message(self, event=None):
        message = self.chat_input.get().strip()
        if not message:
            return
        
        # Clear the input field
        self.chat_input.delete(0, tk.END)
        
        # Display user message
        self.update_chat("You", message)
        
        # Process user message and generate response
        self.process_message(message)
    
    def update_chat(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        # Format the message
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
            self.chat_display.insert(tk.END, f"{sender}: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n", "user_message")
        else:
            self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
            self.chat_display.insert(tk.END, f"{sender}: ", "assistant")
            self.chat_display.insert(tk.END, f"{message}\n", "assistant_message")
        
        # Apply tags for styling
        self.chat_display.tag_configure("timestamp", foreground="#B3B3B3", font=("Helvetica", 9))
        self.chat_display.tag_configure("user", foreground="#1DB954", font=("Helvetica", 11, "bold"))
        self.chat_display.tag_configure("user_message", foreground="#FFFFFF", font=("Helvetica", 11))
        self.chat_display.tag_configure("assistant", foreground="#1ED760", font=("Helvetica", 11, "bold"))
        self.chat_display.tag_configure("assistant_message", foreground="#FFFFFF", font=("Helvetica", 11))
        
        # Scroll to the bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def process_message(self, message):
        # Convert message to lowercase for easier processing
        message_lower = message.lower()
        
        # Simulate "thinking" with a delay and animation
        self.update_chat("Melodic Muse", "Exploring the musical universe for you...")
        
        # Run the actual processing in a separate thread to keep UI responsive
        threading.Thread(target=self._process_message_thread, args=(message_lower,)).start()
    
    def _process_message_thread(self, message_lower):
        # Simulate processing time
        time.sleep(1.5)
        
        # Check for different types of queries
        if any(word in message_lower for word in ["recommend", "suggestion", "suggest"]):
            self._get_recommendations()
        
        elif any(word in message_lower for word in ["genre", "genres"]):
            genre_matches = re.findall(r'(?:like|love|enjoy|into|prefer)\s+([a-z]+(?:\s+[a-z]+)*)', message_lower)
            if genre_matches:
                for genre in self.all_genres:
                    if genre in message_lower:
                        self.genre_vars[genre].set(True)
                self.update_preferences()
            else:
                # Return list of available genres
                genres_list = ", ".join(self.all_genres)
                self.root.after(0, lambda: self.update_chat("Melodic Muse", 
                    f"I can recommend music from these genres: {genres_list}. What kind of genre are you interested in?"))
        
        elif any(word in message_lower for word in ["mood", "feeling", "vibe"]):
            mood_matches = re.findall(r'(?:feeling|mood|vibe is|vibes)\s+([a-z]+(?:\s+[a-z]+)*)', message_lower)
            if mood_matches:
                for mood in self.all_moods:
                    if mood in message_lower:
                        self.mood_vars[mood].set(True)
                self.update_preferences()
            else:
                # Return list of available moods
                moods_list = ", ".join(self.all_moods)
                self.root.after(0, lambda: self.update_chat("Melodic Muse", 
                    f"I can recommend music for these moods: {moods_list}. How are you feeling today?"))
        
        elif "help" in message_lower:
            help_message = (
                "Here's how I can help you:\n\n"
                "- Ask for music recommendations based on mood, genre, or energy level\n"
                "- Update your preferences using the panel on the left\n"
                "- Ask about specific genres or moods\n"
                "- Request music for specific activities (workout, study, relax)\n"
                "- Get information about songs in our database\n\n"
                "For example, try asking:\n"
                "• \"Recommend some energetic rock songs\"\n"
                "• \"I'm feeling melancholic today\"\n"
                "• \"What jazz songs do you have?\"\n"
                "• \"Music for studying\""
            )
            self.root.after(0, lambda: self.update_chat("Melodic Muse", help_message))
        
        elif any(activity in message_lower for activity in ["study", "studying", "work", "working", "focus"]):
            self.mood_vars["peaceful"].set(True)
            self.mood_vars["calm"].set(True)
            self.energy_var.set(3)
            self.update_preferences()
            self._get_study_recommendations()
        
        elif any(activity in message_lower for activity in ["workout", "exercise", "training", "run", "running"]):
            self.mood_vars["energetic"].set(True)
            self.energy_var.set(9)
            self.update_preferences()
            self._get_workout_recommendations()
            
        elif any(activity in message_lower for activity in ["relax", "relaxing", "chill", "calm", "sleep"]):
            self.mood_vars["peaceful"].set(True)
            self.mood_vars["calm"].set(True)
            self.energy_var.set(2)
            self.update_preferences()
            self._get_relaxation_recommendations()
            
        elif any(word in message_lower for word in ["party", "dance", "celebration"]):
            self.mood_vars["energetic"].set(True)
            self.mood_vars["happy"].set(True)
            self.energy_var.set(9)
            self.update_preferences()
            self._get_party_recommendations()
            
        elif "artist" in message_lower or "by" in message_lower:
            # Try to extract artist name
            artist_match = None
            for artist in self.all_artists:
                if artist.lower() in message_lower:
                    artist_match = artist
                    break
            
            if artist_match:
                self._get_artist_recommendations(artist_match)
            else:
                self.root.after(0, lambda: self.update_chat("Melodic Muse", 
                    "I couldn't identify which artist you're interested in. Please mention the artist's name clearly."))
        
        elif "history" in message_lower:
            self._show_recommendation_history()
            
        elif "thank" in message_lower:
            responses = [
                "You're welcome! I'm here to help you discover amazing music.",
                "My pleasure! Music is a journey best shared.",
                "Glad to be your musical companion. Anything else you'd like to explore?",
                "You're welcome! Don't hesitate to ask for more recommendations anytime."
            ]
            self.root.after(0, lambda: self.update_chat("Melodic Muse", random.choice(responses)))
            
        else:
            # Generic recommendation if we can't categorize the query
            self._get_recommendations()
    
    def _get_recommendations(self):
        """Generate music recommendations based on user preferences"""
        filtered_songs = self.music_database["songs"].copy()
        
        # Apply filters based on user preferences
        if self.user_preferences["genres"]:
            filtered_songs = [song for song in filtered_songs 
                             if any(genre in self.user_preferences["genres"] for genre in song["genre"])]
        
        if self.user_preferences["moods"]:
            filtered_songs = [song for song in filtered_songs 
                             if any(mood in self.user_preferences["moods"] for mood in song["mood"])]
        
        # Filter by energy level (with some tolerance)
        energy_level = self.user_preferences["energy_level"]
        energy_min = max(1, energy_level - 2)
        energy_max = min(10, energy_level + 2)
        filtered_songs = [song for song in filtered_songs 
                         if energy_min <= song["energy"] <= energy_max]
        
        # If no songs match the criteria, use all songs
        if not filtered_songs:
            filtered_songs = self.music_database["songs"].copy()
            self.root.after(0, lambda: self.update_chat("Melodic Muse", 
                "I couldn't find songs that exactly match your preferences, so here are some general recommendations:"))
        
        # Select songs based on discovery level
        # Lower discovery = more popular/common songs
        # Higher discovery = more obscure/varied selections
        num_recommendations = min(5, len(filtered_songs))
        
        if self.user_preferences["discovery_level"] <= 3:
            # For low discovery, prioritize popular songs
            recommended_songs = sorted(filtered_songs, key=lambda s: s["year"], reverse=True)[:10]
            recommended_songs = random.sample(recommended_songs, min(num_recommendations, len(recommended_songs)))
        elif self.user_preferences["discovery_level"] >= 8:
            # For high discovery, prioritize variety and obscurity
            recommended_songs = random.sample(filtered_songs, min(num_recommendations, len(filtered_songs)))
        else:
            # For medium discovery, balanced approach
            recommended_songs = random.sample(filtered_songs, min(num_recommendations, len(filtered_songs)))
        
        # Create recommendation message
        if recommended_songs:
            recommendation_text = "Based on your preferences, here are some recommendations:\n\n"
            
            for i, song in enumerate(recommended_songs, 1):
                recommendation_text += f"{i}. \"{song['title']}\" by {song['artist']} ({song['year']})\n"
                recommendation_text += f"   Album: {song['album']}\n"
                recommendation_text += f"   Genre: {', '.join(song['genre'])}\n"
                recommendation_text += f"   Mood: {', '.join(song['mood'])}\n\n"
                
                # Add to history
                if song not in self.user_preferences["history"]:
                    self.user_preferences["history"].append(song)
            
            recommendation_text += "Would you like more specific recommendations, or should I refine these based on your feedback?"
            
            # Update now playing with the first recommendation
            self.now_playing_label.config(text=f"Suggested: {recommended_songs[0]['title']} by {recommended_songs[0]['artist']}")
            
            self.root.after(0, lambda: self.update_chat("Melodic Muse", recommendation_text))
        else:
            self.root.after(0, lambda: self.update_chat("Melodic Muse", 
                "I couldn't find any songs matching your criteria. Try adjusting your preferences or exploring different genres."))
    
    def _get_study_recommendations(self):
        """Generate recommendations for studying/focusing"""
        study_songs = [song for song in self.music_database["songs"] 
                      if any(mood in ["peaceful", "calm", "sophisticated", "reflective"] for mood in song["mood"])
                      and song["energy"] <= 5]
        
        if not study_songs:
            study_songs = [song for song in self.music_database["songs"] if song["energy"] <= 4]
        
        num_recommendations = min(3, len(study_songs))
        recommended_songs = random.sample(study_songs, num_recommendations)
        
        recommendation_text = "Here are some perfect songs for studying and focusing:\n\n"
        
        for i, song in enumerate(recommended_songs, 1):
            recommendation_text += f"{i}. \"{song['title']}\" by {song['artist']} ({song['year']})\n"
            recommendation_text += f"   Album: {song['album']}\n"
            recommendation_text += f"   Why it's good for studying: "
            
            if "classical" in song["genre"]:
                recommendation_text += "Classical music enhances cognitive function and focus.\n\n"
            elif "jazz" in song["genre"]:
                recommendation_text += "Jazz improves creativity while maintaining a steady focus.\n\n"
            else:
                recommendation_text += f"The {', '.join(song['mood'])} mood creates an ideal study atmosphere.\n\n"
            
            # Add to history
            if song not in self.user_preferences["history"]:
                self.user_preferences["history"].append(song)
        
        recommendation_text += "Would you like more study music recommendations? I can also suggest music for deep work or creative studying."
        
        # Update now playing
        self.now_playing_label.config(text=f"Study Session: {recommended_songs[0]['title']} by {recommended_songs[0]['artist']}")
        
        self.root.after(0, lambda: self.update_chat("Melodic Muse", recommendation_text))
    
    def _get_workout_recommendations(self):
        """Generate recommendations for workouts/exercise"""
        workout_songs = [song for song in self.music_database["songs"] 
                        if any(mood in ["energetic", "intense", "motivational"] for mood in song["mood"])
                        and song["energy"] >= 7]
        
        if not workout_songs:
            workout_songs = [song for song in self.music_database["songs"] if song["energy"] >= 7]
        
        num_recommendations = min(3, len(workout_songs))
        recommended_songs = random.sample(workout_songs, num_recommendations)
        
        recommendation_text = "Here are some high-energy tracks to fuel your workout:\n\n"
        
        for i, song in enumerate(recommended_songs, 1):
            recommendation_text += f"{i}. \"{song['title']}\" by {song['artist']} ({song['year']})\n"
            recommendation_text += f"   Album: {song['album']}\n"
            recommendation_text += f"   Energy Level: {song['energy']}/10\n"
            recommendation_text += f"   Perfect for: {' and '.join(song['mood'])} workouts\n\n"
            
            # Add to history
            if song not in self.user_preferences["history"]:
                self.user_preferences["history"].append(song)
        
        recommendation_text += "These tracks will keep your energy up! Would you like more workout music or something for cool-down?"
        
        # Update now playing
        self.now_playing_label.config(text=f"Workout Mix: {recommended_songs[0]['title']} by {recommended_songs[0]['artist']}")
        
        self.root.after(0, lambda: self.update_chat("Melodic Muse", recommendation_text))
    
    def _get_relaxation_recommendations(self):
        """Generate recommendations for relaxation"""
        relax_songs = [song for song in self.music_database["songs"] 
                      if any(mood in ["peaceful", "calm", "melancholic", "gentle"] for mood in song["mood"])
                      and song["energy"] <= 4]
        
        if not relax_songs:
            relax_songs = [song for song in self.music_database["songs"] if song["energy"] <= 3]
        
        num_recommendations = min(3, len(relax_songs))
        recommended_songs = random.sample(relax_songs, num_recommendations)
        
        recommendation_text = "Here are some soothing tracks to help you relax and unwind:\n\n"
        
        for i, song in enumerate(recommended_songs, 1):
            recommendation_text += f"{i}. \"{song['title']}\" by {song['artist']} ({song['year']})\n"
            recommendation_text += f"   Album: {song['album']}\n"
            recommendation_text += f"   Mood: {', '.join(song['mood'])}\n"
            
            if "classical" in song["genre"]:
                recommendation_text += "   Classical pieces are perfect for deep relaxation and stress relief.\n\n"
            else:
                recommendation_text += f"   The gentle {song['energy']}/10 energy level creates a calming atmosphere.\n\n"
            
            # Add to history
            if song not in self.user_preferences["history"]:
                self.user_preferences["history"].append(song)
        
        recommendation_text += "These selections should help create a tranquil atmosphere. Would you like more relaxation music or perhaps some ambient tracks?"
        
        # Update now playing
        self.now_playing_label.config(text=f"Relaxation: {recommended_songs[0]['title']} by {recommended_songs[0]['artist']}")
        
        self.root.after(0, lambda: self.update_chat("Melodic Muse", recommendation_text))
            
    def _get_party_recommendations(self):
        """Generate recommendations for parties/dancing"""
        party_songs = [song for song in self.music_database["songs"] 
                      if any(mood in ["energetic", "party", "happy", "groovy"] for mood in song["mood"])
                      and song["energy"] >= 7]
        
        if not party_songs:
            party_songs = [song for song in self.music_database["songs"] if song["energy"] >= 8]
        
        num_recommendations = min(3, len(party_songs))
        recommended_songs = random.sample(party_songs, num_recommendations)
        
        recommendation_text = "Let's get this party started! Here are some tracks to keep everyone dancing:\n\n"
        
        for i, song in enumerate(recommended_songs, 1):
            recommendation_text += f"{i}. \"{song['title']}\" by {song['artist']} ({song['year']})\n"
            recommendation_text += f"   Album: {song['album']}\n"
            recommendation_text += f"   Genre: {', '.join(song['genre'])}\n"
            recommendation_text += f"   Dance Floor Energy: {song['energy']}/10\n\n"
            
            # Add to history
            if song not in self.user_preferences["history"]:
                self.user_preferences["history"].append(song)
        
        recommendation_text += "These tracks should keep the energy high! Would you like more party hits or maybe some classics everyone knows?"
        
        # Update now playing
        self.now_playing_label.config(text=f"Party Mix: {recommended_songs[0]['title']} by {recommended_songs[0]['artist']}")
        
        self.root.after(0, lambda: self.update_chat("Melodic Muse", recommendation_text))
    
    def _get_artist_recommendations(self, artist):
        """Generate recommendations for a specific artist"""
        artist_songs = [song for song in self.music_database["songs"] if song["artist"] == artist]
        
        if not artist_songs:
            self.root.after(0, lambda: self.update_chat("Melodic Muse", 
                f"I couldn't find any songs by {artist} in my database. Try another artist or a different type of recommendation."))
            return
        
        # Get all songs by this artist
        recommendation_text = f"Here are songs by {artist} in my collection:\n\n"
        
        for i, song in enumerate(artist_songs, 1):
            recommendation_text += f"{i}. \"{song['title']}\" ({song['year']})\n"
            recommendation_text += f"   Album: {song['album']}\n"
            recommendation_text += f"   Genre: {', '.join(song['genre'])}\n"
            recommendation_text += f"   Mood: {', '.join(song['mood'])}\n\n"
            
            # Add to history
            if song not in self.user_preferences["history"]:
                self.user_preferences["history"].append(song)
        
        # Add similar artists recommendation
        genres = [genre for song in artist_songs for genre in song["genre"]]
        most_common_genre = max(set(genres), key=genres.count)
        
        similar_artists = set([song["artist"] for song in self.music_database["songs"] 
                              if most_common_genre in song["genre"] and song["artist"] != artist])
        
        if similar_artists:
            recommendation_text += f"If you like {artist}, you might also enjoy these similar artists:\n"
            for i, similar in enumerate(list(similar_artists)[:3], 1):
                recommendation_text += f"{i}. {similar}\n"
        
        # Update now playing
        self.now_playing_label.config(text=f"Artist Focus: {artist} - {artist_songs[0]['title']}")
        
        self.root.after(0, lambda: self.update_chat("Melodic Muse", recommendation_text))
    
    def _show_recommendation_history(self):
        """Show the user's recommendation history"""
        if not self.user_preferences["history"]:
            self.root.after(0, lambda: self.update_chat("Melodic Muse", 
                "You haven't received any recommendations yet. Try asking for some music recommendations first!"))
            return
        
        history_text = "Here's your recommendation history:\n\n"
        
        # Show the most recent 5 recommendations
        recent_history = self.user_preferences["history"][-5:]
        
        for i, song in enumerate(recent_history, 1):
            history_text += f"{i}. \"{song['title']}\" by {song['artist']} ({song['year']})\n"
            history_text += f"   Album: {song['album']}\n"
            history_text += f"   Genre: {', '.join(song['genre'])}\n\n"
        
        history_text += "Would you like more recommendations based on your history, or would you prefer to explore something new?"
        
        self.root.after(0, lambda: self.update_chat("Melodic Muse", history_text))


# Main application execution
if __name__ == "__main__":
    root = tk.Tk()
    app = MelodicMuse(root)
    
    # Set dark theme for all ttk widgets
    style = ttk.Style()
    style.theme_use('default')
    
    # Configure colors for ttk widgets
    style.configure("TButton", background="#1DB954", foreground="#FFFFFF", 
                   padding=6, relief="flat", font=("Helvetica", 11))
    style.map("TButton",
             background=[("active", "#18A64B"), ("pressed", "#168F41")],
             foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")])
    
    style.configure("Horizontal.TScale", background="#181818", troughcolor="#333333")
    style.map("Horizontal.TScale",
             background=[("active", "#1DB954")],
             troughcolor=[("active", "#444444")])
    
    style.configure("Vertical.TScrollbar", background="#333333", troughcolor="#181818", 
                   arrowcolor="#FFFFFF", borderwidth=0, relief="flat")
    style.map("Vertical.TScrollbar",
             background=[("active", "#1DB954"), ("pressed", "#168F41")],
             troughcolor=[("active", "#282828"), ("pressed", "#282828")])
    
    # Run the application
    root.mainloop()