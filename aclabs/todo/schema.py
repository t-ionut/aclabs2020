import datetime

from django.db.models import Q
import graphene
from graphene_django.types import DjangoObjectType

from todo.models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo

class TodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        text = graphene.String()
        priority = graphene.String()
        dueDate = graphene.String()
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    def mutate(self, info, id, text=None, priority=None, dueDate=None, completed=False):
        todo = Todo.objects.get(pk=id)
        if text is not None:
            todo.text = text
        if priority:
            todo.priority = priority
        if dueDate:
            todo.due_date = datetime.datetime.fromisoformat(dueDate)
        todo.completed = completed
        todo.save()
        return TodoMutation(todo=todo)


class AddTodoInput(graphene.InputObjectType):
    # all fields are optional
    text = graphene.String()
    priority = graphene.String()
    dueDate = graphene.String()
    completed = graphene.Boolean()


class AddTodoMutation(graphene.Mutation):
    class Arguments:
        todo = AddTodoInput(required=True)

    todo = graphene.Field(TodoType)

    def mutate(self, info, todo):
        new_todo = Todo.objects.create(
            text=todo.text,
            priority=todo.priority or "LOW"
        )
        return AddTodoMutation(todo=new_todo)


class Mutation(graphene.ObjectType):
    edit_todo = TodoMutation.Field()
    add_todo = AddTodoMutation.Field()


class Query(object):
    all_todos = graphene.List(TodoType)
    todo = graphene.Field(
        TodoType,
        id=graphene.Int(),
        name=graphene.String()
    )

    def _get_text_filter(self, value):
        return Q(text__istartswith=value) if value else None

    def _get_priority_filter(self, value):
        return Q(priority=value) if value else None

    def _get_completed_filter(self, value):
        return Q(completed=value) if value is not None else value

    def resolve_all_todos(self, info, **kwargs):
        main_filter = None
        for _filter in [self._get_text_filter(kwargs.get("text")),
                        self._get_priority_filter(kwargs.get("priority")),
                        self._get_completed_filter(kwargs.get("completed"))]:
            if _filter:
                main_filter = _filter if main_filter is None else (main_filter & _filter)

        return Todo.objects.all() if main_filter is None else Todo.objects.filter(main_filter)
    
    def resolve_todo(self, info, **kwargs):
        _id = kwargs.get("id")
        _text = kwargs.get("text")

        if _id:
            return Todo.objects.get(id=_id)
        if _text:
            return Todo.objects.get(text=_text)
        return None
