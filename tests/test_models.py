from unittest import TestCase

from app.models import Person, Fellow, Staff, Base, Room, Office, LivingSpace, engine


class PersonTestCase(TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.person = Person.create("Some Name", "staff")

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_class_has_required_attributes(self):
        self.assertTrue(hasattr(Person, 'id'))
        self.assertTrue(hasattr(Person, 'name'))
        self.assertTrue(hasattr(Person, 'role'))
        self.assertTrue(hasattr(Person, '__table__'))

    def test_class_attributes_mapped_to_right_db_types(self):
        self.assertEqual(type(self.person.id), int)
        self.assertEqual(type(self.person.name), str)
        self.assertEqual(type(self.person.role), str)

    def test_class_has_mapped_to_right_table(self):
        self.assertEqual(getattr(Person, '__table__').name, 'people')

    def test_all(self):
        self.assertEqual(1, Person.all().count())
        new_person = Person(name="New Name")
        new_person.save()
        self.assertEquals(2, Person.all().count())

    def test_save(self):
        new_person = Person(name="New Name")
        new_person.save()
        self.assertIn(new_person, Person.all())

    def test_create(self):
        current_count = Person.all().count()
        Person.create("New Person", 'fellow')
        self.assertEqual(Person.all().count(), current_count+1)

    def test_add_to_room(self):
        self.assertEqual(self.person.office_id, None)
        room = Office.create("New Room")
        self.person.add_to_room(room)
        self.assertEqual(self.person.office_id, room.id)

    def test_add_fellow_with_location_request(self):
        current_count = Person.all().count()
        person = Person.add_person("New", "Fellow", "Fellow", wants_accommodation=True)
        self.assertEqual(current_count + 1, Person.all().count())
        self.assertIsNotNone(person.office_id)
        self.assertIsNotNone(person.living_space_id)

    def test_add_fellow_without_location_request(self):
        current_count = Person.all().count()
        person = Person.add_person("New", "Fellow", "Fellow", wants_accommodation=False)
        self.assertEqual(current_count + 1, Person.all().count())
        self.assertIsNotNone(person.office_id)
        self.assertIsNone(person.living_space_id)

    def test_add_staff_with_location_request(self):
        current_count = Person.all().count()
        person = Person.add_person("New", "Staff", "Staff", wants_accommodation=True)
        self.assertEqual(current_count + 1, Person.all().count())
        self.assertIsNotNone(person.office_id)
        self.assertIsNone(person.living_space_id)

    def test_office_and_living_space(self):
        office = Office.create("New Office")
        ls = LivingSpace.create("New Living Space")
        self.person.add_to_room(office)
        self.person.add_to_room(ls)
        self.assertEqual(self.person.office, office)
        self.assertEqual(self.person.living_space, ls)

    def test_relocate_person(self):
        person = Person.add_person("New", "Per", 'staff')
        office = Office.create("R Office")
        print(office.id, office.name)
        self.assertNotEqual(person.office.id, office.id)
        person.relocate("R Office")
        self.assertEqual(person.office.id, office.id)

    def test_load_people(self):
        current_count = Person.all().count()
        new_people = ['OLUWAFEMI SULE FELLOW Y', 'DOMINIC WALTERS STAFF', 'SIMON PATTERSON FELLOW Y']
        Person.load_people(new_people)
        self.assertEqual(Person.all().count(), current_count + len(new_people))


class FellowTestCase(TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.fellow = Fellow(name="Some Name", role="staff")
        self.fellow.save()

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_class_has_required_attributes(self):
        self.assertTrue(hasattr(Fellow, 'id'))
        self.assertTrue(hasattr(Fellow, 'name'))
        self.assertTrue(hasattr(Fellow, '__table__'))

    def test_class_attributes_mapped_to_right_db_types(self):
        self.assertEqual(type(self.fellow.id), int)
        self.assertEqual(type(self.fellow.name), str)

    def test_class_has_mapped_to_right_table(self):
        self.assertEqual(getattr(Fellow, '__table__').name, 'fellow')

    def test_create(self):
        current_count = Fellow.all().count()
        Fellow.create("New Person")
        self.assertEqual(Fellow.all().count(), current_count+1)


class StaffTestCase(TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.staff = Staff(name="Some Name")
        self.staff.save()

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_class_has_required_attributes(self):
        self.assertTrue(hasattr(Staff, 'id'))
        self.assertTrue(hasattr(Staff, 'name'))
        self.assertTrue(hasattr(Staff, '__table__'))

    def test_class_attributes_mapped_to_right_db_types(self):
        self.assertEqual(type(self.staff.id), int)
        self.assertEqual(type(self.staff.name), str)

    def test_class_has_mapped_to_right_table(self):
        self.assertEqual(getattr(Staff, '__table__').name, 'staff')

    def test_create(self):
        current_count = Staff.all().count()
        Staff.create("New Person")
        self.assertEqual(Staff.all().count(), current_count+1)


class RoomTestCase(TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.room = Room.create("Room Name", "office")

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_create_multiple(self):
        current_count = Room.all().count()
        new_rooms = ["office1", "office2", "office3"]
        Room.create_multiple("office", new_rooms)
        self.assertEqual(Room.all().count(), current_count+len(new_rooms))

    def test_class_has_required_attributes(self):
        self.assertTrue(hasattr(Room, 'id'))
        self.assertTrue(hasattr(Room, 'name'))
        self.assertTrue(hasattr(Room, 'room_type'))
        self.assertTrue(hasattr(Room, '__table__'))

    def test_class_attributes_mapped_to_right_db_types(self):
        self.assertEqual(type(self.room.id), int)
        self.assertEqual(type(self.room.name), str)

    def test_class_has_mapped_to_right_table(self):
        self.assertEqual(getattr(Room, '__table__').name, 'rooms')

    def test_all(self):
        self.assertEqual(1, Room.all().count())
        new_room = Room(name="New Name")
        new_room.save()
        self.assertEquals(2, Room.all().count())

    def test_save(self):
        new_room = Room(name="New Name")
        new_room.save()
        self.assertIn(new_room, Room.all())

    def test_create(self):
        current_count = Room.all().count()
        Room.create("New Room", 'living_space')
        self.assertEqual(Room.all().count(), current_count+1)

    def test_get_people(self):
        office = Office.create("office1")
        staff = Staff.create("New Staff")
        fellow = Fellow.create("New Fellow")
        staff.add_to_room(office)
        fellow.add_to_room(office)
        self.assertIn(fellow, office.get_people().all())
        self.assertIn(staff, office.get_people().all())

    def test_get_by_name(self):
        office = Office.create("office1")
        self.assertEqual(office, Office.get_by_name('office1'))


class OfficeTestCase(TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.office = Office.create("Office Name")

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_class_has_required_attributes(self):
        self.assertTrue(hasattr(Office, 'id'))
        self.assertTrue(hasattr(Office, 'name'))
        self.assertTrue(hasattr(Office, 'available_seats'))
        self.assertTrue(hasattr(Office, '__table__'))

    def test_class_attributes_mapped_to_right_db_types(self):
        self.assertEqual(type(self.office.id), int)
        self.assertEqual(type(self.office.name), str)
        self.assertEqual(type(self.office.available_seats), int)

    def test_class_has_mapped_to_right_table(self):
        self.assertEqual(getattr(Office, '__table__').name, 'office')

    def test_all(self):
        self.assertEqual(1, Office.all().count())
        new_office = Office(name="New Name")
        new_office.save()
        self.assertEquals(2, Office.all().count())

    def test_create(self):
        current_count = Office.all().count()
        Office.create("New Office")
        self.assertEqual(Office.all().count(), current_count+1)


class LivingSpaceTestCase(TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.living_space = LivingSpace.create("Office Name")

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_class_has_required_attributes(self):
        self.assertTrue(hasattr(LivingSpace, 'id'))
        self.assertTrue(hasattr(LivingSpace, 'name'))
        self.assertTrue(hasattr(LivingSpace, 'available_seats'))
        self.assertTrue(hasattr(LivingSpace, '__table__'))

    def test_class_attributes_mapped_to_right_db_types(self):
        self.assertEqual(type(self.living_space.id), int)
        self.assertEqual(type(self.living_space.name), str)
        self.assertEqual(type(self.living_space.available_seats), int)

    def test_class_has_mapped_to_right_table(self):
        self.assertEqual(getattr(LivingSpace, '__table__').name, 'living_space')

    def test_all(self):
        self.assertEqual(1, LivingSpace.all().count())
        new_office = LivingSpace(name="New Name")
        new_office.save()
        self.assertEquals(2, LivingSpace.all().count())

    def test_create(self):
        current_count = LivingSpace.all().count()
        LivingSpace.create("New Office")
        self.assertEqual(LivingSpace.all().count(), current_count+1)