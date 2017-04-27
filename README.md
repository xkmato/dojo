# The Dojo - Automatic Room assignment

[![Build Status](https://travis-ci.org/xkmato/dojo.svg?branch=master)](https://travis-ci.org/xkmato/dojo)


### How it works

#### To start interactive shell; use `./dojo.py -i`

- `create_room <room_type> <room_name>...` Create new room of type room_type and name room_name
- `add_person <first_name> <last_name> <role> [<wants_accommodation>]` Add new person and allocate room to them
- `print_room <room_name>` Print room and it's occupant
- `relocate <person_identifier> <new_room_name>` Relocate person to new Room
- `print_allocations [-o=FILENAME]` Print allocations
- `add_people <file_name>` Add multiple people from file