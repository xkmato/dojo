#!/usr/bin/env python
"""The Dojo

Usage:
  dojo.py create_room <room_type> <room_name>...
  dojo.py add_person <first_name> <last_name> <role> [<wants_accommodation>]
  dojo.py print_room <room_name>
  dojo.py print_allocations [-o=FILENAME]

Options:
  -h --help     Show this screen.
  -o=FILENAME   Path to output file
  --version     Show version.

"""
from docopt import docopt
from commands.models import Room, Person, Office, LivingSpace


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

    elif _arguments.get('print_room', None):
        room = Room.get_by_name(_arguments.get('<room_name>')[0])
        if room:
            return [", ".join([person.name, person.role]) for person in room.get_people()] or ['No one here yet']
        return ['Ooops.. Room Does not exist']

    elif _arguments.get('print_allocations', None):
        return ["%s in %s Office and %s Living Space" % allocation for allocation in Person.get_allocations()]

if __name__ == '__main__':
    arguments = docopt(__doc__)
    if not arguments.get('-o'):
        print('\n'.join(handle(arguments)))
    else:
        output_file = open(arguments.get('-o').lstrip('='), 'a')
        output_file.write('\n'.join(handle(arguments)))