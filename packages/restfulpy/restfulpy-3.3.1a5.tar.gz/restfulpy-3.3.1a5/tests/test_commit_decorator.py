from bddrest import response, when
from nanohttp import json, RestController, context, HTTPStatus
from sqlalchemy import Unicode, Integer

from restfulpy.controllers import JsonPatchControllerMixin
from restfulpy.orm import commit, DeclarativeBase, Field, DBSession
from restfulpy.testing import ApplicableTestCase


class CommitCheckingModel(DeclarativeBase):
    __tablename__ = 'commit_checking_model'
    id = Field(Integer, primary_key=True)
    title = Field(Unicode(50), unique=True)


class Root(JsonPatchControllerMixin, RestController):

    @json
    @commit
    def post(self):
        m = CommitCheckingModel()
        m.title = context.form['title']
        DBSession.add(m)
        return m

    @json
    @commit
    def success(self):
        m = CommitCheckingModel()
        m.title = context.form['title']
        DBSession.add(m)
        raise HTTPStatus('200 OK')

    @json
    @commit
    def redirect(self):
        m = CommitCheckingModel()
        m.title = context.form['title']
        DBSession.add(m)
        raise HTTPStatus('300 Redirect')

    @json
    def get(self, title: str=None):
        m = DBSession.query(CommitCheckingModel).\
            filter(CommitCheckingModel.title == title).one()
        return m

    @json
    @commit
    def error(self):
        m = CommitCheckingModel()
        m.title = 'Error'
        DBSession.add(m)
        raise Exception()


class TestCommitDecorator(ApplicableTestCase):
    __controller_factory__ = Root

    def test_commit_decorator(self):
        with self.given(
            'Testing the operation of commit decorator',
            verb='POST',
            url='/',
            form=dict(title='first')
        ):
            when('Geting the result of appling commit decorator',
                 verb='GET',
                 url='/first'
                 )
            assert response.json['title'] == 'first'
            assert response.json['id'] == 1

    def test_commit_decorator_and_json_patch(self):
        with self.given(
            'The commit decorator should not to do anything if the request\
            is a jsonpatch.',
            verb='PATCH',
            url='/',
            json=[
                dict(op='post', path='', value=dict(title='second')),
                dict(op='post', path='', value=dict(title='third'))
            ]):
            when('Inset form parameter to body', verb='GET', url='/third')
            assert response.json['title'] == 'third'

    def test_rollback(self):
        with self.given('Raise exception', verb='ERROR', url='/'):
            assert response.status == 500

    def test_commit_on_raise_http_success(self):
        with self.given(
            'Testing the operation of commit decorator on raise 2xx',
            verb='SUCCESS',
            url='/',
            form=dict(title='HTTPSuccess')
        ):
            when(
                'Geting the result of appling commit decorator',
                 verb='GET',
                 url='/HTTPSuccess'
            )
            assert response.json['title'] == 'HTTPSuccess'

    def test_commit_on_raise_http_redirect(self):
        with self.given(
            'Testing the operation of commit decorator on raise 3xx',
            verb='REDIRECT',
            url='/',
            form=dict(title='HTTPRedirect')
        ):
            when(
                'Geting the result of appling commit decorator',
                 verb='GET',
                 url='/HTTPRedirect'
            )
            assert response.json['title'] == 'HTTPRedirect'

