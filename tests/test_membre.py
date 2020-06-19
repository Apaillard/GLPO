import unittest
import uuid
from exceptions import InvalidData, Error, ResourceNotFound
from controller.person_controller import PersonController
from model.database import DatabaseEngine
from model.mapping.person import Person
from model.mapping.address import Address


class TestPersonController(unittest.TestCase):
    """
    Unit Tests sport controller
    https://docs.python.org/fr/3/library/unittest.html
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._database_engine = DatabaseEngine()
        cls._database_engine.create_database()
        with cls._database_engine.new_session() as session:



            steeve = Person(id=str(uuid.uuid4()),
                           firstname="steeve",
                           lastname="gates",
                           email="steeve.gates@gmail.com")
            steeve.address = Address(street="21 rue docteur guerin",
                                     city="Laval",
                                     postal_code=53000)
            cls.steeve_id = steeve.id
            session.add(steeve)
            session.flush()

    def setUp(self) -> None:
        """
        Function called before each test
        """
        self.person_controller = PersonController(self._database_engine)

    def test_list_Persones(self):
        Persones = self.person_controller.list_people(person_type="Person")
        self.assertGreaterEqual(len(Persones), 1)

    def test_get_Person(self):

        Person = self.person_controller.get_person(self.steeve_id, person_type="Person")
        self.assertEqual(Person['firstname'], "steeve")
        self.assertEqual(Person['lastname'], "gates")
        self.assertEqual(Person['id'], self.steeve_id)
        self.assertIn("address", Person)
        self.assertEqual(Person["address"]["city"], "Laval")

    def test_get_Person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.get_person(str(uuid.uuid4()))


    def test_create_Person_missing_data(self):
        data = {}
        with self.assertRaises(InvalidData):
            self.person_controller.create_person(data, person_type="Person")


    def test_update_Person(self):
        Person_data = self.person_controller.update_person(
            self.steeve_id, {"email": "steeve.gates@updated.com"})
        self.assertEqual(Person_data['email'], "steeve.gates@updated.com")

    def test_update_Person_invalid_data(self):
        with self.assertRaises(InvalidData):
            self.person_controller.update_person(self.steeve_id, {"email": "test"})

    def test_update_Person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.update_member("test", {"description": "test foot"})

    def test_delete_Person(self):
        with self._database_engine.new_session() as session:
            rob = Person(id=str(uuid.uuid4()), firstname="rob", lastname="stark",
                        email="rob.stark@winterfell.com")
            session.add(rob)
            session.flush()
            rob_id = rob.id

        self.person_controller.delete_person(rob_id)
        with self.assertRaises(ResourceNotFound):
            self.person_controller.delete_person(rob_id)

    def test_delete_Person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.delete_person(str(uuid.uuid4()))



if __name__ == '__main__':
    unittest.main()
