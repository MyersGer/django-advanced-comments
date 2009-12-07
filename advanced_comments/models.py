#    This file is part of django-advanced-comments.

#    django-advanced-comments is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    django-advanced-comments is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.

#    You should have received a copy of the GNU Lesser General Public License
#    along with django-advanced-comments.  If not, see <http://www.gnu.org/licenses/>.

import hashlib
from django.contrib.comments.signals import comment_will_be_posted
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.conf import settings
from django.db import models

class AdvancedComment(Comment):

    #GravatarSupport
    def gravatar(self):

        # construct the url
        gravatar_url = "http://www.gravatar.com/avatar/"
        gravatar_url += hashlib.md5(self.user_email.lower()).hexdigest()

        if hasattr(settings, 'ADV_COMMENT_GRAVATAR_S') or hasattr(settings, 'ADV_COMMENTS_GRAVATAR_D'):
            gravatar_url += '?'
        
        if hasattr(settings, 'ADV_COMMENTS_GRAVATAR_S'):
            gravatar_url += 's='+str(settings.ADV_COMMENT_GRAVATAR_S)

        if hasattr(settings, 'ADV_COMMENTS_GRAVATAR_D'):
            gravatar_url += '?d='+settings.ADV_COMMENT_GRAVATAR_D


        return gravatar_url



#AkismetSupport
'''
    we're using the comment_was_posted signal to hook into the comment process
'''
def on_comment_will_be_posted(sender, comment, request, *args, **kwargs):
    if hasattr(settings, 'ADV_COMMENTS_SPAMPROTECTION'):
        if not settings.ADV_COMMENTS_SPAMPROTECTION:
            return

    #if spamprotection is the choice, go on
    try:
        from akismet import Akismet
    except:
        return

    ak = Akismet(
         key=settings.ADV_COMMENTS_AKISMET_API_KEY,
         blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
    )

    if ak.verify_key():
        data = {
            'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'comment_type': 'comment',
            'comment_author': comment.user_name.encode('utf-8'),
        }

        if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
            return False


comment_will_be_posted.connect(on_comment_will_be_posted)
