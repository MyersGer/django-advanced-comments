from django import forms
from django.contrib.comments.forms import CommentForm
from advanced_comments.models import AdvancedComment

class AdvancedCommentForm(CommentForm):

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return AdvancedComment
