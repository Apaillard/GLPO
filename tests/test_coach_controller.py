import unittest
import uuid
from exceptions import InvalidData, Error, ResourceNotFound
from controller.person_controller import PersonController
from model.database import DatabaseEngine
from model.mapping.sport import Sport
from model.mapping.person import Person
from model.mapping.coach import Coach
from model.mapping.address import Address


class TestCoachController(unittest.TestCase):
    """
    Unit Tests sport controller
    https://docs.python.org/fr/3/library/unittest.html
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._database_engine = DatabaseEngine()
        cls._database_engine.create_database()
        with cls._database_engine.new_session() as session:
            # Sport
            basket = Sport(id=str(uuid.uuid4()), name="basket", description="")
            session.add(basket)
            session.flush()
            cls.backet_id = basket.id

            # Person
            john = Coach(id=str(uuid.uuid4()),
                         firstname="john", lastname="do",
                         email="john.do@mail.com",
                         contract="CDI",
                         degree="BPJEPS")
            session.add(john)
            session.flush()
            cls.john_id = john.id
            steeve = Coach(id=str(uuid.uuid4()),
                           firstname="steeve",
                           lastname="gates",
                           email="steeve.gates@gmail.com",
                           contract="Interim",
                           degree="BNSSA")
            steeve.address = Address(street="21 rue docteur guerin",
                                     city="Laval",
                                     postal_code=53000)
            steeve.add_sport(basket, "professional", session)
            cls.steeve_id = steeve.id
            session.add(steeve)
            session.flush()

    def setUp(self) -> None:
        """
        Function called before each test
        """
        self.person_controller = PersonController(self._database_engine)

    def test_list_coaches(self):
        coaches = self.person_controller.list_people(person_type="coach")
        self.assertGreaterEqual(len(coaches), 2)

    def test_get_coach(self):
        coach = self.person_controller.get_person(self.john_id, person_type="coach")
        self.assertEqual(coach['firstname'], "john")
        self.assertEqual(coach['lastname'], "do")
        self.assertEqual(coach['id'], self.john_id)
        self.assertEqual(coach['contract'], 'CDI')
        self.assertEqual(coach['degree'], 'BPJEPS')
        self.assertEqual(len(coach['sports']), 0)

        coach = self.person_controller.get_person(self.steeve_id, person_type="coach")
        self.assertEqual(coach['firstname'], "steeve")
        self.assertEqual(coach['lastname'], "gates")
        self.assertEqual(coach['id'], self.steeve_id)
        self.assertEqual(coach['contract'], 'Interim')
        self.assertEqual(coach['degree'], 'BNSSA')
        self.assertEqual(len(coach['sports']), 1)
        self.assertEqual(coach['sports'][0]['id'], self.backet_id)
        self.assertEqual(coach['sports'][0]['name'], "basket")
        self.assertIn("address", coach)
        self.assertEqual(coach["address"]["city"], "Laval")

    def test_get_coach_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.get_person(str(uuid.uuid4()))

    def test_create_coach(self):
        data = {
            "firstname": "Han",
            "lastname": "Solo",
            "email": "han.solo@star.com",
            "contract": "CDD",
            "degree": "STAPS"
        }
        coach_data = self.person_controller.create_person(data, person_type="coach")
        self.assertIn('id', coach_data)
        self.assertEqual(data['firstname'].lower(), coach_data['firstname'])
        self.assertEqual(data['lastname'].lower(), coach_data['lastname'])

    def test_create_coach_missing_data(self):
        data = {}
        with self.assertRaises(InvalidData):
            self.person_controller.create_person(data, person_type="coach")

    def test_create_person_error_already_exists(self):
        data = {"firstname": "John", "lastname": "Do", "email": "john.do@hostmail.fr",
                "contract": "CDD", "degree": "NO"}
        with self.assertRaises(Error):
            self.person_controller.create_person(data, person_type="coach")

    def test_update_coach(self):
        coach_data = self.person_controller.update_person(
            self.john_id, {"email": "john.do@updated.com"})
        self.assertEqual(coach_data['email'], "john.do@updated.com")

    def test_update_coach_invalid_data(self):
        with self.assertRaises(InvalidData):
            self.person_controller.update_person(self.john_id, {"email": "test"})

    def test_update_coach_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.update_coach("test", {"description": "test foot"})

    def test_delete_coach(self):
        with self._database_engine.new_session() as session:
            rob = Coach(id=str(uuid.uuid4()), firstname="rob", lastname="stark",
                        email="rob.stark@winterfell.com",
                        contract="CDI", degree="test")
            session.add(rob)
            session.flush()
            rob_id = rob.id

        self.person_controller.delete_person(rob_id)
        with self.assertRaises(ResourceNotFound):
            self.person_controller.delete_person(rob_id)

    def test_delete_coach_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.delete_person(str(uuid.uuid4()))

    def test_search_coach(self):
        coach = self.person_controller.search_person("john", "do", person_type="coach")
        self.assertEqual(coach['id'], self.john_id)

    def test_search_sport_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.search_person("john", "snow", person_type="coach")

    def test_add_sport(self):
        with self._database_engine.new_session() as session:
            linus = Coach(id=str(uuid.uuid4()), firstname="linus", lastname="torvalds",
                          email="linus.torvalds@tux.net",
                          contract="CDI", degree="test")
            session.add(linus)
            session.flush()
            linus_id = linus.id

        person = self.person_controller.add_sport_person(linus_id, self.backet_id, "high")
        self.assertEqual(person['id'], linus_id)
        self.assertEqual(len(person['sports']), 1)
        self.assertEqual(person['sports'][0]['name'], "basket")
        self.assertEqual(person['sports'][0]['id'], self.backet_id)

    def test_add_sport_error_exists(self):
        with self.assertRaises(Error):
            self.person_controller.add_sport_person(self.steeve_id, self.backet_id, "high")

    def test_remove_sport(self):
        with self._database_engine.new_session() as session:
            dennis = Coach(id=str(uuid.uuid4()), firstname="Dennis", lastname="Ritchie",
                           email="denis.ritchie@unix.net",
                           contract="CDI", degree="test")
            session.add(dennis)
            session.flush()
            foot = Sport(id=str(uuid.uuid4()), name="foot", description="")
            session.add(foot)
            session.flush()
            foot_id = foot.id
            dennis.add_sport(foot, "expert", session)
            dennis_id = dennis.id

        person = self.person_controller.delete_sport_person(dennis_id, foot_id)
        self.assertEqual(person['id'], dennis_id)
        self.assertEqual(len(person['sports']), 0)

    def test_remove_sport_not_exists(self):
        with self.assertRaises(Error):
            self.person_controller.delete_sport_person(self.john_id, self.backet_id)


if __name__ == '__main__':
    unittest.main()
