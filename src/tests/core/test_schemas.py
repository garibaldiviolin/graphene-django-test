import pytest
from graphene_django.utils.testing import graphql_query

from core.models import Question

pytestmark = pytest.mark.django_db


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


def test_query(client_query):
    Question.objects.create(description="OK")

    response = client_query(
        '''
        query {
            questions {
                id
                description
            }
        }
        ''',
        graphql_url="/graphql"
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'questions': [{
                'id': '1',
                'description': 'OK'
            }]
        }
    }


def test_query_by_id(client_query):
    Question.objects.create(description="OK")

    response = client_query(
        '''
        query {
            questionById(id: "1") {
                id
                description
            }
        }
        ''',
        graphql_url="/graphql"
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'questionById': {
                'id': '1',
                'description': 'OK'
            }
        }
    }


def test_mutation(client_query):
    response = client_query(
        '''
            mutation {
                createQuestion(description: "What?") {
                    question {
                        id
                        description
                    }
                }
            }
        ''',
        graphql_url="/graphql"
    )

    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'createQuestion': {
                'question': {
                    'description': 'What?', 'id': '1'
                }
            }
        }
    }

    question = Question.objects.get(id=1)
    question.description == "What?"
