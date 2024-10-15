from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField



class UserProfile(AbstractUser):

    birth_date = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True,blank=True, region="KG")
    image = models.ImageField(null=True, blank=True)
    address = models.CharField(max_length=32, null=True, blank=True)


    def __str__(self):
        return f'{self.username} - {self.last_name}'



class Address(models.Model):
    user = models.ForeignKey(UserProfile, related_name='addresses', on_delete=models.CASCADE)
    street = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    country = CountryField()

    def __str__(self):
        return f'{self.user} - {self.city} - {self.country}'







class Region(models.Model):
    region_name = models.CharField(max_length=32, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.region_name}'


class RegionPhotos(models.Model):
    region_photos = models.ForeignKey(Region, related_name='reg_photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img_region/')


class RegionFood(models.Model):
    region_food = models.ForeignKey(Region, related_name='reg_food', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=32)
    include_food = models.TextField()
    description_name = models.TextField()
    image = models.ImageField(upload_to='img_region_food/')

    def __str__(self):
        return f'{self.region_food} - {self.food_name}'









class Places(models.Model):
    region_places = models.ForeignKey(Region, on_delete=models.CASCADE)
    places_name = models.CharField(max_length=32,)
    description = models.TextField()

    def __str__(self):
        return f'{self.region_places} - {self.places_name}'


    def average_rating(self):
        """Вычисление среднего рейтинга для продукта"""
        return self.reviews_places.aggregate(models.Avg('rating'))['rating__avg'] or 0


class PlacesPhotos(models.Model):
    places = models.ForeignKey(Places, related_name='places_photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img_places/')














class Hotel(models.Model):
    places = models.ForeignKey(Places, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=32)
    description = models.TextField()
    short_period = models.IntegerField(default=1000)
    medium_period = models.IntegerField(default=1500)
    long_period = models.IntegerField(default=2000)
    phone_number = PhoneNumberField(null=True,blank=True, region="KG")


    def get_average_rating(self):
        """Вычисление среднего рейтинга для продукта"""
        return self.hotels.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return f'{self.places}- {self.hotel_name}'



class HotelPhotos(models.Model):
    hotel = models.ForeignKey(Hotel,related_name='photos_hotel', on_delete=models.CASCADE)
    image = models.ImageField()


class Conditions(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='conditions', on_delete=models.CASCADE)
    name_conditions = models.CharField(max_length=32)
    icon = models.ImageField(upload_to='icon_conditions/')


class Offered_amenities(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='offereds', on_delete=models.CASCADE)
    name_offered = models.CharField(max_length=32)
    icon = models.ImageField(upload_to='icons_offered/')


class Safety_and_hydigene(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='safetys', on_delete=models.CASCADE)
    name_safety = models.CharField(max_length=32)
    icon = models.ImageField(upload_to='icons_safety/', null=True, blank=True)











class Kitchen(models.Model):
    places = models.ForeignKey(Places, on_delete=models.CASCADE)
    name_kitchen = models.CharField(max_length=32)
    category = models.CharField(max_length=32)
    price_range = models.CharField(max_length=32)
    specialized_menu = models.CharField(max_length=100)
    meal_time = models.CharField(max_length=100)
    address = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = PhoneNumberField(null=True,blank=True, region="KG")


    def get_average_rating(self):
        """Вычисление среднего рейтинга для продукта"""
        return self.kitchen.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return f'{self.places} - {self.name_kitchen}'



class KitchenPhotos(models.Model):
    kitchen = models.ForeignKey(Kitchen, related_name='kit_photos', on_delete=models.CASCADE)
    image = models.ImageField()













class Attractions(models.Model):  # Достопремечательности
    att_region = models.ForeignKey(Places, on_delete=models.CASCADE)
    at_name = models.CharField(max_length=32)
    phone_number = PhoneNumberField(null=True,blank=True, region="KG")
    description = models.TextField()

    def __str__(self):
        return f'{self.att_region} - {self.at_name}'


    def get_average_rating(self):
        """Вычисление среднего рейтинга для продукта"""
        return self.att_reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0


class AttractionsPhotos(models.Model):
    attraction = models.ForeignKey(Attractions, related_name='attraction_photos', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)




class CategoryEvent(models.Model):
    category = models.CharField(max_length=32)



class Event(models.Model):
    category = models.ForeignKey(CategoryEvent, on_delete=models.CASCADE)
    places = models.ForeignKey(Places, related_name='events', on_delete=models.CASCADE)
    address = models.CharField(max_length=32)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def str(self):
        return f'{self.category} - {self.title}'








class Review(models.Model):

    REVIEW_TYPE_CHOICES = (
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('attraction', 'Attraction'),
        ('place', 'Place'),
    )

    RATING_CHOICES = [
        (1, 'Плохо'),
        (2, 'Удовлетворительно'),
        (3, 'Средне'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review_type = models.CharField(max_length=50, choices=REVIEW_TYPE_CHOICES)
    hotel = models.ForeignKey(Hotel, null=True, related_name='hotels', blank=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Kitchen, related_name='kitchen', null=True, blank=True, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attractions, related_name='att_reviews', null=True, blank=True, on_delete=models.CASCADE)
    places = models.ForeignKey(Places, related_name='reviews_places', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.PositiveIntegerField(default=0)


class PhotosReview(models.Model):
    review = models.ForeignKey(Review, related_name='reviews_photos', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)














######Culture

class Culture(models.Model):
    culture_name = models.CharField(max_length=32,)
    description = models.TextField()
    image = models.ImageField(upload_to='img_culture/')

    def __str__(self):
        return f'{self.culture_name}'


class Games(models.Model):
    game_name = models.CharField(max_length=32)
    description = models.TextField()
    image = models.ImageField(upload_to='img_games/')

    def __str__(self):
        return f'{self.game_name}'

class NationalClothes(models.Model):
    clothes_name = models.CharField(max_length=32)
    description = models.TextField()
    image = models.ImageField(upload_to='img_clothes/')

    def __str__(self):
        return f'{self.clothes_name}'

class HandCrafts(models.Model):
    handcraft_name = models.CharField(max_length=32)
    description = models.TextField()
    image = models.ImageField(upload_to='img_crafts/')

    def __str__(self):
        return f'{self.handcraft_name}'


class Currency(models.Model):
    currency_name = models.CharField(max_length=32)
    description = models.TextField()
    image = models.ImageField(upload_to='img_currency/')

    def __str__(self):
        return f'{self.currency_name}'


class NationalInstruments(models.Model):
    instrument = models.CharField(max_length=32)
    description = models.TextField()
    image = models.ImageField(upload_to='img_instruments/')

    def __str__(self):
        return f'{self.instrument}'


class NationalFood(models.Model):
    nationalfood_name = models.CharField(max_length=32)
    description = models.TextField()
    image = models.ImageField(upload_to='img_nationalfood/')

    def __str__(self):
        return f'{self.nationalfood_name}'










class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    places = models.ForeignKey(Places, on_delete=models.CASCADE,null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, null=True, blank=True)
    attractions = models.ForeignKey(Attractions, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.cart} - {self.places}'

