import graphene
from graphene_django import DjangoObjectType

from core.models import Question


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "description")


class Query(graphene.ObjectType):
    questions = graphene.List(QuestionType)
    question_by_id = graphene.Field(QuestionType, id=graphene.String())

    def resolve_questions(root, info, **kwargs):
        # Querying a list
        return Question.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return Question.objects.get(pk=id)


class QuestionMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        description = graphene.String(required=True)
        # id = graphene.ID()

    # The class attributes define the response of the mutation
    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, description):
        question = Question.objects.create(description=description)
        # Notice we return an instance of this mutation
        return QuestionMutation(question=question)


class Mutation(graphene.ObjectType):
    create_question = QuestionMutation.Field()
    update_question = QuestionMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
