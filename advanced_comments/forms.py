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

from django import forms
from django.contrib.comments.forms import CommentForm
from advanced_comments.models import AdvancedComment

class AdvancedCommentForm(CommentForm):

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return AdvancedComment
