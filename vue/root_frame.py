from tkinter import *

from vue.menu_frame import MenuFrame
from vue.menu_membre_frame import MenuMembreFrame
from vue.menu_connexion_frame import MenuConnexionFrame
from vue.member_frames.new_member_frame import NewMemberFrame
from vue.member_frames.new_coach_frame import NewCoachFrame
from vue.member_frames.list_members_frame import ListMembersFrame
from vue.member_frames.list_membres_membre_frame import ListMembersMembresFrame
from vue.member_frames.profile_frame import ProfileFrame
from vue.member_frames.profile_membre_frame import ProfileMembreFrame
from vue.sport_frames.list_sports_frame import ListSportsFrame
from vue.sport_frames.list_sports_member_frame import ListSportsMemberFrame
from vue.sport_frames.new_sport_frame import NewSportFrame
from vue.sport_frames.sport_profile_frame import SportProfileFrame
from vue.sport_frames.sport_profile_member_frame import SportProfileMemberFrame
from vue.member_frames.connexion_frame import ConnexionFrame



class RootFrame(Frame):
    """
    Member actions
    help: http://www.xavierdupre.fr/app/teachpyx/helpsphinx/c_gui/tkinter.html
    """

    def __init__(self, person_controller, sport_controller, master=None):
        super().__init__(master)
        self._person_controller = person_controller
        self._sport_controller = sport_controller
        self._menu_frame = MenuFrame(self)
        self._menu_membre_frame = MenuMembreFrame(self)
        self._menu_connexion_frame = MenuConnexionFrame(self)
        self._frames = []

    def new_member(self):
        self.hide_menu()
        self.hide_frames()
        # Show formular subscribe
        subscribe_frame = NewMemberFrame(self._person_controller, self)
        subscribe_frame.show()
        self._frames.append(subscribe_frame)

    def new_coach(self):
        self.hide_menu()
        self.hide_frames()
        subscribe_frame = NewCoachFrame(self._person_controller, self)
        subscribe_frame.show()
        self._frames.append(subscribe_frame)

    def new_sport(self):
        self.hide_menu()
        self.hide_frames()
        new_sport_frame = NewSportFrame(self._sport_controller, self)
        new_sport_frame.show()
        self._frames.append(new_sport_frame)

    def show_members(self):
        # show members
        self.hide_menu()
        list_frame = ListMembersFrame(self._person_controller, self, person_type='member')
        self._frames.append(list_frame)
        list_frame.show()

    def show_members_membre(self):
        # show members
        self.hide_menu()
        list_frame = ListMembersMembresFrame(self._person_controller, self, person_type='member')
        self._frames.append(list_frame)
        list_frame.show()
        
    def show_coaches(self):
        # show members
        self.hide_menu()
        list_frame = ListMembersFrame(self._person_controller, self, person_type='coach')
        self._frames.append(list_frame)
        list_frame.show()

    def show_coaches_membre(self):
        # show members
        self.hide_menu()
        list_frame = ListMembersMembresFrame(self._person_controller, self, person_type='coach')
        self._frames.append(list_frame)
        list_frame.show()

    def show_profile(self, member_id):
        self.hide_menu()
        member_data = self._person_controller.get_person(member_id)
        self.hide_frames()
        profile_frame = ProfileFrame(self._person_controller, self._sport_controller, member_data, self)
        self._frames.append(profile_frame)
        profile_frame.show()

    def show_profile_membre(self, member_id):
        self.hide_menu()
        member_data = self._person_controller.get_person(member_id)
        self.hide_frames()
        profile_frame = ProfileMembreFrame(self._person_controller, self._sport_controller, member_data, self)
        self._frames.append(profile_frame)
        profile_frame.show()

    def show_sports(self):
        self.hide_menu()
        list_frame = ListSportsFrame(self._sport_controller, self)
        self._frames.append(list_frame)
        list_frame.show()

    def show_sports_member(self):
        self.hide_menu()
        list_frame = ListSportsMemberFrame(self._sport_controller, self)
        self._frames.append(list_frame)
        list_frame.show()

    def show_sport(self, sport_id):
        self.hide_menu()
        sport_data = self._sport_controller.get_sport(sport_id)
        self.hide_frames()
        profile_frame = SportProfileFrame(self._sport_controller, sport_data, self)
        self._frames.append(profile_frame)
        profile_frame.show()

    def show_sport_member(self, sport_id):
        self.hide_menu()
        sport_data = self._sport_controller.get_sport(sport_id)
        self.hide_frames()
        profile_frame = SportProfileMemberFrame(self._sport_controller, sport_data, self)
        self._frames.append(profile_frame)
        profile_frame.show()

    def show_connexion(self):
        self.hide_menu()
        # Show fennetre de connexion
        connexion_frame = ConnexionFrame(self._person_controller, self)
        connexion_frame.show()
        self._frames.append(connexion_frame)

    def hide_frames(self):
        for frame in self._frames:
            frame.hide()

    def show_menu(self):
        self.hide_menu()
        for frame in self._frames:
            frame.destroy()
        self._frames = []
        self._menu_frame.show()

    def show_menu_membre(self):
        self.hide_menu()
        for frame in self._frames:
            frame.destroy()
        self._frames = []
        self._menu_membre_frame.show()

    def show_menu_connexion(self):
        self.hide_menu()
        for frame in self._frames:
            frame.destroy()
        self._frames = []
        self._menu_connexion_frame.show()


    def hide_menu(self):
        self._menu_frame.hide()
        self._menu_connexion_frame.hide()
        self._menu_membre_frame.hide()


    def back(self):
        if len(self._frames) <= 1:
            self.show_menu()
            return
        last_frame = self._frames[-1]
        last_frame.destroy()
        del(self._frames[-1])
        last_frame = self._frames[-1]
        last_frame.show()

    def cancel(self):
        self.show_menu()

    def quit(self):
        self.master.destroy()
