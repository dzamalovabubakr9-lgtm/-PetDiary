from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from accounts.models import User
from advice.models import Advice, AdviceCategory
from care.models import Procedure, ProcedureLog
from diary.models import DiaryEntry, VetVisit
from pets.models import Pet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_staff']
        read_only_fields = fields


class PetSerializer(serializers.ModelSerializer):
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    sex_display = serializers.CharField(source='get_sex_display', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'species', 'species_display', 'breed', 'sex', 'sex_display',
            'birth_date', 'weight', 'photo', 'description', 'owner_username', 'created',
        ]
        read_only_fields = ['owner_username', 'created']


class DiaryEntrySerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.none())
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['pet'].queryset = Pet.objects.filter(owner=request.user)

    class Meta:
        model = DiaryEntry
        fields = ['id', 'pet', 'pet_name', 'date', 'title', 'description', 'category', 'category_display', 'created']
        read_only_fields = ['pet_name', 'created']


class VetVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VetVisit
        fields = ['id', 'pet', 'date', 'description', 'recommendations']


class ProcedureSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.none())
    name_display = serializers.CharField(source='get_name_display', read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['pet'].queryset = Pet.objects.filter(owner=request.user)

    class Meta:
        model = Procedure
        fields = ['id', 'pet', 'name', 'name_display', 'description', 'scheduled_date', 'done', 'done_at', 'created']
        read_only_fields = ['done_at', 'created']


class ProcedureLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureLog
        fields = ['id', 'pet', 'procedure', 'name', 'done_date', 'comment']


class AdviceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceCategory
        fields = ['id', 'name', 'description']


class AdviceSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(source='category', read_only=True)

    class Meta:
        model = Advice
        fields = ['id', 'category', 'category_id', 'title', 'content', 'is_published', 'created']
        read_only_fields = ['category_id', 'is_published', 'created']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def save(self):
        form = PasswordResetForm({'email': self.validated_data['email']})
        if form.is_valid():
            form.save(
                request=self.context.get('request'),
                use_https=self.context.get('request').is_secure(),
                email_template_name='accounts/password_reset_email.html',
                subject_template_name='accounts/password_reset_subject.txt',
            )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    def validate(self, attrs):
        try:
            user_id = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(pk=user_id)
        except (ValueError, TypeError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Ссылка восстановления недействительна.')
        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('Ссылка восстановления недействительна или устарела.')
        attrs['user'] = user
        return attrs
    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user
