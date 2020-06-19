from tkinter import Label, Button
from vue.base_frame import BaseFrame


class MenuConnexionFrame(BaseFrame):
    def __init__(self, root_frame):
        super().__init__(root_frame)
        self.create_widgets()

    def create_widgets(self):
        self.title = Label(self, text="Welcome in BDS App")
        self.subscribe = Button(self, text="Subscribe", width=30, command=self._root_frame.new_member)
        self.connexion = Button(self, text="Connexion", width=30, command=self._root_frame.show_connexion)
        self.quit = Button(self, text="QUIT", fg="red", width=30,
                           command=self.quit)
        self.title.pack(side="top")
        self.subscribe.pack()
        self.connexion.pack()
        self.quit.pack(side="bottom")
