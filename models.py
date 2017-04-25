from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///:memory:')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Person(Base):
    __tablename__ = 'people'

    STAFF = 'staff'
    FELLOW = 'fellows'
    ROLES = [STAFF, FELLOW]

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    role = Column(String(250))
    room_id = Column(Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'people',
        'polymorphic_on': role,
        'with_polymorphic': '*'
    }

    def save(self):
        session.add(self)
        session.commit()
        return self

    def add_to_room(self, room):
        self.room_id = room.id
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


class Fellow(Person):
    __tablename__ = 'fellows'

    id = Column(Integer, ForeignKey('people.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'fellows',
    }

    @classmethod
    def create(cls, name):
        return cls(name=name).save()


class Staff(Person):
    __tablename__ = 'staff'

    id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    @classmethod
    def create(cls, name):
        return cls(name=name).save()


class Dojo(object):
    pass


class Room(Base):
    __tablename__ = 'rooms'

    OFFICE = 'offices'
    LIVING_SPACE = 'living spaces'
    KINDS = [OFFICE, LIVING_SPACE]

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    kind = Column(String(250))

    __mapper_args__ = {
        'polymorphic_identity': 'rooms',
        'polymorphic_on': kind,
        'with_polymorphic': '*'
    }

    def save(self):
        session.add(self)
        session.commit()
        return self

    @classmethod
    def all(cls):
        return session.query(cls)

    @classmethod
    def create(cls, name, kind):
        if kind not in cls.KINDS:
            raise ValueError("Kind must be either of %s" % " or ".join(cls.KINDS))
        if kind == cls.LIVING_SPACE:
            return LivingSpace.create(name)
        if kind == cls.OFFICE:
            return Office.create(name)


class Office(Room):
    __tablename__ = "offices"

    id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    unused_seats = Column(Integer, default=6)

    @classmethod
    def create(cls, name):
        return cls(name=name).save()


class LivingSpace(Room):
    __tablename__ = "living_spaces"

    id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    unused_seats = Column(Integer, default=4)

    @classmethod
    def create(cls, name):
        return cls(name=name).save()