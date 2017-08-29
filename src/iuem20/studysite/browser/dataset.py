# -*- coding: utf-8 -*-

from os.path import abspath
from os.path import dirname
from os.path import join
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.namedfile import NamedBlobImage
from z3c.relationfield.relation import RelationValue
# from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.publisher.browser import BrowserView

import logging


PREFIX = abspath(dirname(__file__))
logger = logging.getLogger('iuem20.project: CREATEDATASET')


def input_image_path(f):
    return join(PREFIX, '../tests/images/', f)


lorem = """
Vivamus dictum, nunc a tincidunt semper, lectus justo maximus neque,
et pulvinar ipsum dolor at nisl. Maecenas porttitor dolor nec ante cursus
viverra. Maecenas massa nunc, semper vitae pulvinar at, semper
at metus. Cras a fermentum diam. Sed a lobortis
risus, efficitur tincidunt lorem.
"""

bio_fr_text = """
<h4>Savoir-faire opérationnels</h4>
<ul>
<li>Utiliser les méthodes de prévention et
de gestion des risques<br/></li>
</ul>
<h4>Lieu d'exercice</h4>
<ul>
<li>L’activité s’exerce généralement au sein d'un service informatique<br/>
</li>
</ul>
<h3>Dipl&ocirc;me exig&eacute;</h3>
<ul>
<li>Doctorat, diplôme d’ingénieur<br/></li>
</ul>
<h3>Formations et expérience professionnelle souhaitables</h3>
<ul><li>Filière informatique</li></ul>
"""

bio_alt1_text = """
<h2>ALT 1 The RichTextValue<a class="headerlink" href="#the-richtextvalue"
title="Permalink to this headline">¶</a></h2>
<p>The <code class="docutils literal"><span class="pre">RichText</span>
</code> field does not store a string. Instead, it stores a
<code class="docutils literal"><span class="pre">RichTextValue</span>
</code> object. This is an immutable object that has the
following properties:</p>
<dl class="docutils">
<dt><code class="docutils literal"><span class="pre">raw</span></code></dt>
<dd>a unicode string with the original input markup;</dd>
<dt><code class="docutils literal"><span class="pre">mimeType</span></code>
</dt>
<dd>the MIME type of the original markup, e.g.
<code class="docutils literal"><span class="pre">text/html</span></code> or
<code class="docutils literal"><span class="pre">text/structured</span>
</code>;</dd>
<dt><code class="docutils literal"><span class="pre">encoding</span></code>
</dt>
<dd>the default character encoding used when transforming the input markup.
Most likely, this will be UTF-8;</dd>
<dt><code class="docutils literal"><span class="pre">raw_encoded</span>
</code></dt>
<dd>the raw input encoded in the given encoding;</dd>
<dt><code class="docutils literal"><span class="pre">outputMimeType</span>
</code></dt>
<dd>the MIME type of the default output, taken from the field at the time of
instantiation;</dd>
<dt><code class="docutils literal"><span class="pre">output</span></code></dt>
<dd>a unicode object representing the transformed output. If possible, this
is cached persistently until the <code class="docutils literal">
<span class="pre">RichTextValue</span></code> is replaced with a
new one (as happens when an edit form is saved, for example).</dd>
</dl>
"""
bio_alt2_text = """
<h2>ALT 2 The RichTextValue<a class="headerlink" href="#the-richtextvalue"
title="Permalink to this headline">¶</a></h2>
<p>The <code class="docutils literal"><span class="pre">RichText</span>
</code> field does not store a string. Instead, it stores a
<code class="docutils literal"><span class="pre">RichTextValue</span>
</code> object. This is an immutable object that has the
following properties:</p>
<dl class="docutils">
<dt><code class="docutils literal"><span class="pre">raw</span></code></dt>
<dd>a unicode string with the original input markup;</dd>
<dt><code class="docutils literal"><span class="pre">mimeType</span></code>
</dt>
<dd>the MIME type of the original markup, e.g.
<code class="docutils literal"><span class="pre">text/html</span></code> or
<code class="docutils literal"><span class="pre">text/structured</span>
</code>;</dd>
<dt><code class="docutils literal"><span class="pre">encoding</span></code>
</dt>
<dd>the default character encoding used when transforming the input markup.
Most likely, this will be UTF-8;</dd>
<dt><code class="docutils literal"><span class="pre">raw_encoded</span>
</code></dt>
<dd>the raw input encoded in the given encoding;</dd>
<dt><code class="docutils literal"><span class="pre">outputMimeType</span>
</code></dt>
<dd>the MIME type of the default output, taken from the field at the time of
instantiation;</dd>
<dt><code class="docutils literal"><span class="pre">output</span></code></dt>
<dd>a unicode object representing the transformed output. If possible, this
is cached persistently until the <code class="docutils literal">
<span class="pre">RichTextValue</span></code> is replaced with a
new one (as happens when an edit form is saved, for example).</dd>
</dl>
"""

bio_fr = RichTextValue(bio_fr_text, 'text/plain', 'text/html')

bio_alt1 = RichTextValue(bio_alt1_text, 'text/plain', 'text/html')
bio_alt2 = RichTextValue(bio_alt2_text, 'text/plain', 'text/html')


sts = {}
sts['title'] = u'Mon joli site d\'études'
sts['description'] = u'Et là, on a de la chance de revenir entiers !'
sts['presentation'] = bio_fr
sts['image'] = u'1800-IMGA0106.JPG'
sts['img_author'] = u'AuthYYY'
sts['thumbnail'] = u'200-IMGA0106.JPG'
sts['display_one'] = True
sts['presentation_one'] = bio_alt1
sts['display_two'] = True
sts['presentation_two'] = bio_alt1


class createDataSet(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        self.deleteStudySite()
        self.createStudySite()
        url = portal.absolute_url() + '/folder_contents'
        self.request.response.redirect(url)

    def deleteStudySite(self):
        portal = api.portal.get()
        try:
            title = u'mon-joli-site-detudes'
            api.content.delete(obj=portal[title])
        except Exception:
            pass

    def _loadImage(self, objField, image):
        imgPath = image.split('/')
        if len(imgPath) > 1:
            title = imgPath[len(imgPath) - 1]
        else:
            title = image
        path = input_image_path(image)
        fd = open(path, 'r')
        objField.data = fd.read()
        fd.close()
        objField.filename = title

    def createStudySite(self):
        portal = api.portal.get()
        stsite = api.content.create(type='iuem20.studysite',
                                    title=sts['title'],
                                    description=sts['description'],
                                    presentationr=sts['presentation'],
                                    display_one=sts['display_one'],
                                    presentation_one=sts[
                                     'presentation_one'],
                                    display_two=sts['display_two'],
                                    presentation_two=sts[
                                     'presentation_two'],
                                    image=NamedBlobImage(),
                                    img_author=sts['img_author'],
                                    thumbnail=NamedBlobImage(),
                                    container=portal)
        stsite.presentation = sts['presentation']
        self._loadImage(stsite.image, sts['image'])
        allMissions = self.getMissions()
        stsite.missions = set([RelationValue(allMissions[1]),
                               RelationValue(allMissions[2]),
                               RelationValue(allMissions[3]),
                               RelationValue(allMissions[0]),
                               ])
        self.createCarousel(stsite)
        # image
        path_main = input_image_path(sts['image'])
        fd = open(path_main, 'r')
        stsite.image.data = fd.read()
        fd.close()
        stsite.image.filename = sts['image']
        # Thumbnail
        path_main = input_image_path(sts['thumbnail'])
        fd = open(path_main, 'r')
        stsite.thumbnail.data = fd.read()
        fd.close()
        stsite.thumbnail.filename = sts['thumbnail']
        stsite.reindexObject()
        logger.info(stsite.title + ' Created')

    def createCarousel(self, loc):
        carousel = api.content.create(type='Folder',
                                      title=u'carousel',
                                      container=loc)
        api.content.transition(obj=carousel, transition='publish')
        imgs = [u'1800-IMGA0416.JPG', u'1800-IMGA0417.JPG',
                u'1800-IMGA0420.JPG',
                u'1800-IMGA0425.JPG', u'1800-IMGA0465.JPG']
        self._loadImagesInFolder(carousel, imgs)
        logger.info(carousel.title + ' Created')

    def _loadImagesInFolder(self, folderish, images):
        for img in images:
            imgPath = img.split('/')
            if len(imgPath) > 1:
                title = imgPath[len(imgPath) - 1]
            else:
                title = img
            image = api.content.create(type='Image',
                                       title=title,
                                       image=NamedBlobImage(),
                                       description=lorem,
                                       container=folderish)
            self._loadImage(image.image, img)
            image.reindexObject()
            api.content.transition(obj=image, transition='publish')
            image.reindexObject()

    def getMissions(self):
        portal = api.portal.get()
        intids = getUtility(IIntIds)
        founds = api.content.find(context=portal,
                                  portal_type='iuem20.mission',
                                  path='/'.join(portal.getPhysicalPath())
                                  )
        p_ids = []
        for found in founds:
            p_ids.append(intids.getId(found.getObject()))
        return p_ids
