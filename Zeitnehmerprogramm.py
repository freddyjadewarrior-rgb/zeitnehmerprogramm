import tkinter as tk
from tkinter import filedialog
import os
import pygame
from PIL import Image, ImageTk

# ==========================================
# INITIALISIERUNG & GLOBALE KONSTANTEN
# ==========================================

pygame.mixer.init()
SOUND_FILE = "/home/frederik/Downloads/Toy_Honk_Sound.wav"
DEFAULT_LOGO_PATH = "/home/frederik/jade warriors"


# ==========================================
# KLASSE: CONFIRMDIALOG (TOUCH-BESTÄTIGUNGSFENSTER)
# ==========================================
class ConfirmDialog(tk.Toplevel):
    def __init__(self, parent, title_text, message_text, callback):
        super().__init__(parent)
        self.title(title_text)
        self.geometry("450x250")
        self.configure(bg="#25d9e8")
        self.callback = callback
        
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text=message_text, font=("Arial", 16, "bold"), bg="#25d9e8", fg="black", wraplength=400, justify="center").pack(pady=30)
        
        btn_frame = tk.Frame(self, bg="#25d9e8")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Ja", command=self.yes_clicked, bg="#4CAF50", fg="white", font=("Arial", 16, "bold"), width=8, height=2).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Nein", command=self.no_clicked, bg="#f44336", fg="white", font=("Arial", 16, "bold"), width=8, height=2).pack(side="left", padx=20)

    def yes_clicked(self):
        self.destroy()
        self.callback(True)

    def no_clicked(self):
        self.destroy()
        self.callback(False)


# ==========================================
# KLASSE: SECTIONDIALOG (AUSWAHLLISTE ABSCHNITTE)
# ==========================================
class SectionDialog(tk.Toplevel):
    def __init__(self, parent, period_type, max_periods, current_period, callback):
        super().__init__(parent)
        self.title("Einstellungen Abschnitte")
        dialog_width = 850 if period_type == "Halbzeit" else 680
        dialog_height = 320 if period_type == "Halbzeit" else 250
        self.geometry(f"{dialog_width}x{dialog_height}")
        self.configure(bg="#25d9e8")
        self.callback = callback
        
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Abschnitt auswählen", font=("Arial", 20, "bold"), bg="#25d9e8", fg="black").pack(pady=15)
        
        if period_type == "Halbzeit":
            row1_frame = tk.Frame(self, bg="#25d9e8")
            row1_frame.pack(fill="both", expand=True, padx=20, pady=5)
            tk.Label(row1_frame, text="Drittel:", font=("Arial", 14, "bold"), bg="#25d9e8", width=12, anchor="w").pack(side="left")
            for p_num, p_text in [(1, "1. Drittel"), (2, "2. Drittel"), (3, "3. Drittel")]:
                btn = tk.Button(row1_frame, text=p_text, command=lambda n=p_num, t=p_text: self.select(n, t), bg="#ff7043", fg="black", font=("Arial", 12, "bold"), height=2)
                btn.pack(side="left", expand=True, fill="both", padx=3)

            row2_frame = tk.Frame(self, bg="#25d9e8")
            row2_frame.pack(fill="both", expand=True, padx=20, pady=5)
            tk.Label(row2_frame, text="Halbzeiten:", font=("Arial", 14, "bold"), bg="#25d9e8", width=12, anchor="w").pack(side="left")
            
            halves = [(1, "1. Halbzeit", [1, 2, 3]), (4, "2. Halbzeit", [4, 5, 6])]
            for p_num, p_text, active_list in halves:
                btn = tk.Button(row2_frame, text=p_text, command=lambda n=p_num, t=p_text: self.select(n, t), bg="#ff7043", fg="black", font=("Arial", 12, "bold"), height=2)
                btn.pack(side="left", expand=True, fill="both", padx=3)
        else:
            btn_frame = tk.Frame(self, bg="#25d9e8")
            btn_frame.pack(fill="both", expand=True, padx=20, pady=10)
            periods = [(1, "1. Drittel"), (2, "2. Drittel"), (3, "3. Drittel")]
            for p_num, p_text in periods:
                btn = tk.Button(btn_frame, text=p_text, command=lambda n=p_num, t=p_text: self.select(n, t), bg="#ff7043", fg="black", font=("Arial", 14, "bold"), height=3)
                btn.pack(side="left", expand=True, fill="both", padx=4)

    def select(self, num, text_val):
        self.destroy()
        self.callback(num, text_val)


# ==========================================
# KLASSE: GOALINPUTDIALOG (TOR-DATEN ERFASSEN)
# ==========================================
class GoalInputDialog(tk.Toplevel):
    def __init__(self, parent, team_name, current_time_str, callback):
        super().__init__(parent)
        self.title(f"Tor erfassen - {team_name}")
        self.geometry("420x280")
        self.configure(bg="#25d9e8")
        self.callback = callback
        
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text=f"Tor für {team_name}", font=("Arial", 18, "bold"), bg="#25d9e8", fg="black").pack(pady=15)
        
        form_frame = tk.Frame(self, bg="#25d9e8")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Spieler-Nummer:", font=("Arial", 14, "bold"), bg="#25d9e8").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.entry_num = tk.Entry(form_frame, font=("Arial", 14, "bold"), width=12, justify="center")
        self.entry_num.grid(row=0, column=1, padx=10, pady=8)
        self.entry_num.focus()

        tk.Label(form_frame, text="Zeitpunkt:", font=("Arial", 14, "bold"), bg="#25d9e8").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.entry_time = tk.Entry(form_frame, font=("Arial", 14, "bold"), width=12, justify="center")
        self.entry_time.insert(0, current_time_str)
        self.entry_time.grid(row=1, column=1, padx=10, pady=8)

        btn_frame = tk.Frame(self, bg="#25d9e8")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Bestätigen", command=self.save, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), width=10, height=1).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Abbrechen", command=self.destroy, bg="#f44336", fg="white", font=("Arial", 14, "bold"), width=10, height=1).pack(side="left", padx=10)

    def save(self):
        player_num = self.entry_num.get().strip()
        goal_time = self.entry_time.get().strip()
        self.destroy()
        self.callback(player_num, goal_time)


# ==========================================
# KLASSE: ROUNDEDBUTTON (EIGENE GUI-KOMPONENTE)
# ==========================================
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg="#ff7043", fg="black", font_size=16, radius=15):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.radius = radius
        self.text_val = text
        self.font_size = font_size

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Configure>", self._draw)

    def set_bg(self, color):
        self.bg_color = color
        self._draw()

    def _draw(self, event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        
        if w < 10 or h < 10:
            return
            
        r = self.radius
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=self.bg_color, outline="")
        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, fill=self.bg_color, outline="")
        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, fill=self.bg_color, outline="")
        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, fill=self.bg_color, outline="")
        
        self.create_rectangle(r, 0, w-r, h, fill=self.bg_color, outline="")
        self.create_rectangle(0, r, w, h-r, fill=self.bg_color, outline="")
        
        self.create_text(w//2, h//2, text=self.text_val, fill=self.fg_color, font=("Arial", self.font_size, "bold"))


# ==========================================
# KLASSE: ZUSCHAUERANZEIGE (SEKUNDÄRES FENSTER)
# ==========================================
class ZuschauerAnzeige(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Zuschauer Anzeige")
        self.geometry("1024x600")
        self.configure(bg="#111111")

        self.protocol("WM_DELETE_WINDOW", self.ask_close)

        self.img_home_tk = None
        self.img_guest_tk = None
        self.img_home_end_tk = None
        self.img_guest_end_tk = None

        self.viewer_pen_labels_home = []
        self.viewer_pen_labels_guest = []

        self.build_ui()

    def ask_close(self):
        ConfirmDialog(self, "Zuschaueranzeige", "Möchtest du die Zuschaueranzeige wirklich schließen?", lambda res: self.destroy() if res else None)

    def build_ui(self):
        self.main_container = tk.Frame(self, bg="#111111")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # HEIM
        home_frame = tk.Frame(self.main_container, bg="#111111")
        home_frame.place(relx=0.0, rely=0.0, anchor="nw")

        header_home = tk.Frame(home_frame, bg="#111111")
        header_home.pack(anchor="w")

        self.lbl_logo_home = tk.Label(header_home, bg="#111111")
        self.lbl_logo_home.pack(side="left", padx=(0, 10))

        self.lbl_team_home = tk.Label(header_home, text="HEIM", font=("Arial", 38, "bold"), fg="#ffffff", bg="#111111")
        self.lbl_team_home.pack(side="left")

        z_home_score_box = tk.Frame(home_frame, bg="#111111")
        z_home_score_box.pack(anchor="w")
        self.lbl_score_home = tk.Label(z_home_score_box, text="0", font=("Arial", 85, "bold"), fg="#00ff00", bg="#111111")
        self.lbl_score_home.pack(side="left")

        self.lbl_pen_title_home = tk.Label(home_frame, text="STRAFEN", font=("Arial", 14, "bold"), fg="#aaaaaa", bg="#111111")
        self.frame_pen_home = tk.Frame(home_frame, bg="#111111")

        # GAST
        guest_frame = tk.Frame(self.main_container, bg="#111111")
        guest_frame.place(relx=1.0, rely=0.0, anchor="ne")

        header_guest = tk.Frame(guest_frame, bg="#111111")
        header_guest.pack(anchor="e")

        self.lbl_team_guest = tk.Label(header_guest, text="GAST", font=("Arial", 38, "bold"), fg="#ffffff", bg="#111111")
        self.lbl_team_guest.pack(side="left")

        self.lbl_logo_guest = tk.Label(header_guest, bg="#111111")
        self.lbl_logo_guest.pack(side="left", padx=(10, 0))

        z_guest_score_box = tk.Frame(guest_frame, bg="#111111")
        z_guest_score_box.pack(anchor="e")
        self.lbl_score_guest = tk.Label(z_guest_score_box, text="0", font=("Arial", 85, "bold"), fg="#00ff00", bg="#111111")
        self.lbl_score_guest.pack(side="left")

        self.lbl_pen_title_guest = tk.Label(guest_frame, text="STRAFEN", font=("Arial", 14, "bold"), fg="#aaaaaa", bg="#111111")
        self.frame_pen_guest = tk.Frame(guest_frame, bg="#111111")

        # MITTE
        timer_frame = tk.Frame(self.main_container, bg="#111111")
        timer_frame.place(relx=0.5, rely=0.4, anchor="center")

        self.lbl_period = tk.Label(timer_frame, text="1. Halbzeit", font=("Arial", 24, "bold"), fg="#00e5ff", bg="#111111")
        self.lbl_period.pack(pady=(0, 5))

        self.lbl_clock = tk.Label(timer_frame, text="00:00", font=("Arial", 100, "bold"), fg="#ffcc00", bg="#111111")
        self.lbl_clock.pack()

        self.lbl_timeout = tk.Label(timer_frame, text="", font=("Arial", 30, "bold"), fg="#ff3333", bg="#111111")
        self.lbl_timeout.pack(pady=(5, 0))

        self.frame_pause = tk.Frame(timer_frame, bg="#111111")
        self.lbl_pause_title = tk.Label(self.frame_pause, text="PAUSE", font=("Arial", 45, "bold"), fg="#ff0055", bg="#111111")
        self.lbl_pause_title.pack()
        self.lbl_pause_clock = tk.Label(self.frame_pause, text="00:00", font=("Arial", 90, "bold"), fg="#ffffff", bg="#111111")
        self.lbl_pause_clock.pack()

        # ENDSCHIRM
        self.end_container = tk.Frame(self, bg="#111111")

        self.lbl_winner = tk.Label(self.end_container, text="", font=("Arial", 42, "bold"), fg="#ffcc00", bg="#111111")
        self.lbl_winner.pack(pady=(20, 10))

        self.lbl_final_score = tk.Label(self.end_container, text="", font=("Arial", 110, "bold"), fg="#00ff00", bg="#111111")
        self.lbl_final_score.pack(pady=(0, 20))

        teams_box = tk.Frame(self.end_container, bg="#111111")
        teams_box.pack(fill="x", expand=True, padx=60)

        self.lbl_end_logo_home = tk.Label(teams_box, bg="#111111")
        self.lbl_end_logo_home.pack(side="left", anchor="w")

        self.lbl_end_logo_guest = tk.Label(teams_box, bg="#111111")
        self.lbl_end_logo_guest.pack(side="right", anchor="e")

    def update_logos(self, img_home, img_guest):
        if img_home:
            img_resized = img_home.resize((80, 80), Image.Resampling.LANCZOS)
            self.img_home_tk = ImageTk.PhotoImage(img_resized)
            self.lbl_logo_home.config(image=self.img_home_tk)

            img_end_resized = img_home.resize((180, 180), Image.Resampling.LANCZOS)
            self.img_home_end_tk = ImageTk.PhotoImage(img_end_resized)
            self.lbl_end_logo_home.config(image=self.img_home_end_tk)
        else:
            self.lbl_logo_home.config(image="")
            self.lbl_end_logo_home.config(image="")

        if img_guest:
            img_resized = img_guest.resize((80, 80), Image.Resampling.LANCZOS)
            self.img_guest_tk = ImageTk.PhotoImage(img_resized)
            self.lbl_logo_guest.config(image=self.img_guest_tk)

            img_end_resized = img_guest.resize((180, 180), Image.Resampling.LANCZOS)
            self.img_guest_end_tk = ImageTk.PhotoImage(img_end_resized)
            self.lbl_end_logo_guest.config(image=self.img_guest_end_tk)
        else:
            self.lbl_logo_guest.config(image="")
            self.lbl_end_logo_guest.config(image="")

    def update_display(self, time_str, score_home, score_guest, pen_home, pen_guest, name_home, name_guest, period_str, timeout_sec, pause_sec, blink_state, is_game_over):
        name_h = name_home.strip() if name_home.strip() != "" else "HEIM"
        name_g = name_guest.strip() if name_guest.strip() != "" else "GAST"

        if is_game_over:
            self.main_container.pack_forget()
            self.end_container.pack(fill="both", expand=True)

            if score_home > score_guest:
                self.lbl_winner.config(text=f"DIE {name_h.upper()} HABEN GEWONNEN!")
            elif score_guest > score_home:
                self.lbl_winner.config(text=f"DIE {name_g.upper()} HABEN GEWONNEN!")
            else:
                self.lbl_winner.config(text="UNENTSCHIEDEN!")

            self.lbl_final_score.config(text=f"{score_home} : {score_guest}")
            return

        self.end_container.pack_forget()
        self.main_container.pack(fill="both", expand=True, padx=30, pady=20)

        self.lbl_clock.config(text=time_str)
        self.lbl_score_home.config(text=str(score_home))
        self.lbl_score_guest.config(text=str(score_guest))
        self.lbl_period.config(text=period_str)
        
        self.lbl_team_home.config(text=name_h)
        self.lbl_team_guest.config(text=name_g)

        if timeout_sec > 0:
            self.lbl_timeout.config(text=f"TIME-OUT: {timeout_sec}s")
        else:
            self.lbl_timeout.config(text="")

        if pause_sec > 0:
            m = pause_sec // 60
            s = pause_sec % 60
            self.lbl_clock.pack_forget()
            self.frame_pause.pack()
            self.lbl_pause_clock.config(text=f"{m:02d}:{s:02d}")
        else:
            self.frame_pause.pack_forget()
            self.lbl_clock.pack()

        # STRAFEN HEIM
        active_home_pens = [p for p in pen_home if p["seconds"] > 0]
        if active_home_pens:
            self.lbl_pen_title_home.pack(anchor="w", pady=(10, 2))
            self.frame_pen_home.pack(anchor="w")
            
            if len(self.viewer_pen_labels_home) != len(active_home_pens):
                for w in self.frame_pen_home.winfo_children():
                    w.destroy()
                self.viewer_pen_labels_home = []
                for _ in active_home_pens:
                    lbl = tk.Label(self.frame_pen_home, font=("Arial", 26, "bold"), fg="#ffffff", bg="#ff3333", padx=15, pady=2)
                    lbl.pack(anchor="w", pady=3)
                    self.viewer_pen_labels_home.append(lbl)

            for lbl, p in zip(self.viewer_pen_labels_home, active_home_pens):
                sec = p["seconds"]
                m = sec // 60
                s = sec % 60
                lbl.config(text=f"{m:02d}:{s:02d}")
                
                if sec <= 20:
                    if blink_state:
                        lbl.config(bg="#ff3333", fg="#ffffff")
                    else:
                        lbl.config(bg="#111111", fg="#ff3333")
                else:
                    lbl.config(bg="#ff3333", fg="#ffffff")
        else:
            self.lbl_pen_title_home.pack_forget()
            self.frame_pen_home.pack_forget()
            for w in self.frame_pen_home.winfo_children():
                w.destroy()
            self.viewer_pen_labels_home = []

        # STRAFEN GAST
        active_guest_pens = [p for p in pen_guest if p["seconds"] > 0]
        if active_guest_pens:
            self.lbl_pen_title_guest.pack(anchor="e", pady=(10, 2))
            self.frame_pen_guest.pack(anchor="e")
            
            if len(self.viewer_pen_labels_guest) != len(active_guest_pens):
                for w in self.frame_pen_guest.winfo_children():
                    w.destroy()
                self.viewer_pen_labels_guest = []
                for _ in active_guest_pens:
                    lbl = tk.Label(self.frame_pen_guest, font=("Arial", 26, "bold"), fg="#ffffff", bg="#ff3333", padx=15, pady=2)
                    lbl.pack(anchor="e", pady=3)
                    self.viewer_pen_labels_guest.append(lbl)

            for lbl, p in zip(self.viewer_pen_labels_guest, active_guest_pens):
                sec = p["seconds"]
                m = sec // 60
                s = sec % 60
                lbl.config(text=f"{m:02d}:{s:02d}")

                if sec <= 20:
                    if blink_state:
                        lbl.config(bg="#ff3333", fg="#ffffff")
                    else:
                        lbl.config(bg="#111111", fg="#ff3333")
                else:
                    lbl.config(bg="#ff3333", fg="#ffffff")
        else:
            self.lbl_pen_title_guest.pack_forget()
            self.frame_pen_guest.pack_forget()
            for w in self.frame_pen_guest.winfo_children():
                w.destroy()
            self.viewer_pen_labels_guest = []


# ==========================================
# KLASSE: ZEITNEHMER (BEDIENFELD / STEUERUNG)
# ==========================================
class Zeitnehmer:
    def __init__(self, root, minutes, period_type, rule_90, record_numbers, name_home, name_guest, img_home, img_guest):
        self.root = root
        self.root.title("Zeitnehmer Dashboard (Bedienung)")
        self.root.geometry("1280x780")
        self.root.configure(bg="#25d9e8")

        self.initial_minutes = minutes
        self.remaining = minutes * 60
        self.elapsed = 0
        self.running = False
        self.after_id = None
        self.blink_state = False

        self.name_home = name_home
        self.name_guest = name_guest

        self.pil_img_home = img_home
        self.pil_img_guest = img_guest
        self.prev_home_tk = None
        self.prev_guest_tk = None

        self.rule_90_active = rule_90
        self.rule_90_remaining = 90
        self.record_numbers = record_numbers  

        self.timeout_remaining = 0
        self.pause_remaining = 0
        self.pause_running = False

        self.period_type = period_type
        self.current_period = 1
        self.max_periods = 6 if period_type == "Halbzeit" else 3
        self.period_display_text = "1. Halbzeit" if period_type == "Halbzeit" else "1. Drittel"
        self.is_game_over = False

        self.score_home = 0
        self.score_guest = 0

        self.goals = []  # Speichert Tor-Daten: {"team": 'home'/'guest', "player": nr, "time": str}

        self.penalties_home = []
        self.penalties_guest = []

        self.period_states = {}
        self.drag_start_y = 0

        self.build_ui()

        self.zuschauer_win = ZuschauerAnzeige(self.root)
        if self.pil_img_home or self.pil_img_guest:
            self.zuschauer_win.update_logos(self.pil_img_home, self.pil_img_guest)
        
        self.tick()

    def save_current_state(self):
        self.period_states[self.current_period] = {
            "remaining": self.remaining,
            "elapsed": self.elapsed,
            "display_text": self.period_display_text,
            "penalties_home": [{"seconds": p["seconds"]} for p in self.penalties_home],
            "penalties_guest": [{"seconds": p["seconds"]} for p in self.penalties_guest]
        }

    def load_state(self, period_num):
        for p in self.penalties_home:
            p["frame"].destroy()
        for p in self.penalties_guest:
            p["frame"].destroy()
        self.penalties_home = []
        self.penalties_guest = []

        if period_num in self.period_states:
            data = self.period_states[period_num]
            self.remaining = data["remaining"]
            self.elapsed = data["elapsed"]
            self.period_display_text = data.get("display_text", self.period_display_text)
            for p_data in data["penalties_home"]:
                self.add_penalty_with_seconds('home', p_data["seconds"])
            for p_data in data["penalties_guest"]:
                self.add_penalty_with_seconds('guest', p_data["seconds"])
        else:
            self.remaining = self.initial_minutes * 60
            self.elapsed = 0

    def setup_scroll_events_score(self, widget, team):
        widget.bind("<Button-4>", lambda e: self.change_score(team, 1))
        widget.bind("<Button-5>", lambda e: self.change_score(team, -1))
        widget.bind("<MouseWheel>", lambda e: self.handle_mousewheel_score(e, team))
        widget.bind("<Button-1>", self.on_touch_start)
        widget.bind("<B1-Motion>", lambda e: self.on_touch_drag_score(e, team))

    def handle_mousewheel_score(self, event, team):
        if event.delta > 0:
            self.change_score(team, 1)
        elif event.delta < 0:
            self.change_score(team, -1)

    def on_touch_drag_score(self, event, team):
        diff_y = self.drag_start_y - event.y
        if abs(diff_y) > 25:
            if diff_y > 0:
                self.change_score(team, 1)
            else:
                self.change_score(team, -1)
            self.drag_start_y = event.y

    def setup_scroll_events_penalty(self, widget, team, pen_data):
        widget.bind("<Button-4>", lambda e: self.change_penalty_time(team, pen_data, 1))
        widget.bind("<Button-5>", lambda e: self.change_penalty_time(team, pen_data, -1))
        widget.bind("<MouseWheel>", lambda e: self.handle_mousewheel_penalty(e, team, pen_data))
        widget.bind("<Button-1>", self.on_touch_start)
        widget.bind("<B1-Motion>", lambda e: self.on_touch_drag_penalty(e, team, pen_data))

    def handle_mousewheel_penalty(self, event, team, pen_data):
        if event.delta > 0:
            self.change_penalty_time(team, pen_data, 1)
        elif event.delta < 0:
            self.change_penalty_time(team, pen_data, -1)

    def on_touch_drag_penalty(self, event, team, pen_data):
        diff_y = self.drag_start_y - event.y
        if abs(diff_y) > 15:
            if diff_y > 0:
                self.change_penalty_time(team, pen_data, 1)
            else:
                self.change_penalty_time(team, pen_data, -1)
            self.drag_start_y = event.y

    def on_touch_start(self, event):
        self.drag_start_y = event.y

    def build_ui(self):
        main_container = tk.Frame(self.root, bg="#25d9e8")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        btn_back_setup = tk.Button(main_container, text="← Zurück zur Auswahl", command=self.confirm_back_to_setup, bg="#ff5722", fg="white", font=("Arial", 12, "bold"), height=2, padx=10)
        btn_back_setup.place(relx=0.0, rely=0.96, anchor="sw")

        # HEIM
        home_frame = tk.Frame(main_container, bg="#25d9e8")
        home_frame.place(relx=0.0, rely=0.0, anchor="nw")

        h_name_box = tk.Frame(home_frame, bg="#25d9e8")
        h_name_box.pack(anchor="w", pady=(0, 5))

        self.lbl_home_title = tk.Label(h_name_box, text=self.name_home, font=("Arial", 18, "bold"), bg="#25d9e8")
        self.lbl_home_title.pack(side="left")

        self.lbl_prev_home = tk.Label(h_name_box, bg="#25d9e8")
        self.lbl_prev_home.pack(side="left", padx=5)

        if self.pil_img_home:
            thumb = self.pil_img_home.resize((35, 35), Image.Resampling.LANCZOS)
            self.prev_home_tk = ImageTk.PhotoImage(thumb)
            self.lbl_prev_home.config(image=self.prev_home_tk)

        home_score_box = tk.Frame(home_frame, bg="#25d9e8")
        home_score_box.pack(anchor="w")
        
        tk.Label(home_score_box, text="Tore:", font=("Arial", 22, "bold"), bg="#25d9e8").pack(side="left", padx=(0, 5))
        self.home_score = tk.Label(home_score_box, text="0", font=("Arial", 45, "bold"), bg="#25d9e8")
        self.home_score.pack(side="left")

        self.setup_scroll_events_score(self.home_score, 'home')
        self.setup_scroll_events_score(home_score_box, 'home')

        self.create_score_buttons(home_frame, lambda: self.change_score('home', 1), lambda: self.change_score('home', -1)).pack(anchor="w", pady=2)

        tk.Label(home_frame, text="Strafen", font=("Arial", 14, "bold"), bg="#25d9e8").pack(anchor="w", pady=(12, 2))
        h_pen_btn = tk.Frame(home_frame, bg="#25d9e8")
        h_pen_btn.pack(anchor="w", pady=2)
        tk.Button(h_pen_btn, text="+2m", command=lambda: self.add_penalty('home', 2), bg="#ff9800", fg="white", font=("Arial", 14, "bold"), width=5, height=2).pack(side="left", padx=3)
        tk.Button(h_pen_btn, text="+5m", command=lambda: self.add_penalty('home', 5), bg="#ff9800", fg="white", font=("Arial", 14, "bold"), width=5, height=2).pack(side="left", padx=3)
        tk.Button(h_pen_btn, text="+10m", command=lambda: self.add_penalty('home', 10), bg="#ff9800", fg="white", font=("Arial", 14, "bold"), width=5, height=2).pack(side="left", padx=3)

        self.frame_penalties_home = tk.Frame(home_frame, bg="#25d9e8")
        self.frame_penalties_home.pack(anchor="w", pady=5)

        # GAST
        guest_frame = tk.Frame(main_container, bg="#25d9e8")
        guest_frame.place(relx=1.0, rely=0.0, anchor="ne")

        g_name_box = tk.Frame(guest_frame, bg="#25d9e8")
        g_name_box.pack(anchor="e", pady=(0, 5))

        self.lbl_prev_guest = tk.Label(g_name_box, bg="#25d9e8")
        self.lbl_prev_guest.pack(side="left", padx=5)

        if self.pil_img_guest:
            thumb = self.pil_img_guest.resize((35, 35), Image.Resampling.LANCZOS)
            self.prev_guest_tk = ImageTk.PhotoImage(thumb)
            self.lbl_prev_guest.config(image=self.prev_guest_tk)

        self.lbl_guest_title = tk.Label(g_name_box, text=self.name_guest, font=("Arial", 18, "bold"), bg="#25d9e8")
        self.lbl_guest_title.pack(side="left")

        guest_score_box = tk.Frame(guest_frame, bg="#25d9e8")
        guest_score_box.pack(anchor="e")
        
        tk.Label(guest_score_box, text="Tore:", font=("Arial", 22, "bold"), bg="#25d9e8").pack(side="left", padx=(0, 5))
        self.guest_score = tk.Label(guest_score_box, text="0", font=("Arial", 45, "bold"), bg="#25d9e8")
        self.guest_score.pack(side="left")

        self.setup_scroll_events_score(self.guest_score, 'guest')
        self.setup_scroll_events_score(guest_score_box, 'guest')

        self.create_score_buttons(guest_frame, lambda: self.change_score('guest', 1), lambda: self.change_score('guest', -1)).pack(anchor="e", pady=2)

        tk.Label(guest_frame, text="Strafen", font=("Arial", 14, "bold"), bg="#25d9e8").pack(anchor="e", pady=(12, 2))
        g_pen_btn = tk.Frame(guest_frame, bg="#25d9e8")
        g_pen_btn.pack(anchor="e", pady=2)
        tk.Button(g_pen_btn, text="+2m", command=lambda: self.add_penalty('guest', 2), bg="#ff9800", fg="white", font=("Arial", 14, "bold"), width=5, height=2).pack(side="left", padx=3)
        tk.Button(g_pen_btn, text="+5m", command=lambda: self.add_penalty('guest', 5), bg="#ff9800", fg="white", font=("Arial", 14, "bold"), width=5, height=2).pack(side="left", padx=3)
        tk.Button(g_pen_btn, text="+10m", command=lambda: self.add_penalty('guest', 10), bg="#ff9800", fg="white", font=("Arial", 14, "bold"), width=5, height=2).pack(side="left", padx=3)

        self.frame_penalties_guest = tk.Frame(guest_frame, bg="#25d9e8")
        self.frame_penalties_guest.pack(anchor="e", pady=5)

        # MITTE (NORMALER SPIELBETRIEB)
        self.timer_frame = tk.Frame(main_container, bg="#25d9e8")
        self.timer_frame.place(relx=0.5, rely=0.38, anchor="center")

        self.lbl_period = tk.Label(self.timer_frame, text=self.get_period_string(), font=("Arial", 18, "bold"), bg="#25d9e8", fg="#004d40")
        self.lbl_period.pack()

        sections_btn_frame = tk.Frame(self.timer_frame, bg="#25d9e8")
        sections_btn_frame.pack(pady=(2, 6))

        self.btn_halbzeiten = tk.Button(sections_btn_frame, text="Einstellungen Abschnitte", command=lambda: self.open_section_menu("Halbzeit"), bg="#00897b", fg="white", font=("Arial", 11, "bold"), height=2, padx=6)
        self.btn_halbzeiten.pack(padx=10)

        self.clock_elapsed = tk.Label(self.timer_frame, text=self.format_time(self.elapsed), font=("Arial", 65, "bold"), bg="#25d9e8", fg="#000000")
        self.clock_elapsed.pack()

        self.lbl_90_status = tk.Label(self.timer_frame, text="", font=("Arial", 11, "bold"), bg="#25d9e8", fg="#d32f2f")
        self.lbl_90_status.pack()

        sec_btn_frame = tk.Frame(self.timer_frame, bg="#25d9e8")
        sec_btn_frame.pack(pady=4)
        tk.Button(sec_btn_frame, text="+1s", command=lambda: self.change_remaining(1), font=("Arial", 14, "bold"), width=6, height=1, bg="#ffffff").pack(side="left", padx=5)
        tk.Button(sec_btn_frame, text="-1s", command=lambda: self.change_remaining(-1), font=("Arial", 14, "bold"), width=6, height=1, bg="#ffffff").pack(side="left", padx=5)

        btn_frame = tk.Frame(self.timer_frame, bg="#25d9e8")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Start", command=self.start_timer, bg="#4CAF50", fg="white", font=("Arial", 18, "bold"), width=10, height=2).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Stopp", command=self.stop_timer, bg="#f44336", fg="white", font=("Arial", 18, "bold"), width=10, height=2).pack(side="left", padx=6)

        timeout_frame = tk.Frame(self.timer_frame, bg="#25d9e8")
        timeout_frame.pack(pady=(4, 2))
        tk.Button(timeout_frame, text="Time-Out (30s)", command=self.start_timeout, bg="#ff5722", fg="white", font=("Arial", 14, "bold"), width=16, height=2).pack()
        self.lbl_timeout_status = tk.Label(timeout_frame, text="", font=("Arial", 12, "bold"), bg="#25d9e8", fg="#d32f2f")
        self.lbl_timeout_status.pack()

        remaining_frame = tk.Frame(self.timer_frame, bg="#25d9e8")
        remaining_frame.pack(pady=(4, 0))
        tk.Label(remaining_frame, text="Verbleibende Zeit:", font=("Arial", 10, "bold"), bg="#25d9e8", fg="#333333").pack()
        self.clock = tk.Label(remaining_frame, text=self.format_time(self.remaining), font=("Arial", 22, "bold"), bg="#25d9e8", fg="#004d40")
        self.clock.pack()

        # MITTE PAUSEN-TORANZEIGE (wird nur während der Pause eingeblendet)
        self.pause_goals_frame = tk.Frame(main_container, bg="#25d9e8")
        
        self.frame_goals_home = tk.Frame(self.pause_goals_frame, bg="#25d9e8")
        self.frame_goals_home.pack(side="left", fill="both", expand=True, padx=20)

        self.frame_goals_guest = tk.Frame(self.pause_goals_frame, bg="#25d9e8")
        self.frame_goals_guest.pack(side="right", fill="both", expand=True, padx=20)

        # UNTERER RAND: PAUSENZEIT
        self.pause_box = tk.LabelFrame(main_container, text=" Pausenzeit Steuerfeld ", font=("Arial", 12, "bold"), bg="#25d9e8", fg="#004d40", bd=2)

        p_inner = tk.Frame(self.pause_box, bg="#25d9e8")
        p_inner.pack(pady=8)

        tk.Button(p_inner, text="3 Min Pause", command=lambda: self.start_pause(3), bg="#9c27b0", fg="white", font=("Arial", 13, "bold"), height=2, padx=10).pack(side="left", padx=8)
        tk.Button(p_inner, text="5 Min Pause", command=lambda: self.start_pause(5), bg="#9c27b0", fg="white", font=("Arial", 13, "bold"), height=2, padx=10).pack(side="left", padx=8)
        tk.Button(p_inner, text="10 Min Pause", command=lambda: self.start_pause(10), bg="#9c27b0", fg="white", font=("Arial", 13, "bold"), height=2, padx=10).pack(side="left", padx=8)

        tk.Label(p_inner, text="Oder Min:", font=("Arial", 13, "bold"), bg="#25d9e8").pack(side="left", padx=(15, 2))
        self.entry_pause_custom = tk.Entry(p_inner, font=("Arial", 14, "bold"), width=4, justify="center")
        self.entry_pause_custom.insert(0, "15")
        self.entry_pause_custom.pack(side="left", padx=2, ipady=6)
        
        tk.Button(p_inner, text="Start", command=self.start_custom_pause, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2, width=6).pack(side="left", padx=6)
        tk.Button(p_inner, text="Pause beenden", command=self.stop_pause, bg="#d32f2f", fg="white", font=("Arial", 12, "bold"), height=2, padx=8).pack(side="left", padx=(10, 6))

        self.lbl_pause_status = tk.Label(p_inner, text="", font=("Arial", 14, "bold"), bg="#25d9e8", fg="#9c27b0")
        self.lbl_pause_status.pack(side="left", padx=10)

    def confirm_back_to_setup(self):
        self.stop_timer()
        ConfirmDialog(self.root, "Zurück zur Auswahl", "Möchtest du wirklich zur Auswahl zurückkehren?", lambda res: self.return_to_setup() if res else None)

    def return_to_setup(self):
        if hasattr(self, 'zuschauer_win') and self.zuschauer_win.winfo_exists():
            self.zuschauer_win.destroy()
        for widget in self.root.winfo_children():
            widget.destroy()
        Auswahl(self.root)

    def play_honk_sound(self):
        if os.path.exists(SOUND_FILE):
            pygame.mixer.music.load(SOUND_FILE)
            pygame.mixer.music.play()

    def start_timeout(self):
        self.stop_timer()
        self.timeout_remaining = 30
        self.lbl_timeout_status.config(text=f"Time-Out: {self.timeout_remaining}s")
        self.update_zuschauer()

    def start_pause(self, minutes):
        self.stop_timer()
        self.pause_remaining = minutes * 60
        self.pause_running = True
        self.update_pause_label()
        self.update_zuschauer()

    def start_custom_pause(self):
        try:
            val = int(self.entry_pause_custom.get())
            if val > 0:
                self.start_pause(val)
        except ValueError:
            pass

    def stop_pause(self):
        self.pause_running = False
        self.pause_remaining = 0
        self.lbl_pause_status.config(text="")
        self.pause_goals_frame.place_forget()
        self.timer_frame.place(relx=0.5, rely=0.38, anchor="center")
        self.pause_box.place_forget()
        self.next_period()

    def update_pause_label(self):
        if self.pause_remaining > 0:
            m = self.pause_remaining // 60
            s = self.pause_remaining % 60
            self.lbl_pause_status.config(text=f"Pause läuft: {m:02d}:{s:02d}")
        else:
            self.lbl_pause_status.config(text="")

    def get_period_string(self):
        return self.period_display_text

    def open_section_menu(self, period_type=None):
        if period_type is not None:
            self.period_type = period_type
            self.max_periods = 6 if period_type == "Halbzeit" else 3
            if self.period_type == "Drittel" and self.current_period > 3:
                self.current_period = 1
                self.period_display_text = "1. Drittel"
            self.lbl_period.config(text=self.get_period_string())
        SectionDialog(self.root, self.period_type, self.max_periods, self.current_period, self.jump_to_period)

    def jump_to_period(self, period_num, text_val):
        if period_num == self.current_period and text_val == self.period_display_text:
            return
        self.save_current_state()
        self.current_period = period_num
        self.period_display_text = text_val
        self.is_game_over = False
        self.lbl_period.config(text=self.get_period_string())
        self.stop_timer()
        self.load_state(period_num)
        self.clock.config(text=self.format_time(self.remaining))
        self.clock_elapsed.config(text=self.format_time(self.elapsed))
        self.update_zuschauer()

    def next_period(self):
        if self.current_period < self.max_periods:
            self.save_current_state()
            self.current_period += 1
            if self.period_type == "Halbzeit":
                if self.current_period <= 3:
                    self.period_display_text = f"{self.current_period}. Drittel"
                elif self.current_period == 4:
                    self.period_display_text = "2. Halbzeit"
                else:
                    self.period_display_text = f"{self.current_period - 3}. Drittel"
            else:
                self.period_display_text = f"{self.current_period}. Drittel"

            self.is_game_over = False
            self.lbl_period.config(text=self.get_period_string())
            self.stop_timer()
            self.load_state(self.current_period)
            if self.current_period not in self.period_states:
                self.remaining = self.initial_minutes * 60
                self.elapsed = 0
            self.clock.config(text=self.format_time(self.remaining))
            self.clock_elapsed.config(text=self.format_time(self.elapsed))
            self.update_zuschauer()

    def create_score_buttons(self, parent, add_cmd, sub_cmd):
        f = tk.Frame(parent, bg="#25d9e8")
        tk.Button(f, text="+", command=add_cmd, font=("Arial", 22, "bold"), width=4, height=1, bg="#ffffff").pack(side="left", padx=4)
        tk.Button(f, text="-", command=sub_cmd, font=("Arial", 22, "bold"), width=4, height=1, bg="#ffffff").pack(side="left", padx=4)
        return f

    def change_remaining(self, seconds):
        old_remaining = self.remaining
        self.remaining = max(0, self.remaining + seconds)
        
        actual_diff = self.remaining - old_remaining
        self.elapsed = max(0, self.elapsed - actual_diff)

        if self.remaining > 0 and self.is_game_over:
            self.is_game_over = False
            
        time_str = self.format_time(self.remaining)
        self.clock.config(text=time_str)
        self.clock_elapsed.config(text=self.format_time(self.elapsed))
        self.update_zuschauer()

    def change_score(self, team, amount):
        if amount > 0 and self.record_numbers:
            team_name = self.name_home if team == 'home' else self.name_guest
            current_time_str = self.format_time(self.elapsed)
            GoalInputDialog(self.root, team_name, current_time_str, lambda p_num, g_time: self.apply_score_with_data(team, amount, p_num, g_time))
        else:
            self.apply_score_direct(team, amount)

    def apply_score_direct(self, team, amount):
        if team == 'home':
            self.score_home = max(0, self.score_home + amount)
            self.home_score.config(text=str(self.score_home))
        else:
            self.score_guest = max(0, self.score_guest + amount)
            self.guest_score.config(text=str(self.score_guest))
        self.update_zuschauer()

    def apply_score_with_data(self, team, amount, player_num, goal_time):
        if player_num:
            self.goals.append({
                "team": team,
                "player": player_num,
                "time": goal_time
            })
        self.apply_score_direct(team, amount)

    def update_pause_goals_display(self):
        for w in self.frame_goals_home.winfo_children():
            w.destroy()
        for w in self.frame_goals_guest.winfo_children():
            w.destroy()

        tk.Label(self.frame_goals_home, text=f"Tore {self.name_home}:", font=("Arial", 16, "bold"), bg="#25d9e8", fg="#004d40").pack(anchor="w", pady=(0, 5))
        tk.Label(self.frame_goals_guest, text=f"Tore {self.name_guest}:", font=("Arial", 16, "bold"), bg="#25d9e8", fg="#004d40").pack(anchor="e", pady=(0, 5))

        for g in self.goals:
            txt = f"Nr. {g['player']} - {g['time']} Min."
            if g['team'] == 'home':
                tk.Label(self.frame_goals_home, text=txt, font=("Arial", 14, "bold"), bg="#25d9e8", fg="black").pack(anchor="w", pady=2)
            else:
                tk.Label(self.frame_goals_guest, text=txt, font=("Arial", 14, "bold"), bg="#25d9e8", fg="black").pack(anchor="e", pady=2)

    def add_penalty(self, team, minutes):
        self.add_penalty_with_seconds(team, minutes * 60)

    def add_penalty_with_seconds(self, team, seconds):
        target_list = self.penalties_home if team == 'home' else self.penalties_guest
        target_frame = self.frame_penalties_home if team == 'home' else self.frame_penalties_guest

        pen_row = tk.Frame(target_frame, bg="#25d9e8")
        pen_row.pack(pady=2, anchor="w" if team == 'home' else "e")

        lbl = tk.Label(pen_row, text=self.format_time(seconds), font=("Arial", 18, "bold"), bg="#000000", fg="#ffeb3b", padx=10, pady=2)
        lbl.pack(side="left")

        pen_data = {"seconds": seconds, "label": lbl, "frame": pen_row}

        btn_cancel = tk.Button(pen_row, text="✕", font=("Arial", 12, "bold"), bg="#f44336", fg="white", 
                               command=lambda p=pen_data: self.remove_penalty(team, p), width=2)
        btn_cancel.pack(side="left", padx=4)

        self.setup_scroll_events_penalty(lbl, team, pen_data)

        target_list.append(pen_data)
        self.update_zuschauer()

    def change_penalty_time(self, team, pen_data, seconds_change):
        pen_data["seconds"] += seconds_change
        if pen_data["seconds"] <= 0:
            self.remove_penalty(team, pen_data)
        else:
            pen_data["label"].config(text=self.format_time(pen_data["seconds"]))
            self.update_zuschauer()

    def remove_penalty(self, team, pen_data):
        target_list = self.penalties_home if team == 'home' else self.penalties_guest
        if pen_data in target_list:
            pen_data["frame"].destroy()
            target_list.remove(pen_data)
            self.update_zuschauer()

    def start_timer(self):
        if self.remaining > 0:
            self.running = True
            self.is_game_over = False
            if self.rule_90_active:
                self.rule_90_remaining = 90
                self.lbl_90_status.config(text="90s-Regel: 90s")

            if self.pause_running:
                self.stop_pause()

    def stop_timer(self):
        self.running = False
        if self.rule_90_active:
            self.rule_90_remaining = 90
            self.lbl_90_status.config(text="90s-Regel: Inaktiv")

    def update_zuschauer(self):
        if hasattr(self, 'zuschauer_win') and self.zuschauer_win.winfo_exists():
            self.zuschauer_win.update_display(
                self.format_time(self.remaining),
                self.score_home,
                self.score_guest,
                self.penalties_home,
                self.penalties_guest,
                self.name_home,
                self.name_guest,
                self.get_period_string(),
                self.timeout_remaining,
                self.pause_remaining,
                self.blink_state,
                self.is_game_over
            )

    def tick(self):
        self.blink_state = not self.blink_state

        if self.pause_running or self.remaining == 0:
            self.pause_box.place(relx=0.5, rely=0.94, anchor="s", relwidth=0.95)
            self.timer_frame.place_forget()
            self.pause_goals_frame.place(relx=0.5, rely=0.38, anchor="center", relwidth=0.55, relheight=0.45)
            self.update_pause_goals_display()
        else:
            self.pause_box.place_forget()
            self.pause_goals_frame.place_forget()
            self.timer_frame.place(relx=0.5, rely=0.38, anchor="center")

        if 0 < self.remaining <= 120:
            self.clock.config(fg="#d32f2f")
        else:
            self.clock.config(fg="#004d40")

        if self.timeout_remaining > 0:
            self.timeout_remaining -= 1
            if self.timeout_remaining > 0:
                self.lbl_timeout_status.config(text=f"Time-Out: {self.timeout_remaining}s")
            else:
                self.lbl_timeout_status.config(text="")

        if self.pause_running:
            if self.pause_remaining > 0:
                self.pause_remaining -= 1
                self.update_pause_label()
            else:
                self.stop_pause()

        if self.running:
            if self.remaining > 0:
                self.remaining -= 1
                self.elapsed += 1
                self.clock.config(text=self.format_time(self.remaining))
                self.clock_elapsed.config(text=self.format_time(self.elapsed))

                if self.rule_90_active:
                    self.rule_90_remaining -= 1
                    self.lbl_90_status.config(text=f"90s-Regel: {self.rule_90_remaining}s")

                    if self.rule_90_remaining <= 0:
                        self.play_honk_sound()
                        self.stop_timer()

                self.update_team_penalties('home', self.penalties_home)
                self.update_team_penalties('guest', self.penalties_guest)
            else:
                self.running = False
                if self.current_period == self.max_periods:
                    self.is_game_over = True
                    self.play_honk_sound()

        self.update_zuschauer()
        self.after_id = self.root.after(1000, self.tick)

    def update_team_penalties(self, team, penalty_list):
        to_remove = []
        for p in penalty_list:
            if p["seconds"] > 0:
                p["seconds"] -= 1
                sec = p["seconds"]
                p["label"].config(text=self.format_time(sec))

                if sec <= 20:
                    if self.blink_state:
                        p["label"].config(bg="#ff3333", fg="#ffffff")
                    else:
                        p["label"].config(bg="#000000", fg="#ff3333")
                else:
                    p["label"].config(bg="#000000", fg="#ffeb3b")

                if sec == 0:
                    to_remove.append(p)

        for p in to_remove:
            self.remove_penalty(team, p)

    @staticmethod
    def format_time(seconds):
        seconds = max(0, int(seconds))
        return f"{seconds // 60:02d}:{seconds % 60:02d}"


# ==========================================
# KLASSE: AUSWAHL (STARTBILDSCHIRM/KONFIGURATION)
# ==========================================
class Auswahl:
    def __init__(self, root):
        self.root = root
        self.root.title("Zeitnehmer Auswahl")
        self.root.geometry("1280x820")
        self.root.configure(bg="#25d9e8")

        self.container = tk.Frame(self.root, bg="#25d9e8")
        self.container.pack(fill="both", expand=True)

        self.time_minutes = tk.IntVar(value=0)
        self.period = tk.StringVar(value="")
        self.rule_90 = tk.BooleanVar(value=False)
        self.rule_selected = False
        
        self.record_numbers = tk.BooleanVar(value=False)
        self.numbers_rule_selected = False

        self.pil_img_home = None
        self.pil_img_guest = None

        self.build()

    def text(self, value, size, bold=False):
        return tk.Label(self.container, text=value, font=("Arial", size, "bold" if bold else "normal"), bg="#25d9e8", fg="black")

    def select_button(self, text, command):
        return RoundedButton(self.container, text=text, command=command, bg="#ff7043", fg="black", font_size=22, radius=20)

    def build(self):
        home_box = tk.Frame(self.container, bg="#25d9e8")
        home_box.place(x=20, y=20)

        tk.Label(home_box, text="Heim-Team:", font=("Arial", 12, "bold"), bg="#25d9e8").pack(anchor="w")
        
        h_input_line = tk.Frame(home_box, bg="#25d9e8")
        h_input_line.pack(anchor="w", pady=2)

        self.entry_home = tk.Entry(h_input_line, font=("Arial", 14, "bold"), width=12)
        self.entry_home.insert(0, "HEIM")
        self.entry_home.pack(side="left", padx=(0, 5))

        tk.Button(h_input_line, text="Datei", command=lambda: self.select_logo('home'), font=("Arial", 9, "bold"), bg="#ffffff").pack(side="left")
        
        self.lbl_prev_home = tk.Label(h_input_line, bg="#25d9e8")
        self.lbl_prev_home.pack(side="left", padx=5)

        if self.pil_img_home:
            thumb = self.pil_img_home.resize((35, 35), Image.Resampling.LANCZOS)
            self.prev_home_tk = ImageTk.PhotoImage(thumb)
            self.lbl_prev_home.config(image=self.prev_home_tk)

        guest_box = tk.Frame(self.container, bg="#25d9e8")
        guest_box.place(relx=1.0, y=20, x=-20, anchor="ne")

        tk.Label(guest_box, text="Gast-Team:", font=("Arial", 12, "bold"), bg="#25d9e8").pack(anchor="e")

        g_input_line = tk.Frame(guest_box, bg="#25d9e8")
        g_input_line.pack(anchor="e", pady=2)

        self.lbl_prev_guest = tk.Label(g_input_line, bg="#25d9e8")
        self.lbl_prev_guest.pack(side="left", padx=5)

        tk.Button(g_input_line, text="Datei", command=lambda: self.select_logo('guest'), font=("Arial", 9, "bold"), bg="#ffffff").pack(side="left", padx=(0, 5))

        self.entry_guest = tk.Entry(g_input_line, font=("Arial", 14, "bold"), width=12, justify="right")
        self.entry_guest.insert(0, "GAST")
        self.entry_guest.pack(side="left")

        self.text("Spielzeit auswählen", 30, True).place(relx=0.5, y=30, anchor="n")

        self.b12 = self.select_button("12 min", lambda: self.choose_time(12))
        self.b12.place(x=290, y=90, width=170, height=65)

        self.b15 = self.select_button("15 min", lambda: self.choose_time(15))
        self.b15.place(x=490, y=90, width=170, height=65)

        self.b20 = self.select_button("20 min", lambda: self.choose_time(20))
        self.b20.place(x=690, y=90, width=170, height=65)

        custom_time_frame = tk.Frame(self.container, bg="#25d9e8")
        custom_time_frame.place(relx=0.5, y=175, anchor="n")

        tk.Label(custom_time_frame, text="Eigene Zeit (Min):", font=("Arial", 16, "bold"), bg="#25d9e8").pack(side="left", padx=5)
        
        self.entry_custom_time = tk.Entry(custom_time_frame, font=("Arial", 16, "bold"), width=5, justify="center")
        self.entry_custom_time.pack(side="left", padx=5)
        
        btn_apply_time = tk.Button(custom_time_frame, text="OK", command=self.choose_custom_time, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=4)
        btn_apply_time.pack(side="left", padx=5)

        self.lbl_selected_time_info = tk.Label(self.container, text="", font=("Arial", 14, "bold"), bg="#25d9e8", fg="#004d40")
        self.lbl_selected_time_info.place(relx=0.5, y=220, anchor="n")

        self.text("Spielabschnitt auswählen", 24, True).place(relx=0.5, y=260, anchor="n")
        self.bhalf = self.select_button("Halbzeit", lambda: self.choose_period("Halbzeit"))
        self.bhalf.place(x=320, y=315, width=250, height=60)

        self.bthird = self.select_button("Drittel", lambda: self.choose_period("Drittel"))
        self.bthird.place(x=610, y=315, width=250, height=60)

        self.text("90-Sekunden-Regel (U-10)", 22, True).place(relx=0.5, y=395, anchor="n")
        self.b90 = self.select_button("Mit 90 s. Regel", lambda: self.choose_rule(True))
        self.b90.place(x=320, y=445, width=250, height=55)

        self.bno90 = self.select_button("Ohne 90 s. Regel", lambda: self.choose_rule(False))
        self.bno90.place(x=610, y=445, width=250, height=55)

        self.text("Nummern erfassen (Tore & Strafzeiten)", 22, True).place(relx=0.5, y=520, anchor="n")
        self.bnum_yes = self.select_button("Mit Nummern", lambda: self.choose_numbers_rule(True))
        self.bnum_yes.place(x=320, y=570, width=250, height=55)

        self.bnum_no = self.select_button("Ohne Nummern", lambda: self.choose_numbers_rule(False))
        self.bnum_no.place(x=610, y=570, width=250, height=55)

    def select_logo(self, team):
        initial_dir = DEFAULT_LOGO_PATH if os.path.exists(DEFAULT_LOGO_PATH) else "/"
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=[("Bilder", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
        )
        if file_path:
            try:
                img = Image.open(file_path)
                thumb = img.resize((35, 35), Image.Resampling.LANCZOS)
                if team == 'home':
                    self.pil_img_home = img
                    self.prev_home_tk = ImageTk.PhotoImage(thumb)
                    self.lbl_prev_home.config(image=self.prev_home_tk)
                else:
                    self.pil_img_guest = img
                    self.prev_guest_tk = ImageTk.PhotoImage(thumb)
                    self.lbl_prev_guest.config(image=self.prev_guest_tk)
            except Exception as e:
                print(f"Fehler beim Öffnen des Bildes: {e}")

    def check_complete(self):
        if (self.time_minutes.get() > 0 and 
            self.period.get() in ("Halbzeit", "Drittel") and 
            self.rule_selected and 
            self.numbers_rule_selected):
            self.start_game()

    def choose_time(self, minutes):
        self.time_minutes.set(minutes)
        self.b12.set_bg("#ffff00" if minutes == 12 else "#ff7043")
        self.b15.set_bg("#ffff00" if minutes == 15 else "#ff7043")
        self.b20.set_bg("#ffff00" if minutes == 20 else "#ff7043")
        self.lbl_selected_time_info.config(text=f"Gewählte Spielzeit: {minutes} Minuten")
        self.check_complete()

    def choose_custom_time(self):
        try:
            val = int(self.entry_custom_time.get())
            if val > 0:
                self.time_minutes.set(val)
                self.b12.set_bg("#ff7043")
                self.b15.set_bg("#ff7043")
                self.b20.set_bg("#ff7043")
                self.lbl_selected_time_info.config(text=f"Gewählte Spielzeit: {val} Minuten (Benutzerdefiniert)")
                self.check_complete()
        except ValueError:
            pass

    def choose_period(self, period):
        self.period.set(period)
        self.bhalf.set_bg("#ffff00" if period == "Halbzeit" else "#ff7043")
        self.bthird.set_bg("#ffff00" if period == "Drittel" else "#ff7043")
        self.check_complete()

    def choose_rule(self, enabled):
        self.rule_90.set(enabled)
        self.rule_selected = True
        self.b90.set_bg("#ffff00" if enabled else "#ff7043")
        self.bno90.set_bg("#ffff00" if not enabled else "#ff7043")
        self.check_complete()

    def choose_numbers_rule(self, enabled):
        self.record_numbers.set(enabled)
        self.numbers_rule_selected = True
        self.bnum_yes.set_bg("#ffff00" if enabled else "#ff7043")
        self.bnum_no.set_bg("#ffff00" if not enabled else "#ff7043")
        self.check_complete()

    def start_game(self):
        name_h = self.entry_home.get().strip() if self.entry_home.get().strip() else "HEIM"
        name_g = self.entry_guest.get().strip() if self.entry_guest.get().strip() else "GAST"
        
        minutes = self.time_minutes.get()
        period_type = self.period.get()
        rule_90 = self.rule_90.get()
        record_numbers = self.record_numbers.get()
        
        img_h = self.pil_img_home
        img_g = self.pil_img_guest

        self.container.destroy()
        Zeitnehmer(self.root, minutes=minutes, period_type=period_type, rule_90=rule_90, record_numbers=record_numbers, name_home=name_h, name_guest=name_g, img_home=img_h, img_guest=img_g)


# ==========================================
# HAUPTPROGRAMM (PROGRAMMSTART)
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    
    def on_main_close():
        ConfirmDialog(root, "Programm beenden", "Möchtest du das Hauptprogramm wirklich schließen?", lambda res: root.destroy() if res else None)
        
    root.protocol("WM_DELETE_WINDOW", on_main_close)
    
    app = Auswahl(root)
    root.mainloop()