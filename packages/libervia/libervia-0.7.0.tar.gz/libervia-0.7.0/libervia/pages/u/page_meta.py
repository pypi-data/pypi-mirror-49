#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from libervia.server.constants import Const as C
from twisted.internet import defer
from twisted.words.protocols.jabber import jid

"""page used to target a user profile, e.g. for public blog"""

name = u"user"
access = C.PAGES_ACCESS_PUBLIC  # can be a callable
template = u"blog/articles.html"
url_cache = True


@defer.inlineCallbacks
def parse_url(self, request):
    try:
        prof_requested = self.nextPath(request)
    except IndexError:
        self.pageError(request)

    data = self.getRData(request)

    target_profile = yield self.host.bridgeCall("profileNameGet", prof_requested)
    request.template_data[u"target_profile"] = target_profile
    target_jid = yield self.host.bridgeCall(
        "asyncGetParamA", "JabberID", "Connection", "value", profile_key=target_profile
    )
    target_jid = jid.JID(target_jid)
    data[u"service"] = target_jid

    # if URL is parsed here, we'll have atom.xml available and we need to
    # add the link to the page
    atom_url = self.getSubPageURL(request, u'user_blog_feed_atom')
    request.template_data[u'atom_url'] = atom_url
    request.template_data.setdefault(u'links', []).append({
        u"href": atom_url,
        u"type": "application/atom+xml",
        u"rel": "alternate",
        u"title": "{target_profile}'s blog".format(target_profile=target_profile)})


@defer.inlineCallbacks
def prepare_render(self, request):
    data = self.getRData(request)
    self.checkCache(
        request, C.CACHE_PUBSUB, service=data[u"service"], node=None, short="microblog"
    )
    self.pageRedirect(u"blog_view", request)

def on_data_post(self, request):
    return self.getPageByName(u"blog_view").on_data_post(self, request)
