from unittest import TestCase
from dojo import handle


class DojoTestCase(TestCase):
    def setUp(self):
        self.arguments = {'<first_name>': 'Kenneth', '<last_name>': 'Matovu', '<role>': 'Fellow',
                          '<room_name>': ['office1'], '<room_type>': "office", '<wants_accommodation>': 'N',
                          'add_person': False, 'create_room': True}

    def test_adding_room(self):
        result = ['A(n) Office called office1 has been successfully created']
        self.assertEqual(result, handle(self.arguments))

    def test_adding_staff(self):
        self.arguments['create_room'] = False
        self.arguments['add_person'] = True
        self.arguments['<role>'] = "Staff"
        result = ['Staff Kenneth Matovu has been successfully added',
                  'Kenneth Matovu has been allocated the Office']
        self.assertIn(result[0], handle(self.arguments))
        self.assertIn(result[1], handle(self.arguments)[1][:-7])

    def test_adding_fellow_no_accommodation(self):
        self.arguments['<role>'] = "Fellow"
        self.arguments['create_room'] = False
        self.arguments['add_person'] = True
        result = ['Fellow Kenneth Matovu has been successfully added', 'Kenneth Matovu has been allocated the Office',
                  'Kenneth Matovu has been allocated the Living Space']
        self.assertIn(result[0], handle(self.arguments))
        self.assertIn(result[1], handle(self.arguments)[1][:-7])

    def test_adding_fellow_with_accommodation(self):
        self.arguments['create_room'] = False
        self.arguments['add_person'] = True
        self.arguments['<role>'] = "Fellow"
        result = ['Fellow Kenneth Matovu has been successfully added', 'Kenneth Matovu has been allocated the Office',
                  'Kenneth Matovu has been allocated the Living Space']
        self.arguments['<wants_accommodation>'] = 'Y'
        self.assertIn(result[2], handle(self.arguments)[2][:-7])