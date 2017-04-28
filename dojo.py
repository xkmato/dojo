#!/usr/bin/env python
"""
Some of the code in this file is copied as is from docopt CMD example
Usage:
  dojo create_room <room_type> <room_name>...
  dojo add_person <first_name> <last_name> <role> [<wants_accommodation>]
  dojo print_room <room_name>
  dojo relocate <person_identifier> <new_room_name>
  dojo print_allocations [--o=FILENAME]
  dojo add_people <file_name>
  dojo load_state <sqlite_database>
  dojo save_state [--db=sqlite_database]
  dojo -i

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from commands.handler import handle


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class DojoInterface (cmd.Cmd):
    intro = 'Welcome to Dojo room assigner' \
        + ' (type help when you get stuck)'
    prompt = '(dojo) '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""

        arg.update(dict(create_room=True))
        [print(line) for line in handle(arg)]

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <role> [<wants_accommodation>]"""

        arg.update(dict(add_person=True))
        [print(line) for line in handle(arg)]

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: add_person <room_name> """

        arg.update(dict(add_person=True))
        [print(line) for line in handle(arg)]

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=FILENAME] """

        arg.update(dict(print_allocations=True))
        [print(line) for line in handle(arg)]

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name> """

        arg.update(dict(load_people=True))
        [print(line) for line in handle(arg)]

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database] """

        arg.update(dict(save_state=True))
        [print(line) for line in handle(arg)]

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database> """

        arg.update(dict(load_state=True))
        [print(line) for line in handle(arg)]

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

if __name__ == "__main__":
    opt = docopt(__doc__, sys.argv[1:])

    DojoInterface().cmdloop()
