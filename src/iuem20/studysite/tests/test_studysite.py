# -*- coding: utf-8 -*-
from iuem20.studysite.interfaces import Istudysite
from iuem20.studysite.testing import IUEM20_STUDYSITE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class studysiteIntegrationTest(unittest.TestCase):

    layer = IUEM20_STUDYSITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='studysite')
        schema = fti.lookupSchema()
        self.assertEqual(Istudysite, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='studysite')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='studysite')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(Istudysite.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='studysite',
            id='studysite',
        )
        self.assertTrue(Istudysite.providedBy(obj))
