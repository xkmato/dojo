from unittest import TestCase
from dojo import handle


class DojoTestCase(TestCase):
    def test_handle(self):
        arguments = {'<first_name>': 'Kenneth', '<last_name>': 'Matovu', '<role>': 'Fellow', '<room_name>': ['office1'],
                     '<room_type>': "office", '<wants_accommodation>': 'N', 'add_person': False, 'create_room': True}

        result = ['A(n) Office called office1 has been successfully created']
        self.assertEqual(result, handle(arguments))  # Adding Room

        arguments['create_room'] = False
        arguments['add_person'] = True
        arguments['<role>'] = "Staff"
        result = ['Staff Kenneth Matovu has been successfully added',
                  'Kenneth Matovu has been allocated the Office']  # Adding Staff
        self.assertIn(result[0], handle(arguments))
        self.assertIn(result[1], handle(arguments)[1][:-7])

        arguments['<role>'] = "Fellow"
        result = ['Fellow Kenneth Matovu has been successfully added', 'Kenneth Matovu has been allocated the Office',
                  'Kenneth Matovu has been allocated the Living Space']  # Adding Fellow No accommodation
        self.assertIn(result[0], handle(arguments))
        self.assertIn(result[1], handle(arguments)[1][:-7])

        arguments['<wants_accommodation>'] = 'Y'
        self.assertIn(result[2], handle(arguments)[2][:-7])