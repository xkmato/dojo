from shutil import copyfile
from commands.models import Person, Room


def handle(_arguments):
    """Handle commands and argument"""

    try:
        if _arguments.get('create_room'):
            room_name = _arguments.get('<room_name>')
            room_type = _arguments.get('<room_type>').replace(' ', '_').lower()
            new_rooms = Room.create_multiple(room_type, room_name)
            return ["A(n) %s called %s has been successfully created" % (room.room_type.capitalize(), room.name)
                    for room in new_rooms]

        elif _arguments.get('add_person'):
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

        elif _arguments.get('print_room'):
            room = Room.get_by_name(_arguments.get('<room_name>')[0])
            if room:
                return [", ".join([person.name, person.role]) for person in room.get_people()] or ['No one here yet']
            return ['Ooops.. Room Does not exist']

        elif _arguments.get('print_allocations'):
            return ["%s in %s Office and %s Living Space" % allocation for allocation in Person.get_allocations()]

        elif _arguments.get('relocate_person'):
            person = Person.all().get(int(_arguments.get("<person_identifier>")))
            room_name = _arguments.get("<new_room_name>")
            person.relocate(room_name)
            return ['%s has been relocated to %s' % (person.name, room_name)]

        elif _arguments.get('load_people'):
            file = open(_arguments.get("<file_name>"))
            people_list = file.readlines()
            people = Person.load_people(people_list)
            p = []
            for key in people:
                text = "%s\n------------------------------------\n %s" % (key, ", ".join(people[key]))
                p.append(text)
            return p
        elif _arguments.get('save_state'):
            db_file = _arguments.get('--db')
            copyfile('dojo.db', db_file)
            return ["Data successfully saved to %s" % db_file]
        elif _arguments.get('load_state'):
            db_file = _arguments.get('<sqlite_database>')
            copyfile(db_file, 'dojo.db')
            return ["Data successfully loaded from %s" % db_file]
    except KeyboardInterrupt:
        return
    except Exception as e:
        return ["Ooops Something unexpected happened: %s" % str(e)]