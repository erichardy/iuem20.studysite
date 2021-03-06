# -*- coding: utf-8 -*-
"""
Nous auront besoin des references :
http://docs.plone.org/external/plone.app.dexterity/docs/advanced/references.html
pour associer un projet a des missions et des portraits.
"""

from iuem20.studysite import _
from iuem20.studysite.interfaces import IStudysite
from plone import api
from plone.dexterity.browser import add
from plone.dexterity.content import Container
from plonetheme.iuem20.utils import getGalleryImages as ggi
from plonetheme.iuem20.utils import canView
# from Products.CMFPlone.utils import safe_unicode
from z3c.form import button
from zope.interface import implementer
from zope.publisher.browser import BrowserView

import logging


logger = logging.getLogger('iuem20 STUDYSITE')


class StudySiteView(BrowserView):
    def getGalleryImages(self):
        logger.info('getGalleryImages iuem20 STUDYSITE')
        return ggi(self.context)

    def getMissions(self):
        missions = [mission.to_object
                    for mission in self.context.missions
                    if canView(mission.to_object)]
        return missions

@implementer(IStudysite)
class studysite(Container):

    def _toHTML(self, ch):
        s = ch.replace('\'', '&rsquo;').\
            replace('"', '&rdquo;')
        return s

    def getMissions(self):
        return [mission.to_object for mission in self.missions]

    def getImgAuthor(self):
        if not self.img_author:
            return False
        return self.img_author

    def getPresentation(self):
        """
        :return: Le texte en français en format ``output`` s'il existe.
           Sinon ``False``
        """
        try:
            if len(self.presentation.output) < 6:
                # logger.info('inf a 6')
                return False
            else:
                return self.presentation.output
        except Exception:
            # logger.info('excepppppp')
            return False

    def getMissionsLabel(self):
        try:
            return self.missions_label
        except Exception:
            return u''


class AddForm(add.DefaultAddForm):
    portal_type = 'iuem20.studysite'
    ignoreContext = True
    label = _(u'Add a new study site !')

    def update(self):
        super(add.DefaultAddForm, self).update()
        # logger.info('update()')

    def updateWidgets(self):
        super(add.DefaultAddForm, self).updateWidgets()
        # logger.info('updateWidgets()')

    @button.buttonAndHandler(_(u'Save this study site'),
                             name='save_this_studysite')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return
        try:
            obj = self.createAndAdd(data)
            logger.info(obj.absolute_url())
            contextURL = self.context.absolute_url()
            self.request.response.redirect(contextURL)
        except Exception:
            raise

    @button.buttonAndHandler(_(u'Cancel this study site'))
    def handleCancel(self, action):
        data, errors = self.extractData()
        # context is the thesis repo
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


class AddView(add.DefaultAddView):
    form = AddForm
