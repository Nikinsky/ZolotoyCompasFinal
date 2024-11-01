from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from yaml import serialize_all
from .serializers import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.conf import settings
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({
            'user': {
                'email': user.email,
                'username': user.username,
                'token': str(token.access_token),
            }
        }, status=status.HTTP_201_CREATED)




class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Получаем токен из заголовков
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]

            # Здесь можно добавить логику для черного списка токенов
            # Например, если вы используете простую JWT, вы можете использовать:
            RefreshToken.for_user(request.user).blacklist()

            return Response({"message": "Успешный выход."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Ошибка выхода: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)





class ResetPasswordRequestView(generics.CreateAPIView):
    serializer_class = ResetPasswordEmailSerializer
    def post(self, request):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = UserProfile.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            reset_url = request.build_absolute_uri(f'/reset-password-confirm/{token}/')

            # Отправляем email
            send_mail(
                subject="Сброс пароля",
                message=f"Перейдите по следующей ссылке для сброса пароля: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({"message": "Письмо для сброса пароля отправлено."}, status=200)
        return Response(serializer.errors, status=400)



class ResetPasswordConfirmView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = UserProfile.objects.get(id=user_id)
        except Exception:
            return Response({"error": "Недействительный или истекший токен"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({"message": "Пароль успешно обновлен"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializers
    queryset1 = Address.objects.all()

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# class UserProfileView(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializers


class AddressView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = AddressSerializer












class RegionView(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializers


class RegionPhotosView(viewsets.ModelViewSet):
    queryset = RegionPhotos.objects.all()
    serializer_class = RegionPhotosSerializers


class RegionFoodView(viewsets.ModelViewSet):
    queryset = RegionFood.objects.all()
    serializer_class = RegionFoodSerializers







class PlacesViewSet(viewsets.ModelViewSet):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializers
    filterset_class = PlacesFilter


class PlacesPhotosView(viewsets.ModelViewSet):
    queryset = PlacesPhotos.objects.all()
    serializer_class = PlacesPhotosSerializers

class PlacesListView(viewsets.ModelViewSet):
    queryset = Places.objects.all()
    serializer_class = PlacesListSerializers
    filterset_class = PlacesFilter

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_class = ReviewPlacesFilter









class AttractionsView(viewsets.ModelViewSet):
    queryset = Attractions.objects.all()
    serializer_class = AttractionSerializers
    filterset_class = AttractionFilter

class AttractionListView(viewsets.ModelViewSet):
    queryset = Attractions.objects.all()
    serializer_class = AttractionListSerializers
    filterset_class = AttractionFilter


class AttractionSimpleListView(viewsets.ModelViewSet):
    queryset = Attractions.objects.all()
    serializer_class = AttractionSimpleListSerializers
    filterset_class = AttractionFilter









class HotelView(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializers

class HotelListView(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializers
    filterset_class = HotelFilter




class KitchenView(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializers
    filterset_class = KitchenFilter


class KitchenListView(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenListSerializers
    filterset_class = KitchenFilter




class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter











class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers

class CartItemsView(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers












class CultureView(viewsets.ModelViewSet):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializers


class GamesView(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializers


class NationalClothesView(viewsets.ModelViewSet):
    queryset = NationalClothes.objects.all()
    serializer_class = NationalClothesSerializers
    

class HandCraftSerializers(viewsets.ModelViewSet):
    queryset = HandCrafts.objects.all()
    serializer_class = HandCraftsSerializers


class CurrencyView(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializers


class NationalInstrumentsView(viewsets.ModelViewSet):
    queryset = NationalInstruments.objects.all()
    serializer_class = NationalInstrumentsSerializers

class NationalFoodView(viewsets.ModelViewSet):
    queryset = NationalFood.objects.all()
    serializer_class = NationalFoodSerializers