# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import DateString, SanitizedUnicode
from marshmallow import fields


class DCObjectSchemaV1Mixin:
    title = SanitizedUnicode(required=True)
    alternative = SanitizedUnicode(required=False)
    abstract = SanitizedUnicode(required=False)
    creator = SanitizedUnicode(required=True)
    contributor = SanitizedUnicode(required=False)
    dateSubmitted = DateString(required=False)
    available = DateString(required=False)
    created = DateString(required=True)
    modified = DateString(required=True)
    description = SanitizedUnicode(required=False)
