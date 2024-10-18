from modeltranslation.translator import TranslationOptions, register
from .models import *

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('address',)
@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('street', 'city',)

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region_name', 'description',)
@register(RegionFood)
class RegionFoodTranslationOptions(TranslationOptions):
    fields = ('food_name', 'include_food', 'description_name',)

@register(Places)
class PlacesTranslationOptions(TranslationOptions):
    fields = ('places_name', 'description',)
@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'description',)

@register(Kitchen)
class KitchenTranslationOptions(TranslationOptions):
    fields = ('name_kitchen', 'category', 'specialized_menu', 'meal_time',)
@register(Attractions)
class AttractionsTranslationOptions(TranslationOptions):
    fields = ('at_name', 'description',)

@register(Culture)
class CultureTranslationOptions(TranslationOptions):
    fields = ('culture_name', 'description',)
@register(Games)
class GamesTranslationOptions(TranslationOptions):
    fields = ('game_name', 'description',)

@register(NationalClothes)
class NationalClothesTranslationOptions(TranslationOptions):
    fields = ('clothes_name', 'description',)
@register(HandCrafts)
class HandCraftsTranslationOptions(TranslationOptions):
    fields = ('handcraft_name', 'description',)

@register(Currency)
class CurrencyTranslationOptions(TranslationOptions):
    fields = ('currency_name', 'description',)
@register(NationalInstruments)
class NationalInstrumentsTranslationOptions(TranslationOptions):
    fields = ('instrument', 'description',)

@register(NationalFood)
class NationalFoodTranslationOptions(TranslationOptions):
    fields = ('nationalfood_name', 'description',)