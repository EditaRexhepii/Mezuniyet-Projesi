import tkinter as tk
import all_frames
import inspect

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared_data = {"username": tk.StringVar()}
        self.wm_title("Test Application")
        self.container = tk.Frame(self, height=400, width=600)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        all_classes=[]
        self.level_class=[]
        for name, obj in inspect.getmembers(all_frames):
            if inspect.isclass(obj):
                if obj.__name__ == 'Thread':
                    pass
                elif obj.__name__ == 'sign_in':
                    all_classes.insert(0,obj)
                elif obj.__name__ == 'choose_level':
                    self.level_class.insert(0,obj)
                else:
                    all_classes.append(obj)
        for F in (all_classes):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(all_classes[0])

    def show_frame(self, cont):
        frame = self.frames[cont]
        # frame.update()
        frame.tkraise()

    def add_level_page(self):
        for F in (self.level_class):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    root = windows()
    root.attributes("-fullscreen", True)
    root.mainloop()