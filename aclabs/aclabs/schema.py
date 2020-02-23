import graphene
import todo.schema


class Mutation(todo.schema.Mutation, graphene.ObjectType):
    pass

class Query(todo.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
