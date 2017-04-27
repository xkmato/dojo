#!/usr/bin/env python
"""The Dojo

Usage:
  dojo.py create_room <room_type> <room_name>...
  dojo.py add_person <first_name> <last_name> <role> [<wants_accommodation>]

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from commands.models import Room, Person


def handle(_arguments):
    if _arguments.get('create_room', None):
        room_name = _arguments.get('<room_name>')
        room_type = _arguments.get('<room_type>').replace(' ', '_').lower()
        new_rooms = Room.create_multiple(room_type, room_name)
        return ["A(n) %s called %s has been successfully created" % (room.room_type.capitalize(), room.name)
                for room in new_rooms]
    elif _arguments.get('add_person', None):
        first_name = _arguments.get('<first_name>')
        last_name = _arguments.get('<last_name>')
        role = _arguments.get('<role>')
        wants_accommodation = True if _arguments.get('<wants_accommodation>') == 'Y' else False
        person = Person.add_person(first_name, last_name, role, wants_accommodation=wants_accommodation)
        result = ["%s %s has been successfully added" % (person.role.capitalize(), person.name),
                  "%s has been allocated the Office %s" % (person.name, person.office.name)]
        if role.lower() == Person.FELLOW and wants_accommodation:
            result.append("%s has been allocated the Living Space %s" % (person.name, person.living_space.name))
        return result

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print('\n'.join(handle(arguments)))