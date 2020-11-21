import graphene
import app.schema


class Query(app.schema.Query, graphene.ObjectType):
    # Esta clase heredara de multiples consultas
    # segun vayamos agregando aplicaciones a nuestro proyecto
    pass

class Mutation(app.schema.Mutation, graphene.ObjectType,):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)