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

        if hasattr(settings, 'ADV_COMMENTS_GRAVATAR_S') or hasattr(settings, 'ADV_COMMENTS_GRAVATAR_D'):
            gravatar_url += '?'
        
        if hasattr(settings, 'ADV_COMMENTS_GRAVATAR_S'):
            gravatar_url += 's='+str(settings.ADV_COMMENTS_GRAVATAR_S)

        if hasattr(settings, 'ADV_COMMENTS_GRAVATAR_D'):
            
            if hasattr(settings, 'ADV_COMMENTS_GRAVATAR_S'):
                gravatar_url += '&'
                
            gravatar_url += 'd='+settings.ADV_COMMENTS_GRAVATAR_D


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
