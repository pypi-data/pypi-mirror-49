from datetime import datetime, time

import pytest
from bddrest import response, when, status
from dateutil.tz import tzoffset
from nanohttp import json
from sqlalchemy import Integer, Time

from restfulpy.configuration import settings
from restfulpy.controllers import JSONPatchControllerMixin, ModelRestController
from restfulpy.datetimehelpers import parse_datetime, format_datetime, \
    format_time
from restfulpy.mockup import mockup_localtimezone
from restfulpy.orm import commit, DeclarativeBase, Field, DBSession
from restfulpy.testing import ApplicableTestCase


class Azan(DeclarativeBase):
    __tablename__ = 'azan'
    id = Field(Integer, primary_key=True)
    when = Field(Time)


class Root(JSONPatchControllerMixin, ModelRestController):
    __model__ = 'azan'

    @json
    @commit
    def post(self):
        m = Azan()
        m.update_from_request()
        DBSession.add(m)
        return m.when.isoformat()


class TestTime(ApplicableTestCase):
    __controller_factory__ = Root

    def test_update_from_request(self):
        with self.given(
            'Posting a time in form',
            verb='POST',
            form=dict(
                when='00:01',
            )
        ):
            assert status == 200
            assert response.json == '00:01:00'

            when(
                'Posting a date instead of time',
                form=dict(
                    when='2001-01-01'
                )
            )
            assert status == 200
            assert response.json == '00:00:00'

            when(
                'Posting a datetime instead of time',
                form=dict(
                    when='2001-01-01T00:01:00.123456'
                )
            )
            assert status == 200
            assert response.json == '00:01:00.123456'

            when(
                'Posting an invalid time',
                form=dict(
                    when=''
                )
            )
            assert status == '400 Invalid date or time: '

            when(
                'Posting another invalid time',
                form=dict(
                    when='invalid'
                )
            )
            assert status == '400 Invalid date or time: invalid'

    def test_format_time(self):
        assert '01:02:03' == format_time(time(1, 2, 3))
        assert '01:02:03' == format_time(datetime(1970, 1, 1, 1, 2, 3))

