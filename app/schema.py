import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from django.contrib.auth.models import Group
from django.db.models import F
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from graphene_django.filter import DjangoFilterConnectionField
from datetime import date
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

class LoanModel(DjangoObjectType):
    class Meta:
        model = Loan

class LoanBook(graphene.Mutation):
    loan = graphene.Field(LoanModel)
    
    class Arguments:
        book = graphene.String(required=True)
        finishdate = graphene.String(required=True)
        userclient = graphene.String(required=True)
        quantity = graphene.String(required=True)
    
    def mutate(self, info, book, finishdate, userclient, quantity):
        book = Book.objects.get(title=book)
        book.existence = F('existence') - quantity
        userclient = get_user_model().objects.get(username=userclient)
        loan = Loan(book=book, finish_date=finishdate, user_client=userclient, quantity=int(quantity))
        book.save()
        loan.save()
        
        return LoanBook(loan=loan)

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

class GroupNode(DjangoObjectType):
    class Meta:
        model = Group

class UserNode(DjangoObjectType):
    group = graphene.List(GroupNode)
    
    @graphene.resolve_only_args
    def resolve_group(self):
        return self.group.all()

    class Meta:
        model = get_user_model()
        filter_fields = ['groups', 'username' ]
        interfaces = (relay.Node, )

class LoanNode(DjangoObjectType):    
    class Meta:
        model = Loan
        filter_fields = ['id', 'book', 'active',]
        interfaces = (relay.Node, )

class DoneLoan(graphene.Mutation):
    loan = graphene.Field(LoanModel)
    
    class Arguments:
        id = graphene.String(required=True)
        book = graphene.String(required=True)
        quantity = graphene.String(required=True)
    
    def mutate(self, info, id, book, quantity):
        book = Book.objects.get(id=book)
        book.existence = F('existence') + quantity
        loan = Loan.objects.get(id=id)
        loan.active = False
        loan.done_date = date.today()
        loan.save()
        book.save()
        
        return LoanBook(loan=loan)

class Query(graphene.ObjectType):
    country = relay.Node.Field(CountryNode)
    all_countries = DjangoFilterConnectionField(CountryNode)
    
    book = relay.Node.Field(BookNode)
    all_books = DjangoFilterConnectionField(BookNode)
    
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
    
    loan = relay.Node.Field(LoanNode)
    all_loans = DjangoFilterConnectionField(LoanNode)

class Mutation(graphene.ObjectType):
    create_user_client = CreateUserClient.Field()
    
    create_loan = LoanBook.Field()
    
    done_loan = DoneLoan.Field()