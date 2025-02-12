import tkinter as tk
from tkinter import messagebox
import os, platform

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer de Desligamento")

        # Variáveis de controle
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.timer_running = False
        self.paused = False
        self.timer_id = None

        # Entradas de tempo
        tk.Label(master, text="Horas:").grid(row=0, column=0)
        self.entry_h = tk.Entry(master, width=5)
        self.entry_h.grid(row=0, column=1)

        tk.Label(master, text="Minutos:").grid(row=0, column=2)
        self.entry_m = tk.Entry(master, width=5)
        self.entry_m.grid(row=0, column=3)

        tk.Label(master, text="Segundos:").grid(row=0, column=4)
        self.entry_s = tk.Entry(master, width=5)
        self.entry_s.grid(row=0, column=5)

        # Botões
        self.start_button = tk.Button(master, text="Iniciar Timer", command=self.start_timer)
        self.start_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.pause_button = tk.Button(master, text="Pausar", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.grid(row=1, column=2, pady=5)

        self.resume_button = tk.Button(master, text="Retomar", command=self.resume_timer, state=tk.DISABLED)
        self.resume_button.grid(row=1, column=3, pady=5)

        self.stop_button = tk.Button(master, text="Interromper", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=4, pady=5)

        # Exibição do tempo restante
        self.time_label = tk.Label(master, text="Tempo Restante: 00:00:00", font=("Helvetica", 16))
        self.time_label.grid(row=2, column=0, columnspan=6, pady=10)

        # Campo e botão para acrescentar tempo (em segundos)
        tk.Label(master, text="Adicionar tempo (s):").grid(row=3, column=0, columnspan=2)
        self.add_time_entry = tk.Entry(master, width=5)
        self.add_time_entry.grid(row=3, column=2)
        self.add_time_button = tk.Button(master, text="Adicionar", command=self.add_time, state=tk.DISABLED)
        self.add_time_button.grid(row=3, column=3, pady=5)

    def start_timer(self):
        try:
            hours = int(self.entry_h.get() or 0)
            minutes = int(self.entry_m.get() or 0)
            seconds = int(self.entry_s.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números.")
            return

        self.total_seconds = hours * 3600 + minutes * 60 + seconds
        if self.total_seconds <= 0:
            messagebox.showerror("Erro", "Informe um tempo maior que zero.")
            return

        self.remaining_seconds = self.total_seconds
        self.timer_running = True
        self.paused = False
        self._altera_botoes(rodando=True)
        self.countdown()

    def countdown(self):
        if self.timer_running and not self.paused:
            self._atualiza_label()
            if self.remaining_seconds <= 0:
                self.shutdown_system()
                return
            self.remaining_seconds -= 1
            self.timer_id = self.master.after(1000, self.countdown)

    def _atualiza_label(self):
        hrs = self.remaining_seconds // 3600
        mins = (self.remaining_seconds % 3600) // 60
        secs = self.remaining_seconds % 60
        self.time_label.config(text=f"Tempo Restante: {hrs:02d}:{mins:02d}:{secs:02d}")

    def pause_timer(self):
        if self.timer_running and not self.paused:
            self.paused = True
            if self.timer_id:
                self.master.after_cancel(self.timer_id)
            self._altera_botoes(paused=True)

    def resume_timer(self):
        if self.timer_running and self.paused:
            self.paused = False
            self._altera_botoes(paused=False)
            self.countdown()

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            if self.timer_id:
                self.master.after_cancel(self.timer_id)
            self._resetar_interface()

    def add_time(self):
        try:
            adicional = int(self.add_time_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Erro", "Informe um valor numérico.")
            return
        if adicional > 0:
            self.remaining_seconds += adicional
            self._atualiza_label()

    def shutdown_system(self):
        # Removido o popup para desligamento automático
        sistema = platform.system()
        if sistema == "Windows":
            os.system("shutdown /s /t 1")
        elif sistema == "Linux":
            os.system("shutdown -h now")
        elif sistema == "Darwin":
            os.system("osascript -e 'tell app \"System Events\" to shut down'")
        self._resetar_interface()

    def _resetar_interface(self):
        self.timer_running = False
        self.paused = False
        self.remaining_seconds = 0
        self._atualiza_label()
        self._altera_botoes(rodando=False)

    def _altera_botoes(self, rodando=False, paused=False):
        if rodando:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL if not paused else tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL if paused else tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.add_time_button.config(state=tk.NORMAL)
            self.entry_h.config(state=tk.DISABLED)
            self.entry_m.config(state=tk.DISABLED)
            self.entry_s.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.add_time_button.config(state=tk.DISABLED)
            self.entry_h.config(state=tk.NORMAL)
            self.entry_m.config(state=tk.NORMAL)
            self.entry_s.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
