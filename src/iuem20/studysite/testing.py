# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import iuem20.studysite


class Iuem20StudysiteLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=iuem20.studysite)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'iuem20.studysite:default')


IUEM20_STUDYSITE_FIXTURE = Iuem20StudysiteLayer()


IUEM20_STUDYSITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IUEM20_STUDYSITE_FIXTURE,),
    name='Iuem20StudysiteLayer:IntegrationTesting'
)


IUEM20_STUDYSITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IUEM20_STUDYSITE_FIXTURE,),
    name='Iuem20StudysiteLayer:FunctionalTesting'
)


IUEM20_STUDYSITE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IUEM20_STUDYSITE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='Iuem20StudysiteLayer:AcceptanceTesting'
)
