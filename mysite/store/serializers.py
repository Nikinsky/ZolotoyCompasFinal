from django.contrib.admin.utils import model_ngettext
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.fields import SerializerMethodField
from rest_framework.permissions import AllowAny
from rest_framework.utils.representation import manager_repr
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django_countries.serializers import CountryFieldMixin





class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'password', 'password_confirm', 'birth_date', 'phone_number', 'image', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Убираем поле 'password_confirm' перед сохранением
        validated_data.pop('password_confirm')

        # Создаем пользователя
        user = UserProfile.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Проверяем, что введенный пароль совпадает с подтверждением пароля
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"detail": "Passwords do not match."})

        # Удаляем confirm_password, так как он не нужен для дальнейшей обработки
        attrs.pop('confirm_password')

        return super().validate(attrs)







class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)


class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(write_only=True)
    class Meta:
        model = UserProfile
        fields = ['email']
    def validate_email(self, value):
        """
        Проверка, существует ли пользователь с таким email.
        """
        if not UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, max_length=16, min_length=8)

    def validate_password(self, value):
        # Дополнительные проверки на сложность пароля (опционально)
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать не менее 8 символов.")
        return value





class AddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'country']

class UserProfileSerializers(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password', 'last_name', 'birth_date', 'phone_number', 'image', 'addresses']


class UserProfileSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'last_name', 'image']



class UserProfileGalerySerializers(serializers.ModelSerializer):
    addresses = AddressSerializer()
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'last_name', 'image', 'addresses']














class RegionPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegionPhotos
        fields = ['region_photos', 'image']

class RegionSerializers(serializers.ModelSerializer):
    reg_photos = RegionPhotosSerializers(many=True)
    class Meta:
        model = Region
        fields = ['id', 'region_name', 'description', 'reg_photos']


class RegionFoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegionFood
        fields = ['id', 'region_food', 'food_name', 'include_food', 'description_name', 'image']












class PlacesPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlacesPhotos
        fields = ['image']



class PlacesSerializers(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    places_photos = PlacesPhotosSerializers(many=True)
    class Meta:
        model = Places
        fields = ['id', 'places_name', 'description', 'average_rating', 'places_photos']

    def average_rating(self, obj):
        return obj.average_rating()


class PlacesListSerializers(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    places_photos = PlacesPhotosSerializers(many=True)
    class Meta:
        model = Places
        fields = ['id', 'places_name', 'average_rating', 'places_photos']

    def average_rating(self, obj):
        return obj.average_rating()






# class PlacesSimpleSerializer(serializers.ModelSerializer):
#     reviews = ReviewSerializer(many=True, read_only=True)
#     average_rating = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Places
#         fields = ['places_name', 'description', 'average_rating', 'reviews']
#
#
#     def get_average_rating(self, obj):
#         return obj.average_rating()






class ConditionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Conditions
        fields = ['id', 'name_conditions', 'icon']


class OfferedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Offered_amenities
        fields = ['id', 'name_offered', 'icon']


class SafetySerializers(serializers.ModelSerializer):
    class Meta:
        model = Safety_and_hydigene
        fields = ['id', 'name_safety', 'icon']



class HotelPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelPhotos
        fields = ['id', 'image']


class HotelSerializers(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    photos_hotel = HotelPhotosSerializers(many=True)
    conditions = ConditionsSerializers(many=True)
    offereds = OfferedSerializers(many=True)
    safetys = SafetySerializers(many=True)


    class Meta:
        model = Hotel
        fields = ['id', 'places', 'hotel_name', 'average_rating', 'description', 'photos_hotel',
                'short_period', 'medium_period', 'long_period', 'phone_number', 'conditions', 'offereds', 'safetys' ]


    def get_average_rating(self, obj):
        return obj.get_average_rating()



class HotelListSerializers(serializers.ModelSerializer):
    average_rating= serializers.SerializerMethodField()
    photos_hotel = HotelPhotosSerializers(many=True)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'photos_hotel', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()











class AttractionsPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = AttractionsPhotos
        fields = ['image']


class AttractionSerializers(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    attraction_photos = AttractionsPhotosSerializers(many=True)
    class Meta:
        model = Attractions
        fields = ['id', 'at_name', 'description', 'attraction_photos', 'average_rating', 'phone_number']


    def get_average_rating(self, obj):
        return obj.get_average_rating()




class AttractionListSerializers(serializers.ModelSerializer):
    average_rating= serializers.SerializerMethodField()
    attraction_photos = AttractionsPhotosSerializers(many=True)

    class Meta:
        model = Attractions
        fields = ['id', 'at_name', 'attraction_photos', 'average_rating', 'description']

    def get_average_rating(self, obj):
        return obj.get_average_rating()



class AttractionSimpleListSerializers(serializers.ModelSerializer):
    average_rating= serializers.SerializerMethodField()
    attraction_photos = AttractionsPhotosSerializers(many=True)

    class Meta:
        model = Attractions
        fields = ['id', 'at_name', 'attraction_photos', 'average_rating',]

    def get_average_rating(self, obj):
        return obj.get_average_rating()









class KitchenPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = KitchenPhotos
        fields = ['image']


class KitchenSerializers(serializers.ModelSerializer):
    kit_photos = KitchenPhotosSerializers(many=True)
    average_rating = SerializerMethodField()

    class Meta:
        model = Kitchen
        fields = ['id', 'name_kitchen', 'category', 'price_range', 'specialized_menu', 'meal_time', 'address', 'email', 'phone_number', 'average_rating',
                  'kit_photos']

    def get_average_rating(self, obj):
        return obj.get_average_rating()




class KitchenListSerializers(serializers.ModelSerializer):
    average_rating= serializers.SerializerMethodField()
    kit_photos = AttractionsPhotosSerializers(many=True)

    class Meta:
        model = Kitchen
        fields = ['id', 'name_kitchen', 'kit_photos', 'average_rating', 'category' ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()










class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'ticket_price', 'image']




class PhotosReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = PhotosReview
        fields = ['image']



class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializers()
    reviews_photos = PhotosReviewSerializers(many=True)
    class Meta:
        model = Review
        fields = ['id', 'author', 'rating', 'comment', 'created_at', 'reviews_photos', 'likes']











class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'places', 'hotel']


class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(many=True)
    user = UserProfile()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']












class CultureSerializers(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'culture_name', 'description', 'image']

class GamesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'game_name', 'description', 'image']

class NationalClothesSerializers(serializers.ModelSerializer):
    class Meta:
        model = NationalClothes
        fields = ['id', 'clothes_name', 'description', 'image']

class HandCraftsSerializers(serializers.ModelSerializer):
    class Meta:
        model = HandCrafts
        fields = ['id', 'handcraft_name', 'description', 'image']

class CurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'currency_name', 'description', 'image']

class NationalInstrumentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = NationalInstruments
        fields = ['id', 'instrument', 'description', 'image']

class NationalFoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = NationalFood
        fields = ['id', 'nationalfood_name', 'description', 'image']
