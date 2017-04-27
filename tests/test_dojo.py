from unittest import TestCase
from commands.models import Office, Person
from dojo import handle


class DojoTestCase(TestCase):
    def setUp(self):
        self.arguments = {'<first_name>': 'New', '<last_name>': 'User', '<role>': 'Fellow',
                          '<room_name>': ['office1'], '<room_type>': "office", '<wants_accommodation>': 'N',
                          'add_person': False, 'create_room': True}

    def test_adding_room(self):
        result = ['A(n) Office called office1 has been successfully created']
        self.assertEqual(result, handle(self.arguments))

    def test_adding_staff(self):
        self.arguments['create_room'] = False
        self.arguments['add_person'] = True
        self.arguments['<last_name>'] = 'Staff'
        self.arguments['<role>'] = "Staff"
        result = ['Staff New Staff has been successfully added', 'New Staff has been allocated the Office']
        handled = handle(self.arguments)
        self.assertIn(result[0], handled)
        self.assertEqual(result[1], handled[1][:-7])

    def test_adding_fellow_no_accommodation(self):
        self.arguments['<role>'] = "Fellow"
        self.arguments['create_room'] = False
        self.arguments['add_person'] = True
        self.arguments['<last_name>'] = 'Fellow1'
        result = ['Fellow New Fellow1 has been successfully added', 'New Fellow1 has been allocated the Office',
                  'New Fellow1 has been allocated the Living Space']
        handled = handle(self.arguments)
        self.assertIn(result[0], handled)
        self.assertEqual(result[1], handled[1][:-7])

    def test_adding_fellow_with_accommodation(self):
        self.arguments['create_room'] = False
        self.arguments['add_person'] = True
        self.arguments['<role>'] = "Fellow"
        self.arguments['<last_name>'] = 'Fellow2'
        result = ['Fellow New Fellow2 has been successfully added', 'New Fellow2 has been allocated the Office',
                  'New Fellow2 has been allocated the Living Space']
        self.arguments['<wants_accommodation>'] = 'Y'
        self.assertEqual(result[2], handle(self.arguments)[2][:-7])

    def test_print_room_non_existent_room(self):
        self.arguments = {'<first_name>': None, '<last_name>': None, '<role>': None, '<room_name>': ['office5'],
                          '<room_type>': None, '<wants_accommodation>': None, 'add_person': False, 'create_room': False,
                          'print_room': True}
        result = ['Ooops.. Room Does not exist']
        self.assertEqual(result, handle(self.arguments))

    def test_print_room_empty_room(self):
        Office.create("office2")
        self.arguments = {'<first_name>': None, '<last_name>': None, '<role>': None, '<room_name>': ['office2'],
                          '<room_type>': None, '<wants_accommodation>': None, 'add_person': False, 'create_room': False,
                          'print_room': True}
        result = ['No one here yet']
        self.assertEqual(result, handle(self.arguments))

    def test_print_room(self):
        person = Person.add_person("New", "Person", "staff")
        self.arguments = {'<first_name>': None, '<last_name>': None, '<role>': None,
                          '<room_name>': [person.office.name], '<room_type>': None, '<wants_accommodation>': None,
                          'add_person': False, 'create_room': False, 'print_room': True}
        self.assertIn('%s, %s' % (person.name, person.role), handle(self.arguments))

    def test_print_allocations(self):
        self.arguments = {'<first_name>': None, '<last_name>': None, '<role>': None, '<room_name>': [],
                          '<room_type>': None, '<wants_accommodation>': None, 'add_person': False, 'create_room': False,
                          'print_allocations': True, 'print_room': False}
        self.assertListEqual(["%s in %s Office and %s Living Space" % allocation
                              for allocation in Person.get_allocations()], handle(self.arguments))