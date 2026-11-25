from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status

from accounts.models import User
from advice.models import Advice, AdviceCategory
from api import serializers
from care.models import Procedure, ProcedureLog
from diary.models import DiaryEntry, VetVisit
from pets.models import Pet


class PetViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    serializer_class = serializers.PetSerializer

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DiaryEntryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DiaryEntrySerializer

    def get_queryset(self):
        return DiaryEntry.objects.filter(pet__owner=self.request.user)


class VetVisitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.VetVisitSerializer

    def get_queryset(self):
        return VetVisit.objects.filter(pet__owner=self.request.user)


class ProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProcedureSerializer

    def get_queryset(self):
        return Procedure.objects.filter(pet__owner=self.request.user)


class ProcedureLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProcedureLogSerializer

    def get_queryset(self):
        return ProcedureLog.objects.filter(pet__owner=self.request.user)


class AdviceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.AdviceSerializer

    def get_queryset(self):
        return Advice.objects.filter(is_published=True)


class AdviceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.AdviceCategorySerializer
    queryset = AdviceCategory.objects.all()


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class APIRootView(APIView):
    def get(self, request, format=None):
        return Response({
            'pets': '/api/pets/',
            'diary': '/api/diary/',
            'vet-visits': '/api/vet-visits/',
            'care': '/api/care/',
            'procedure-logs': '/api/procedure-logs/',
            'advice': '/api/advice/',
            'advice-categories': '/api/advice-categories/',
            'users-me': '/api/users/me/',
        })


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]


class PasswordResetRequestAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Если аккаунт с таким email существует, письмо будет отправлено.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Пароль успешно изменён.'}, status=status.HTTP_200_OK)
