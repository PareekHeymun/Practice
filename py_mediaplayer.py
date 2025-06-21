import sys, tkinter as tk, vlc

VIDEO = "video.mp4"   # must be next to this script

class MediaPlayer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title("py_mediaplayer (VLC)")
        self.pack(fill=tk.BOTH, expand=1)

        # 1) VLC instance + player
        self.instance = vlc.Instance('--no-video-title-show')
        self.player   = self.instance.media_player_new()

        # 2) embed into Tk
        panel = tk.Frame(self); panel.pack(fill=tk.BOTH, expand=1)
        self.update_idletasks()
        win_id = panel.winfo_id()
        if sys.platform == "win32":
            self.player.set_hwnd(win_id)
        else:
            self.player.set_xwindow(win_id)

        # 3) load and play
        media = self.instance.media_new(VIDEO)
        self.player.set_media(media)
        self.player.play()

        # ───────────────────────────────────────────────────
        # ONE LINER: quit the Tk loop as soon as the movie ends
        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached,
            lambda e: master.destroy()
        )
        # ───────────────────────────────────────────────────

        # 4) clean up on [X]
        master.protocol("WM_DELETE_WINDOW", master.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x450")
    MediaPlayer(root)
    root.mainloop()
