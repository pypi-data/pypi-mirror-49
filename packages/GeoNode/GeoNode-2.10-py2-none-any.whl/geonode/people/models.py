# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from uuid import uuid1, uuid4
import logging
import traceback

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sites.models import Site
from django.db.models import signals
from django.conf import settings

from taggit.managers import TaggableManager

from geonode.decorators import on_ogc_backend
from geonode.base.enumerations import COUNTRIES
from geonode.base.auth import (get_or_create_token,
                               delete_old_tokens,
                               set_session_token,
                               remove_session_token)
from geonode.groups.models import GroupProfile
# from geonode.notifications_helper import send_notification

from geonode import geoserver

from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
# from account.models import EmailAddress

from .utils import format_address
from .signals import (update_user_email_addresses,
                      notify_admins_new_signup)
from .languages import LANGUAGES
from .timezones import TIMEZONES

logger = logging.getLogger(__name__)


class ProfileUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class Profile(AbstractUser):

    """Fully featured Geonode user"""

    organization = models.CharField(
        _('Organization Name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('name of the responsible organization'))
    profile = models.TextField(
        _('Profile'),
        null=True,
        blank=True,
        help_text=_('introduce yourself'))
    position = models.CharField(
        _('Position Name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('role or position of the responsible person'))
    voice = models.CharField(_('Voice'), max_length=255, blank=True, null=True, help_text=_(
        'telephone number by which individuals can speak to the responsible organization or individual'))
    fax = models.CharField(_('Facsimile'), max_length=255, blank=True, null=True, help_text=_(
        'telephone number of a facsimile machine for the responsible organization or individual'))
    delivery = models.CharField(
        _('Delivery Point'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('physical and email address at which the organization or individual may be contacted'))
    city = models.CharField(
        _('City'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('city of the location'))
    area = models.CharField(
        _('Administrative Area'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('state, province of the location'))
    zipcode = models.CharField(
        _('Postal Code'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('ZIP or other postal code'))
    country = models.CharField(
        _('Country'),
        choices=COUNTRIES,
        max_length=3,
        blank=True,
        null=True,
        help_text=_('country of the physical address'))
    keywords = TaggableManager(_('keywords'), blank=True, help_text=_(
        'commonly used word(s) or formalised word(s) or phrase(s) used to describe the subject \
            (space or comma-separated'))
    language = models.CharField(
        _("language"),
        max_length=10,
        choices=LANGUAGES,
        default=settings.LANGUAGE_CODE
    )
    timezone = models.CharField(
        _('Timezone'),
        max_length=100,
        default="",
        choices=TIMEZONES,
        blank=True,
    )

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self._previous_active_state = self.is_active

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.username, ])

    def __unicode__(self):
        return u"%s" % (self.username)

    def class_name(value):
        return value.__class__.__name__

    objects = ProfileUserManager()
    USERNAME_FIELD = 'username'

    def group_list_public(self):
        return GroupProfile.objects.exclude(
            access="private").filter(groupmember__user=self)

    def group_list_all(self):
        return GroupProfile.objects.filter(groupmember__user=self).distinct()

    def is_member_of_group(self, group_slug):
        """
        Returns if the Profile belongs to a group of a given slug.
        """
        return self.groups.filter(name=group_slug).exists()

    def keyword_list(self):
        """
        Returns a list of the Profile's keywords.
        """
        return [kw.name for kw in self.keywords.all()]

    @property
    def name_long(self):
        if self.first_name and self.last_name:
            return '%s %s (%s)' % (self.first_name,
                                   self.last_name, self.username)
        elif (not self.first_name) and self.last_name:
            return '%s (%s)' % (self.last_name, self.username)
        elif self.first_name and (not self.last_name):
            return '%s (%s)' % (self.first_name, self.username)
        else:
            return self.username

    @property
    def location(self):
        return format_address(self.delivery, self.zipcode,
                              self.city, self.area, self.country)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        self._notify_account_activated()
        self._previous_active_state = self.is_active

    def _notify_account_activated(self):
        """Notify user that its account has been activated by a staff member"""
        became_active = self.is_active and not self._previous_active_state
        if became_active and self.last_login is None:
            try:
                # send_notification(users=(self,), label="account_active")

                from invitations.adapters import get_invitations_adapter
                current_site = Site.objects.get_current()
                ctx = {
                    'username': self.username,
                    'current_site': current_site,
                    'site_name': current_site.name,
                    'email': self.email,
                    'inviter': self,
                }

                email_template = 'pinax/notifications/account_active/account_active'

                get_invitations_adapter().send_mail(
                    email_template,
                    self.email,
                    ctx)
            except BaseException:
                import traceback
                traceback.print_exc()


def get_anonymous_user_instance(Profile):
    return Profile(pk=-1, username='AnonymousUser')


def profile_post_save(instance, sender, **kwargs):
    """
    Make sure the user belongs by default to the anonymous group.
    This will make sure that anonymous permissions will be granted to the new users.
    """
    from django.contrib.auth.models import Group
    anon_group, created = Group.objects.get_or_create(name='anonymous')
    instance.groups.add(anon_group)
    # do not create email, when user-account signup code is in use
    if getattr(instance, '_disable_account_creation', False):
        return


""" Connect relevant signals to their corresponding handlers. """
social_account_added.connect(
    update_user_email_addresses,
    dispatch_uid=str(uuid4()),
    weak=False
)
user_signed_up.connect(
    notify_admins_new_signup,
    dispatch_uid=str(uuid4()),
    weak=False
)
signals.post_save.connect(profile_post_save, sender=Profile)


@on_ogc_backend(geoserver.BACKEND_PACKAGE)
def do_login(sender, user, request, **kwargs):
    """
    Take action on user login. Generate a new user access_token to be shared
    with GeoServer, and store it into the request.session
    """
    if user and user.is_authenticated():
        token = None
        try:
            token = get_or_create_token(user)
        except BaseException:
            u = uuid1()
            token = u.hex
            tb = traceback.format_exc()
            logger.debug(tb)

        set_session_token(request.session, token)


@on_ogc_backend(geoserver.BACKEND_PACKAGE)
def do_logout(sender, user, request, **kwargs):
    if 'access_token' in request.session:
        try:
            delete_old_tokens(user)
        except BaseException:
            tb = traceback.format_exc()
            logger.debug(tb)
        remove_session_token(request.session)
        request.session.modified = True


user_logged_in.connect(do_login)
user_logged_out.connect(do_logout)
