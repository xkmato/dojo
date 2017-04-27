from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///:memory:')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Person(Base):
    __tablename__ = 'people'

    STAFF = 'staff'
    FELLOW = 'fellow'
    ROLES = [STAFF, FELLOW]

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    role = Column(String(250))
    office_id = Column(Integer, nullable=True)
    living_space_id = Column(Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'people',
        'polymorphic_on': role,
        'with_polymorphic': '*'
    }

    def __eq__(self, other):
        return self.id == other.id and isinstance(self, Person)

    @property
    def office(self):
        return session.query(Office).get(self.office_id)

    @property
    def living_space(self):
        return session.query(LivingSpace).get(self.living_space_id)

    def save(self):
        session.add(self)
        session.commit()
        return self

    def add_to_room(self, room):
        print(room.available_seats)
        print(room.id, room.room_type, room.name)
        if room.available_seats > 0:
            room.reduce_available_seats()
            if room.room_type == Room.OFFICE:
                self.office_id = room.id
            else:
                self.living_space_id = room.id
            self.save()


    @classmethod
    def all(cls):
        return session.query(cls)

    @classmethod
    def create(cls, name, role):
        if role not in cls.ROLES:
            raise ValueError("Role should be either of %s" % " or ".join(cls.ROLES))
        if role == cls.STAFF:
            person = Staff.create(name)
        else:
            person = Fellow.create(name)
        return person

    @classmethod
    def add_person(cls, first_name, last_name, role, wants_accommodation=False):
        name = "%s %s" % (first_name, last_name)
        role = role.lower()
        person = cls.create(name, role)
        room = Office.get_or_create(name)
        person.add_to_room(room)
        if wants_accommodation and role == Person.FELLOW:
            room = LivingSpace.get_or_create(name)
            person.add_to_room(room)
        return person


class Fellow(Person):
    __tablename__ = 'fellow'

    id = Column(Integer, ForeignKey('people.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'fellow',
    }

    @classmethod
    def create(cls, name, role=Person.FELLOW):
        return cls(name=name, role=role).save()


class Staff(Person):
    __tablename__ = 'staff'

    id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    @classmethod
    def create(cls, name, role=Person.STAFF):
        return cls(name=name, role=role).save()


class Dojo(object):
    pass


class Room(Base):
    __tablename__ = 'rooms'

    OFFICE = 'office'
    LIVING_SPACE = 'living space'
    KINDS = [OFFICE, LIVING_SPACE]

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    room_type = Column(String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'rooms',
        'polymorphic_on': room_type,
        'with_polymorphic': '*'
    }

    def reduce_available_seats(self):
        self.available_seats -= 1
        self.save()

    def save(self):
        session.add(self)
        session.commit()
        return self

    def get_people(self):
        return session.query(Person).filter(or_(Person.office_id == self.id, Person.living_space_id == self.id))

    @classmethod
    def get_or_create(cls, name=None):
        available = session.query(cls).filter(cls.available_seats > 0).one_or_none()
        if available:
            return available
        return cls.create(name)

    @classmethod
    def all(cls):
        return session.query(cls)

    @classmethod
    def create(cls, name, room_type):
        if room_type not in cls.KINDS:
            raise ValueError("Room Type must be either of %s" % " or ".join(cls.KINDS))
        if room_type == cls.LIVING_SPACE:
            return LivingSpace.create(name)
        if room_type == cls.OFFICE:
            return Office.create(name)

    @classmethod
    def create_multiple(cls, room_type, room_names):
        return [cls.create(name, room_type) for name in room_names]


class Office(Room):
    __tablename__ = "office"

    id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    available_seats = Column(Integer, default=6)

    __mapper_args__ = {
        'polymorphic_identity': 'office',
    }

    @classmethod
    def create(cls, name, room_type=Room.OFFICE):
        return cls(name=name, room_type=room_type).save()


class LivingSpace(Room):
    __tablename__ = "living_space"

    id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    available_seats = Column(Integer, default=4)

    __mapper_args__ = {
        'polymorphic_identity': 'living_space',
    }

    @classmethod
    def create(cls, name, room_type=Room.LIVING_SPACE):
        return cls(name=name, room_type=room_type).save()

Base.metadata.create_all()