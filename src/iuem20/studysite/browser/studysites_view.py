# -*- coding: utf-8 -*-

from iuem20.studysite import _
from plone import api
from plonetheme.iuem20.utils import sort_by_position
from zope.publisher.browser import BrowserView

import logging


logger = logging.getLogger('iuem20.studysite')


class studySitesView(BrowserView):

    title = _(u'studysites_view')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getStudySitesObjs(self,
                          effective=False):
        """
        :param effective: si ``True``, tri par date de publication
        :type effective: Boolean
        :return: liste des sites d'étude triés par disposition dans le
          dossier, ou par ordre de date de publication. Pour les sites
          d'étude, c'est la date de publication qui est choisie.
        """
        portal = api.portal.get()
        founds = api.content.find(context=portal,
                                  portal_type='iuem20.studysite',
                                  path='/'.join(portal.getPhysicalPath()),
                                  depth=9,
                                  )
        # logger.info(founds)
        if len(founds) == 0:
            return False
        objs = [found.getObject() for found in founds]
        if effective:
            sortedObjs = sorted(objs,
                                key=lambda obj: obj.effective(),
                                reverse=True)
            return sortedObjs
        return sorted(objs, sort_by_position)
