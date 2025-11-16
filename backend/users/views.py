from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet

from .models import Subscribe
from .serializers import SubscribeSerializer


class UserViewSet(DjoserUserViewSet):
    lookup_field = 'username'

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, username=None):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            author = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'errors': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'POST':
            if author == request.user:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            subscribe, created = Subscribe.objects.get_or_create(
                user=request.user,
                author=author
            )
            if created:
                serializer = SubscribeSerializer(
                    subscribe,
                    context={'request': request}
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Вы уже подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST
            )

        elif request.method == 'DELETE':
            subscribe = get_object_or_404(
                Subscribe,
                user=request.user,
                author=author
            )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        subscribes = Subscribe.objects.filter(user=request.user)
        page = self.paginate_queryset(subscribes)
        if page is not None:
            serializer = SubscribeSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscribeSerializer(
            subscribes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
