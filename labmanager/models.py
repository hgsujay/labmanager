# -*-*- encoding: utf-8 -*-*-
# 
# lms4labs is free software: you can redistribute it and/or modify
# it under the terms of the BSD 2-Clause License
# lms4labs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

"""
  :copyright: 2012 Pablo Orduña, Elio San Cristobal, Alberto Pesquera Martín
  :license: BSD, see LICENSE for more details
"""

from sqlalchemy import Column, Integer, Unicode, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relation, backref, relationship
from labmanager.database import Base

class LMS(Base):

    __tablename__ = 'LMSs'

    id = Column(Integer, primary_key=True)


    name                = Column(Unicode(50), nullable = False)
    url                 = Column(Unicode(300), nullable = False) # remote url

    lms_login           = Column(Unicode(50), nullable = False, unique=True)
    lms_password        = Column(Unicode(50), nullable = False) # hash
    
    labmanager_login    = Column(Unicode(50), nullable = False)
    labmanager_password = Column(Unicode(50), nullable = False) # plaintext: my password there

    def __init__(self, name = None, url = None, lms_login = None, lms_password = None, labmanager_login = None, labmanager_password = None):
        self.name                = name
        self.url                 = url
        self.lms_login           = lms_login
        self.lms_password        = lms_password
        self.labmanager_login    = labmanager_login
        self.labmanager_password = labmanager_password


class LabManagerUser(Base):
    __tablename__ = 'LabManagerUsers'

    id = Column(Integer, primary_key=True)

    login    = Column(Unicode(50),  unique = True ) 
    name     = Column(Unicode(50) )
    password = Column(Unicode(50)) # hash

    def __init__(self, login = None, name = None, password = None):
        self.login    = login
        self.name     = name
        self.password = password


class RLMSType(Base):
    __tablename__ = 'RLMS_types'

    id = Column(Integer, primary_key = True)

    name    = Column(Unicode(50), unique = True)

    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return 'RLMSType(%r)' % self.name

class RLMSTypeVersion(Base):
    __tablename__  = 'RLMS_type_versions'
    __table_args__ = (UniqueConstraint('rlms_type_id', 'version'), )

    id = Column(Integer, primary_key = True)

    rlms_type_id = Column(Integer, ForeignKey('RLMS_types.id'), nullable = False)
    version = Column(Unicode(50))

    rlms_type = relation(RLMSType.__name__, backref = backref('versions', order_by=id, cascade = 'all,delete'))

    def __init__(self, rlms_type = None, version = None):
        self.rlms_type = rlms_type
        self.version   = version


class RLMS(Base):
    __tablename__ = 'RLMSs'
    
    id = Column(Integer, primary_key = True)

    name     = Column(Unicode(100), nullable = False)
    location = Column(Unicode(100), nullable = False)
    rlms_version_id = Column(Integer, ForeignKey('RLMS_type_versions.id'), nullable = False)

    configuration = Column(Unicode(10 * 1024)) # JSON document
    
    rlms_version = relation(RLMSTypeVersion.__name__, backref = backref('rlms', order_by=id, cascade = 'all,delete'))

    def __init__(self, name = None, location = None, rlms_version = None, configuration = None):
        self.name          = name
        self.location      = location
        self.rlms_version  = rlms_version
        self.configuration = configuration

class Laboratory(Base):
    __tablename__ = 'Laboratories'
    __table_args__ = (UniqueConstraint('laboratory_id', 'rlms_id'), )

    id = Column(Integer, primary_key = True)

    name          = Column(Unicode(50), nullable = False)
    laboratory_id = Column(Unicode(50), nullable = False)
    rlms_id       = Column(Integer, ForeignKey('RLMSs.id'), nullable = False)

    rlms          = relation(RLMS.__name__, backref = backref('laboratories', order_by=id, cascade = 'all,delete'))

    def __init__(self, name = None, laboratory_id = None, rlms = None):
        self.name          = name
        self.laboratory_id = laboratory_id
        self.rlms          = rlms


class PermissionOnLaboratory(Base):
    __tablename__ = 'PermissionOnLaboratories'
    __table_args__ = (UniqueConstraint('laboratory_id', 'lms_id'), UniqueConstraint('local_identifier', 'lms_id'))

    id = Column(Integer, primary_key = True)

    local_identifier     = Column(Unicode(100), nullable = False, index = True)

    laboratory_id = Column(Integer, ForeignKey('Laboratories.id'), nullable = False)
    lms_id        = Column(Integer, ForeignKey('LMSs.id'),  nullable = False)

    configuration = Column(Unicode(10 * 1024)) # JSON document

    laboratory = relation(Laboratory.__name__,  backref = backref('permissions', order_by=id, cascade = 'all,delete'))
    lms        = relation(LMS.__name__, backref = backref('permissions', order_by=id, cascade = 'all,delete'))

    def __init__(self, lms = None, laboratory = None, configuration = None, local_identifier = None):
        self.lms              = lms
        self.laboratory       = laboratory
        self.configuration    = configuration
        self.local_identifier = local_identifier


class Course(Base):
    __tablename__  = 'Courses'
    __table_args__ = (UniqueConstraint('course_id', 'lms_id'), )

    id = Column(Integer, primary_key = True)

    # The ID in the remote LMS
    course_id = Column(Unicode(50), nullable = False)

    name   = Column(Unicode(50), nullable = False)

    lms_id = Column(Integer, ForeignKey('LMSs.id'), nullable = False)

    lms  = relation(LMS.__name__, backref = backref('courses', order_by=id, cascade = 'all,delete'))

    def __init__(self, lms = None, course_id = None, name = None):
        self.course_id = course_id
        self.name      = name
        self.lms       = lms

class PermissionOnCourse(Base):
    __tablename__  = 'PermissionOnCourses'
    __table_args__ = (UniqueConstraint('course_id', 'permission_on_lab_id'),)
    
    id = Column(Integer, primary_key = True)

    configuration        = Column(Unicode(10 * 1024)) # JSON document

    permission_on_lab_id = Column(Integer, ForeignKey('PermissionOnLaboratories.id'), nullable = False)
    course_id            = Column(Integer, ForeignKey('Courses.id'), nullable = False)

    permission_on_lab    = relation(PermissionOnLaboratory.__name__, backref = backref('course_permissions', order_by=id, cascade = 'all,delete'))
    course               = relation(Course.__name__, backref = backref('permissions', order_by=id, cascade = 'all,delete'))

    def __init__(self, permission_on_lab = None, course = None, configuration = None):
        self.permission_on_lab = permission_on_lab
        self.course            = course
        self.configuration     = configuration


class NewLMS(Base):
    __tablename__  = 'newlms'
    id = Column(Integer, primary_key = True)
    name = Column(Unicode(50), nullable = False)
    url = Column(Unicode(300), nullable = False)

    permissions_on_experiments = relationship('Permission', backref=backref('LMS', order_by=id))
    authentication = relationship('Credential', backref=backref('LMS', order_by=id))
    courses = relationship('NewCourse', backref=backref('LMS', order_by=id))


    def __init__(self, name = None, url = None):
        self.name = name
        self.url = url

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name
        

class Credential(Base):
    __tablename__  = 'credential'
    id = Column(Integer, primary_key = True)
    lms_id = Column(Integer, ForeignKey('newlms.id'), nullable = False)
    key = Column(Unicode(50), nullable = False, unique=True)
    secret = Column(Unicode(50), nullable = False)
    type = Column(Unicode(50), nullable = False)

    def __init__(self, key = None, secret = None, type = None):
        self.key = key
        self.secret = secret
        self.type = type

class Permission(Base):
    __tablename__  = 'permission'
    id = Column(Integer, primary_key = True)
    lms_id = Column(Integer, ForeignKey('newlms.id'), nullable = False)
    context_id = Column(Unicode(50), nullable = False)
    resource_link_id = Column(Integer, nullable = False)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable = False)
    access = Column(Integer, nullable = False)

    def __init__(self, lms_id = None, context_id = None, resource_link_id = None,
                 experiment_id = None, access = None):
        self.lms_id = lms_id
        self.context_id = context_id
        self.resource_link_id = resource_link_id
        self.experiment_id = experiment_id
        self.access = access


class Experiment(Base):
    __tablename__  = 'experiment'
    id = Column(Integer, primary_key = True)
    name = Column(Unicode(50), nullable = False)
    rlms_version = Column(Integer, nullable = False) # Foreign key to RLMS
    url = Column(Unicode(300), nullable = False)
    permissions = relationship('Permission', backref=backref('Experiment',order_by=id))

    def __init__(self, name = None, rlms_version = None, url = None):
        self.name = name
        self.rlms_version = rlms_version
        self.url = url

    def __repr__(self):
        return "%s version %s" % (self.name, self.rlms_version)

class NewCourse(Base):
    __tablename__ = 'newcourse'
    id = Column(Integer, primary_key = True)
    name = Column(Unicode(50), nullable = False)
    lms_id = Column(Integer, ForeignKey('newlms.id'), nullable = False)

    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return "%s from %s" % (self.name, self.lms_id)
