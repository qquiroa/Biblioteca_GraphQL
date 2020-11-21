import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from graphene_django.filter import DjangoFilterConnectionField
from app.models import *

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class CreateUserClient(graphene.Mutation):
    user = graphene.Field(UserType)
    
    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, name, username, password):
        user = get_user_model()(
            username=username,
            first_name=name,
        )
        user.set_password(password)
        user.save()
        group = Group.objects.get(name='client')
        user.groups.add(group)
        return CreateUserClient(user=user)

class CountryNode(DjangoObjectType):
    class Meta:
        model = Country
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author

class BookNode(DjangoObjectType):
    author = graphene.List(AuthorNode)

    
    @graphene.resolve_only_args
    def resolve_author(self):
        return self.author.all()
    
    class Meta:
        model = Book
        filter_fields = ['title', 'description']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    country = relay.Node.Field(CountryNode)
    all_countries = DjangoFilterConnectionField(CountryNode)
    
    book = relay.Node.Field(BookNode)
    all_books = DjangoFilterConnectionField(BookNode)

class Mutation(graphene.ObjectType):
    create_user_client = CreateUserClient.Field()