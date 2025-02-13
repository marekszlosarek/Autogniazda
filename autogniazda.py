import tkinter as tk
from tkinter import scrolledtext, Scrollbar
import keyboard
from time import sleep

class Automat(tk.Tk):

    def get_entries_list(self) -> list[str]:
        entries_text = self.spp_area.get("1.0", tk.END)
        entries_list = list(filter(None, entries_text.split('\n')))

        return entries_list

    def on_clear(self) -> None:
        self.spp_area.delete("1.0", tk.END)

    def on_exit(self) -> None:
        self.destroy()

    def highlight_line(self, line_number: int) -> None:
        self.spp_area.tag_remove("highlight", "1.0", tk.END)  
        self.spp_area.tag_add("highlight", f"{line_number}.0", f"{line_number}.end")
        self.spp_area.tag_config("highlight", background="yellow")  
        
    def return_to_first(self) -> None:
        self.highlight_counter = 1
        self.highlight_line(self.highlight_counter)

    def step_back(self) -> None:
        self.highlight_counter -= 1
        if self.highlight_counter < 1:
            self.highlight_counter = len(self.get_entries_list())
        self.highlight_line(self.highlight_counter)

    def step_forward(self) -> None:
        self.highlight_counter += 1
        if self.highlight_counter > len(self.get_entries_list()):
            self.highlight_counter = 1
        self.highlight_line(self.highlight_counter)

    def listen_spp(self, event) -> None:
        self.spp_area.edit_modified(False)
        self.return_to_first()

    def prevent_newline(self, event) -> None:
        return "break"

    def paste_hotkey(self) -> None:
        id_text = self.id_area.get("1.0", tk.END)
        id_text = id_text.removesuffix('\n')
        if len(entries_list := self.get_entries_list()) >= self.highlight_counter:
            spp_text = entries_list[self.highlight_counter-1]
        else:
            spp_text = ''

        keyboard.write(id_text)
        sleep(.1)
        keyboard.press_and_release('tab')
        sleep(.1)
        keyboard.write(spp_text)

        self.highlight_counter += 1
        if self.highlight_counter > len(entries_list):
            self.highlight_counter = 1
        self.highlight_line(self.highlight_counter)

    def toggle(self):
        self.status = not self.status
        self.status_label.config(state="normal") 
        self.status_label.delete('1.0', tk.END)
        if self.status:
            self.status_label.insert("1.0", f"Status:   Aktywny ")
            self.status_label.tag_add("highlight", f"1.7", tk.END)
            self.status_label.tag_config("highlight", background='#06402b', foreground="white") 
            keyboard.add_hotkey('f9', self.paste_hotkey)
            self.status_toggle.config(text='Wyłącz')
            self.status_explanation.config(text="Kliknij na miejsce, gdzie powinno się wpisać identyfikator i wciśnij F9")
        else:
            self.status_label.insert("1.0", f"Status: Nieaktywny")
            self.status_label.tag_add("highlight", f"1.7", tk.END)
            self.status_label.tag_config("highlight", background='#a62c2b', foreground="white") 
            keyboard.remove_all_hotkeys()
            self.status_toggle.config(text='Włącz')
            self.status_explanation.config(text="")
        self.status_label.config(state="disabled") 



    def __init__(self) -> None:
        super().__init__()
        
        self.highlight_counter = 0
        self.status = False

        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)

        ## Segment identyfikatora
        id_frame = tk.Frame(frame)
        id_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nw')

        self.id_label = tk.Label(id_frame, text="Numer identyfikatora: ")
        self.id_label.pack(fill=tk.X, pady=2, anchor='w')

        self.id_area = tk.Text(id_frame, width=15, height=1)
        self.id_area.pack(fill=tk.X, pady=2, anchor='w')
        self.id_area.bind("<Return>", self.prevent_newline)

        ## Segment włączania
        toggle_frame = tk.Frame(frame)
        toggle_frame.grid(row=1, column=1, padx=5, pady=5)

        self.status_label = tk.Text(toggle_frame, width=19, height=1, background="#f0f0f0")
        self.status_label.insert("1.0", f"Status: Nieaktywny")
        self.status_label.tag_add("highlight", f"1.7", tk.END)
        self.status_label.tag_config("highlight", background='#a62c2b', foreground="white")
        self.status_label.config(state="disabled") 
        self.status_label.pack(fill=tk.X, pady=2)

        self.status_toggle = tk.Button(toggle_frame, text="Włącz", width=10, height=1, command=self.toggle)
        self.status_toggle.pack(fill=tk.X, pady=2)


        ## Segment indeksów
        self.spp_label = tk.Label(frame, text="Indeksy SPP: ")
        self.spp_label.grid(row=2, column=0, sticky="w")

        self.spp_area = scrolledtext.ScrolledText(frame, width=20, height=16, wrap=tk.WORD)
        self.spp_area.grid(row=3, column=0, padx=5, pady=5)
        self.spp_area.bind('<<Modified>>', self.listen_spp)

        ## Segment przycisków
        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=1, padx=5, pady=5, sticky="ns")

        self.status_explanation = tk.Label(button_frame, text='', wraplength=160, height=4, font=13, width=20)
        self.status_explanation.pack(fill=tk.X, pady=(0, 40), anchor='n')

        clear_btn = tk.Button(button_frame, text="Wyczyść", command=self.on_clear)
        clear_btn.pack(fill=tk.X, pady=2)

        to_first_btn = tk.Button(button_frame, text="⧋ Wróć do pierwszego", command=self.return_to_first)
        to_first_btn.pack(fill=tk.X, pady=2)

        return_btn = tk.Button(button_frame, text="△ Poprzedni", command=self.step_back)
        return_btn.pack(fill=tk.X, pady=2)

        advance_btn = tk.Button(button_frame, text="▽ Następny", command=self.step_forward)
        advance_btn.pack(fill=tk.X, pady=2)

        exit_btn = tk.Button(button_frame, text="Wyjdź", command=self.on_exit)
        exit_btn.pack(fill=tk.X, pady=2)


if __name__ == '__main__':
    root = Automat()
    root.title("Automat do otwierania gniazd")
    root.mainloop()
