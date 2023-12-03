import tkinter as tk
import win32gui
import win32con

class UstteDurPencere(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Üstte Duran Pencereleri Yönet")
        self.geometry("400x400")

        self.pencere_listesi = self.get_open_windows()
        self.secili_pencere = None

        # Açık pencerelerin listesini gösteren liste kutucuğu
        self.pencere_listbox = tk.Listbox(self, selectmode=tk.SINGLE, exportselection=0)
        self.refresh_window_list()
        self.pencere_listbox.pack(pady=10)
        self.pencere_listbox.bind("<<ListboxSelect>>", self.secili_pencereyi_degistir)

        # "Seçili Pencereyi Üstte Tut" düğmesi
        ustte_tut_button = tk.Button(self, text="Seçili Pencereyi Üstte Tut", command=self.secili_pencereyi_ustte_tut)
        ustte_tut_button.pack(pady=10)

        # "Pencere Listesini Yenile" düğmesi
        yenile_button = tk.Button(self, text="Pencere Listesini Yenile", command=self.refresh_window_list)
        yenile_button.pack(pady=10)

        # "Pasif" düğmesi
        pasif_button = tk.Button(self, text="Pasif", command=self.pasif_yap)
        pasif_button.pack(pady=10)

        # Pencerenin kapatılmasını dinle
        self.protocol("WM_DELETE_WINDOW", self.pencere_kapat)

    def get_open_windows(self):
        windows = []
        toplist = []
        win32gui.EnumWindows(lambda hwnd, param: toplist.append((hwnd, win32gui.GetWindowText(hwnd))), None)
        for hwnd, title in toplist:
            if title:
                windows.append((hwnd, title))
        return windows

    def refresh_window_list(self):
        self.pencere_listesi = self.get_open_windows()
        self.pencere_listbox.delete(0, tk.END)
        for _, title in self.pencere_listesi:
            self.pencere_listbox.insert(tk.END, title)

    def secili_pencereyi_degistir(self, event):
        if self.pencere_listbox.curselection():
            index = self.pencere_listbox.curselection()[0]
            self.secili_pencere = self.pencere_listesi[index]

    def secili_pencereyi_ustte_tut(self):
        if self.secili_pencere:
            win32gui.SetWindowPos(self.secili_pencere[0], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def pasif_yap(self):
        if self.secili_pencere:
            win32gui.SetWindowPos(self.secili_pencere[0], win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def pencere_kapat(self):
        self.destroy()

# Tkinter uygulamasını başlat
ustte_dur_pencere = UstteDurPencere()
ustte_dur_pencere.mainloop()
