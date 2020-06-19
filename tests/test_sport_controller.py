import unittest
import uuid
from exceptions import InvalidData, Error, ResourceNotFound
from controller.sport_controller import SportController
from model.database import DatabaseEngine
from model.mapping.sport import Sport
from model.mapping.person import Person


class TestSportController(unittest.TestCase):
    """
    Unit Tests sport controller
    https://docs.python.org/fr/3/library/unittest.html
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._database_engine = DatabaseEngine()
        cls._database_engine.create_database()
        with cls._database_engine.new_session() as session:
            basket = Sport(id=str(uuid.uuid4()), name="basket", description="")
            session.add(basket)
            session.flush()
            cls.backet_id = basket.id

    def setUp(self) -> None:
        """
        Function called before each test
        """
        self.sport_controller = SportController(self._database_engine)

    def test_list_sports(self):
        sports = self.sport_controller.list_sports()
        self.assertGreaterEqual(len(sports), 1)

    def test_get_sport(self):
        sport = self.sport_controller.get_sport(self.backet_id)
        self.assertEqual(sport['name'], "basket")
        self.assertEqual(sport['id'], self.backet_id)

    def test_get_sport_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.sport_controller.get_sport(str(uuid.uuid4()))

    def test_create_sport(self):
        data = {
            "name": "foot",
            "description": "Kicking a ball and chasing after"
        }
        sport_data = self.sport_controller.create_sport(data)
        self.assertIn('id', sport_data)
        self.assertEqual(data['name'], sport_data['name'])
        self.assertEqual(data['description'], sport_data['description'])

    def test_create_sport_missing_data(self):
        data = {}
        with self.assertRaises(InvalidData):
            self.sport_controller.create_sport(data)

    def test_create_sport_error_already_exists(self):
        data = {"name": "foot", "description": "Kicking a ball and chasing after"}
        with self.assertRaises(Error):
            self.sport_controller.create_sport(data)

    def test_update_sport(self):
        sport_data = self.sport_controller.update_sport(self.backet_id,
                                                        {"description": "test foot"})
        self.assertEqual(sport_data['description'], "test foot")

    def test_update_sport_invalid_data(self):
        with self.assertRaises(InvalidData):
            self.sport_controller.update_sport("test", {"description": 1})

    def test_update_sport_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.sport_controller.update_sport("test", {"description": "test foot"})

    def test_delete_sport(self):
        with self._database_engine.new_session() as session:
            basket = Sport(id=str(uuid.uuid4()), name="hockey", description="")
            session.add(basket)
            session.flush()
            hockey_id = basket.id

        self.sport_controller.delete_sport(hockey_id)
        with self.assertRaises(ResourceNotFound):
            self.sport_controller.get_sport(hockey_id)

    def test_delete_sport_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.sport_controller.delete_sport(str(uuid.uuid4()))

    def test_search_sport(self):
        sport = self.sport_controller.search_sport("basket")
        self.assertEqual(sport['name'], "basket")
        self.assertEqual(sport['id'], self.backet_id)

    def test_search_sport_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.sport_controller.search_sport("danse")


if __name__ == '__main__':
    unittest.main()
