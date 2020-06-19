from tkinter import Label, Button
from vue.base_frame import BaseFrame


class MenuMembreFrame(BaseFrame):
    def __init__(self, root_frame):
        super().__init__(root_frame)
        self.create_widgets()

    def create_widgets(self):
        self.title = Label(self, text="Welcome in BDS App")
        self.members = Button(self, text="Members", width=30, command=self._root_frame.show_members_membre)
        self.coaches = Button(self, text="Coaches", width=30, command=self._root_frame.show_coaches_membre)
        self.sports = Button(self, text="Sports", width=30, command=self._root_frame.show_sports_member)
        self.quit = Button(self, text="QUIT", fg="red", width=30,
                           command=self.quit)
        self.title.pack(side="top")
        self.members.pack()
        self.coaches.pack()
        self.sports.pack()
        self.quit.pack(side="bottom")
