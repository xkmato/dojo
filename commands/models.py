import random
import string
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///dojo.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Person(Base):
    """Person Model for either Staff or Fellow"""

    __tablename__ = 'people'

    STAFF = 'staff'
    FELLOW = 'fellow'
    ROLES = [STAFF, FELLOW]

    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    role = Column(String(250))
    office_id = Column(Integer, nullable=True)
    living_space_id = Column(Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'people',
        'polymorphic_on': role,
        'with_polymorphic': '*'
    }

    def __eq__(self, other):
        return self.id == other.id and isinstance(self, Person) and isinstance(other, Person)

    @property
    def office(self):
        return session.query(Office).get(self.office_id)

    @property
    def living_space(self):
        return session.query(LivingSpace).get(self.living_space_id)

    def relocate(self, room_name):
        """Relocate user to different Room"""

        room = Room.get_by_name(room_name)
        if room.room_type == Room.OFFICE:
            self.office_id = room.id
        else:
            self.living_space_id = room.id
        self.save()

    def save(self):
        session.add(self)
        session.commit()
        return self

    def add_to_room(self, room):
        """Add user to Room """
        if room.available_seats > 0:
            room.reduce_available_seats()
            if room.room_type == Room.OFFICE:
                self.office_id = room.id
            else:
                self.living_space_id = room.id
            self.save()

    @classmethod
    def all(cls):
        """Return QuerySet of all users"""

        return session.query(cls)

    @classmethod
    def create(cls, name, role):
        """Create New Person"""

        if role not in cls.ROLES:
            raise ValueError("Role should be either of %s" % " or ".join(cls.ROLES))
        if role == cls.STAFF:
            person = Staff.create(name)
        else:
            person = Fellow.create(name)
        return person

    @classmethod
    def add_person(cls, first_name, last_name, role, wants_accommodation=False):
        """Adding person with Rooms f available """

        if wants_accommodation == 'Y':
            wants_accommodation = True
        name = "%s %s" % (first_name.capitalize(), last_name.capitalize())
        role = role.lower()
        person = cls.create(name, role)
        room = Office.get_or_create(name)
        person.add_to_room(room)
        if wants_accommodation and role == Person.FELLOW:
            room = LivingSpace.get_or_create(name)
            person.add_to_room(room)
        return person

    @classmethod
    def get_allocations(cls):
        """Return Person and Room they are assigned to"""

        allocations = []
        for person in Person.all():
            if person.living_space_id:
                allocations.append((person.name, person.office.name, person.living_space.name))
            else:
                allocations.append((person.name, person.office.name, "No"))
        return allocations

    @classmethod
    def load_people(cls, people):
        """Load multiple people from a file"""

        rooms = {}

        def add_to_rooms(room, _person):
            if room.name in rooms:
                rooms[room.name].append(_person.name)
            else:
                rooms[room.name] = [_person.name]

        for person in people:
            _p = Person.add_person(*[p.strip() for p in person.split()])
            if _p.office_id:
                add_to_rooms(_p.office, _p)
            if _p.living_space_id:
                add_to_rooms(_p.living_space, _p)

        return rooms


class Fellow(Person):
    """This is class that represents a fellow"""

    __tablename__ = 'fellow'

    id = Column(Integer, ForeignKey('people.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'fellow',
    }

    @classmethod
    def create(cls, name, role=Person.FELLOW):
        """Method for creating a Fellow"""

        return cls(name=name, role=role).save()


class Staff(Person):
    """Class that represents Staff"""

    __tablename__ = 'staff'

    id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    @classmethod
    def create(cls, name, role=Person.STAFF):
        """Method for creating a Staff"""

        return cls(name=name, role=role).save()


class Dojo(object):
    pass


class Room(Base):
    """Class that Represents Room"""

    __tablename__ = 'rooms'

    OFFICE = 'office'
    LIVING_SPACE = 'living_space'
    KINDS = [OFFICE, LIVING_SPACE]

    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    available_seats = Column(Integer)
    room_type = Column(String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'rooms',
        'polymorphic_on': room_type,
        'with_polymorphic': '*'
    }

    def reduce_available_seats(self):
        """Reduce number of available seats by one whenever a new user is added"""

        self.available_seats -= 1
        self.save()

    def save(self):
        """Method to save Object into db. Does both update and insert SQL Queries"""

        session.add(self)
        session.commit()
        return self

    def get_people(self):
        """Return people in this Room"""

        return session.query(Person).filter(or_(Person.office_id == self.id, Person.living_space_id == self.id))

    @classmethod
    def get_or_create(cls, name=None):
        """Get available Room or Create a new one"""

        available = session.query(cls).filter(cls.available_seats > 0).first()
        if available:
            return available
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return cls.create(name)

    @classmethod
    def all(cls):
        """Return QuerySet of all Rooms"""

        return session.query(cls)

    @classmethod
    def create(cls, name, room_type):
        """Method to create New room"""

        if room_type not in cls.KINDS:
            raise ValueError("Room Type must be either of %s" % " or ".join(cls.KINDS))
        if room_type == cls.LIVING_SPACE:
            return LivingSpace.create(name)
        if room_type == cls.OFFICE:
            return Office.create(name)

    @classmethod
    def create_multiple(cls, room_type, room_names):
        """Create multiple rooms of the same type"""

        return [cls.create(name, room_type) for name in room_names]

    @classmethod
    def get_by_name(cls, name):
        """Return a room with NAME"""

        return session.query(cls).filter(cls.name == name).first()


class Office(Room):
    """Class that Represents an Office"""

    __tablename__ = "office"

    id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    available_seats = Column(Integer, default=6)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
    }

    @classmethod
    def create(cls, name, room_type=Room.OFFICE):
        """Create new office"""

        return cls(name=name, room_type=room_type).save()


class LivingSpace(Room):
    """Class that represents a Living Space"""

    __tablename__ = "living_space"

    id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    available_seats = Column(Integer, default=4)

    __mapper_args__ = {
        'polymorphic_identity': 'living_space',
    }

    @classmethod
    def create(cls, name, room_type=Room.LIVING_SPACE):
        """Create new living space"""

        return cls(name=name, room_type=room_type).save()

Base.metadata.create_all()