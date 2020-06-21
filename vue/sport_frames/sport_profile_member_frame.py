from tkinter import *
from tkinter import messagebox

from vue.sport_frames.sport_formular_frame import SportFormularFrame
from exceptions import Error


class SportProfileMemberFrame(SportFormularFrame):

    def __init__(self, sport_controller, sport, master=None):
        super().__init__(master)
        self._sport_controller = sport_controller
        self._sport = sport
        self.refresh()

    def create_widgets(self):
        super().create_widgets()

        # Buttons
        self.return_button = Button(self, text="Return", fg="red",
                                    command=self.back)

        self.return_button.grid(row=20, column=0)

    def edit(self):
        entries = [self.name_entry, self.description_entry]
        for entry in entries:
            entry.config(state=NORMAL)

    def _refresh_entry(self, entry, value=""):
        entry.delete(0, END)
        if value != "":
            entry.insert(0, value)
        entry.config(state=DISABLED)

    def refresh(self):
        # Restore window with member value and cancel edition
        self._refresh_entry(self.name_entry, self._sport['name'])
        self.description_entry.delete("0.0", END)
        self.description_entry.insert("0.0", self._sport['description'])
        self.description_entry.config(state=DISABLED)

    def update(self):

        data = self.get_data()
        sport = self._sport_controller.update_sport(self._sport['id'], data)
        self._sport = sport
        self.refresh()

    def remove(self):
        sport_id = self._sport['id']
        self._sport_controller.delete_sport(sport_id)
        # show confirmation
        messagebox.showinfo("Success",
                            "Sport %s deleted !" % self._sport['name'])
        self.back()
