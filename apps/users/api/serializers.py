from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.forms import PasswordResetForm
from apps.users.models import CustomUser, StudentProfile, InstructorProfile, BaseProfile
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken




class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "password_confirm", "is_student", "is_instructor")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_student=validated_data['is_student'],
            is_instructor=validated_data['is_instructor'],
            is_active=False  
        )
        user.set_password(validated_data['password'])
        user.save()


        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"{reverse('activate')}?uid={uid}&token={token}"
        email_subject = 'Activate your account'
        email_body = f"Hi {user.username}, please use this link to activate your account: {activation_link}"
        send_mail(email_subject, email_body, 'no-reply@example.com', [user.email])

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProfile
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'


class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid credentials')

        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('No user is associated with this email address')
        return value

    def save(self, **kwargs):
        request = self.context.get('request')
        user = CustomUser.objects.get(email=self.validated_data['email'])
        form = PasswordResetForm(data={'email': user.email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                token_generator=default_token_generator,
                from_email='no-reply@example.com',  
                email_template_name='registration/password_reset_email.html',
            )


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def save(self, **kwargs):
        uid = force_str(urlsafe_base64_decode(self.validated_data['uidb64']))
        user = CustomUser.objects.get(pk=uid)
        if not default_token_generator.check_token(user, self.validated_data['token']):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

