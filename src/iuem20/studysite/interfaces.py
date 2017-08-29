# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective import dexteritytextindexer
from iuem20.studysite import _
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource as CS
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import alsoProvides
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IIuem20StudysiteLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IStudysite(model.Schema):

    model.fieldset('general',
                   label=_(u'general'),
                   fields=['title',
                           'description',
                           'presentation',
                           'image',
                           'img_author',
                           'thumbnail',
                           ])
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'study site label'),
        required=True,
        )
    dexteritytextindexer.searchable('description')
    description = schema.TextLine(
        title=_(u'very short study site description'),
        required=True,
        )
    dexteritytextindexer.searchable('presentation')
    presentation = RichText(
        title=_(u'presentation'),
        description=_(u'study site presentation'),
        required=False
        )
    image = NamedBlobImage(
        title=_(u'main photo'),
        required=True
        )
    img_author = schema.TextLine(
        title=_(u'picture author'),
        required=False,
        )
    thumbnail = NamedBlobImage(
        title=_(u'thumbnail'),
        required=True
        )

    model.fieldset('missions',
                   label=_(u'missions'),
                   fields=['missions',
                           ])
    missions = RelationList(
        title=_(u'related missions'),
        value_type=RelationChoice(
            title=_(u'Target'),
            source=CS(
                portal_type='iuem20.mission')),
        required=False,
        )


alsoProvides(IStudysite, IFormFieldProvider)
