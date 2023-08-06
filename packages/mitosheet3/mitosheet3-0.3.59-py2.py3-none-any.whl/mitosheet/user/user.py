#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains interfaces and helpers for dealing with the user profile.

Currently, the users profile is stored on disk where Mito is installed, 
but in the future we will support other profile storing locations (e.g.
on a server, so that users can log into a webapp!)
"""
import getpass
import os
import json
from datetime import datetime

from mitosheet.utils import get_random_id
from mitosheet.mito_analytics import log

from mitosheet._version import __version__
from mitosheet.user.user_utils import (
    get_user_field, set_user_field,
    MITO_FOLDER, USER_JSON_PATH
)

# NOTE: this is the default user.json object, and it MUST STAY 
# in sync with the object in mitoinstaller. 

# This is the default user json object
USER_JSON_DEFAULT = {
    'user_json_version': 1,
    'static_user_id': '',
    # A random secret that the user can use as salt when hashing things
    'user_salt': get_random_id(),
    'user_email': '',
    # A list of actions the user intends to do on the tool, which they fill
    # out when they sign up
    'intended_behavior': [],
    'received_tours': [],
    # A list of all the feedback the user has given
    'feedbacks': [],
    # If the user opted out of feedback, we store that they opted out, so
    # that we don't bombard them with feedback
    'closed_feedback': False,
    'mitosheet_current_version': __version__,
    'mitosheet_last_upgraded_date': datetime.today().strftime('%Y-%m-%d'),
    'mitosheet_last_five_usages': [datetime.today().strftime('%Y-%m-%d')]
}

# NOTE: This function must stay in sync with the same file in the
# installer
def try_create_user_json_file():
    # Create the mito folder if it does not exist
    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    # We only create a user.json file if it does not exist
    if not os.path.exists(USER_JSON_PATH):
        # First, we write an empty default object
        with open(USER_JSON_PATH, 'w+') as f:
            f.write(json.dumps(USER_JSON_DEFAULT))

        # Then, we create a new static id and capture the email for the user. 
        # We take special care to put all the CI enviornments 
        # (e.g. Github actions) under one ID and email
        if 'CI' in os.environ and os.environ['CI'] is not None:
            static_user_id = 'github_action'
            user_email = 'github@action.com'
        else:
            # Take the static user id from the installer, if it exists, and otherwise
            # generate a new one
            static_user_id = get_random_id()
            # We used to read the user email if they were signed in on a kubernetes
            # cluster, but instead we ask the user to go through the full signup flow
            # to make sure they accept the privacy policy, and get appropraite tours
            user_email = ''

        set_user_field('static_user_id', static_user_id)
        set_user_field('user_email', user_email)


def is_on_kuberentes_mito():
    """
    Returns True if the user is on Kuberentes Mito
    """
    user = getpass.getuser()
    return user == 'jovyan'


def is_local_deployment():
    """
    Helper function for figuring out if this a local deployment or a
    Mito server deployment
    """
    return not is_on_kuberentes_mito()  


def initialize_user():
    """
    Internal helper function that gets called every time mitosheet 
    is imported.

    It:
    1. Creates a ~/.mito folder, if it does not exist.

    2. Creates new, default user.json file if it does not exist, taking
       special care to do things properly if we're in a CI enviornment.

       Notably, if the user has used the installer, it sets the user
       id to be the same as the installed id, so that we can understand
       how users make it through installation

    3. Updates the user.json file with any new variables, as well as logging
       this usage, and any potential upgrades that may have occured
    """
    # Try to create the user.json file, if it does not already exist
    try_create_user_json_file()

    # Then we just make sure that the user.json has all the fields it needs defined
    # and if they are not defined, it sets them to the default values
    for field, default_value in USER_JSON_DEFAULT.items():
        if get_user_field(field) is None:
            set_user_field(field, default_value)

    # Then, we check if Mito has been upgraded since it was last imported
    # and if it has been upgraded, we upgrade the version and the upgrade date
    mitosheet_current_version = get_user_field('mitosheet_current_version')
    if mitosheet_current_version != __version__:
        set_user_field('mitosheet_current_version', __version__)
        set_user_field('mitosheet_last_upgraded_date', datetime.today().strftime('%Y-%m-%d'))
        # Log the upgrade. Note that this runs when the user _actually_ changes
        # the version of mitosheet that they are using, not just when they 
        # click the upgrade button in the app (although clicking this upgrade
        # button will stop the upgrade popup from showing up)
        log('upgraded_mitosheet', {'old_version': mitosheet_current_version, 'new_version': __version__})

    # We also note this import as a Mito usage, making sure to only 
    # mark this as usage once per day
    last_five_usages = get_user_field('mitosheet_last_five_usages')
    if len(last_five_usages) == 0 or last_five_usages[-1] != datetime.today().strftime('%Y-%m-%d'):
        last_five_usages.append(datetime.today().strftime('%Y-%m-%d'))
    # Then, we take the 5 most recent (or as many as there are), and save them
    if len(last_five_usages) < 5:
        most_recent_five = last_five_usages
    else: 
        most_recent_five = last_five_usages[-5:]
    set_user_field('mitosheet_last_five_usages', most_recent_five)

    # Reidentify the user, just in case things have changed
    from mitosheet.mito_analytics import identify
    identify()


def should_upgrade_mitosheet():
    """
    A helper function that calculates if a user should upgrade,
    which in practice does this with the following heuristic:
    1. If the user has not upgraded in two weeks, then we always reccomend that the user
       upgrades.
    2. If the user has used the tool 4 times since they last upgraded, then we also reccomend
       that they upgrade

    NOTE: this should always return false if it is not a local installation, for obvious
    reasons.

    NOTE: if the user clicks the upgrade button in the app, then we change the upgraded 
    date to this date, so that the user doesn't get a bunch of annoying popups. This just
    pushes back when they are annoyed to upgrade!

    The motivation here is just: we want them to upgrade frequently, but we also don't
    want to just bombard them with upgrade messages. This is a nice middle ground.
    """
    if not is_local_deployment():
        return False

    mitosheet_last_upgraded_date = datetime.strptime(get_user_field('mitosheet_last_upgraded_date'), '%Y-%m-%d')
    mitosheet_last_five_usages = [datetime.strptime(usage, '%Y-%m-%d') for usage in get_user_field('mitosheet_last_five_usages')]

    current_time = datetime.now()
    # Condition (1)
    if (current_time - mitosheet_last_upgraded_date).days > 14:
        return True
    # Condition (2)
    elif len(mitosheet_last_five_usages) >= 4:
        # As this list is chronological, we just need to check 4 back
        if mitosheet_last_five_usages[-4] > mitosheet_last_upgraded_date:
            return True

    return False


def should_display_feedback():
    """
    Returns true if the user has used the tool on 3 seperate
    days and has not yet closed the feedback taskpane.
    """
    num_feedbacks = len(get_user_field('feedbacks'))
    num_days = len(get_user_field('mitosheet_last_five_usages'))
    closed_feedback = get_user_field('closed_feedback')

    return num_feedbacks <= 1 and num_days >= 3 and not closed_feedback

