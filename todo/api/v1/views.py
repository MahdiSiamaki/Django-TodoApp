from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from .serializers import TodoSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPageNumberPagination
from todo.models import Todo

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_fields = ['done']
    search_fields = ['title', 'description']
    ordering_fields= ['due_date', 'done']
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
