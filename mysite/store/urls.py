from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Password Reset API",
      default_version='v1',
      description="API для сброса пароля через email",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset-password'),
# {
#     "email": "example@example.com"
# }
    path('reset-password-confirm/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),

# {
#     "password": "new_secure_password"
# }

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),



    path('profile/', UserProfileView.as_view(), name='user-profile'),


    # path('userprofile', UserProfileView.as_view({'get': 'list', 'post': 'create'}), name='userprofile_list'),
    # path('userprofile/<int:pk>/', UserProfileView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='userprofile_detail'),

    # path('address', AddressView.as_view({'get': 'list', 'post': 'create'}), name='address_list'),
    # path('address/<int:pk>/', AddressView.as_view({'get': 'retrieve', 'put': 'update', 'delete':'destroy'}), name='address_detail'),



    path('region', RegionView.as_view({'get': 'list', 'post': 'create'}), name='region_list'),
    path('region/<int:pk>/', RegionView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),name='region_detail'),

    path('region_food', RegionFoodView.as_view({'get': 'list', 'post': 'create'}), name='region_food_list'),
    path('region_food/<int:pk>/', RegionFoodView.as_view({'get': 'retrieve', 'put': 'update', 'delete':'destroy'}), name='region_food_detail'),





    path('places', PlacesViewSet.as_view({'get': 'list', 'post': 'create'}), name='places_list'),
    path('places/<int:pk>/', PlacesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='places_detail'),

    path('places_list', PlacesListView.as_view({'get': 'list', 'post': 'create'}), name='places_list_list'),
    path('place_list/<int:pk>/', PlacesListView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='places_list_detail'),

    path('review', ReviewView.as_view({'get': 'list', 'post': 'create'}), name='review_list'),
    path('review/<int:pk>/', ReviewView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='review_detail'),






    path('hotel', HotelView.as_view({'get': 'list', 'post': 'create'}), name='hotel_list'),
    path('hotel/<int:pk>/', HotelView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),name='hotel_detail'),

    path('hotel_list', HotelListView.as_view({'get':'list'}), name='hotel_list_list'),





    path('attractions', AttractionsView.as_view({'get': 'list', 'post': 'create'}), name='attractions_list'),
    path('attractions/<int:pk>/', AttractionsView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='attractions_detail'),

    path('attraction_list', AttractionListView.as_view({'get': 'list'}), name='attraction_list_list'),

    path('attractions_regions_list', AttractionSimpleListView.as_view({'get': 'list'}), name='attraction_region_list'),




    path('kitchen_list', KitchenListView.as_view({'get': 'list'}), name='kitchen_list_list'),

    path('kitchen', KitchenView.as_view({'get':'list', 'post':'create'}), name='kitchen_list'),
    path('kitchen/<int:pk>/', KitchenView.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'}), name='kitchen_detail'),




    path('events', EventViewSet.as_view({'get':'list', 'post':'create', }), name='event_list'),
    path('events/<int:pk>/', EventViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete':'destroy' }), name='event_detail'),




    path('cart', CartView.as_view({'get': 'list', 'post': 'create'}), name='cart_list'),
    path('cart/<int:pk>/', CartView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='cart_detail'),

    path('cart_items', CartItemsView.as_view({'get': 'list', 'post': 'create'}), name='cart_item_list'),
    path('cart_items/<int:pk>/', CartItemsView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='cart_item_detail'),







    path('culture', CultureView.as_view({'get': 'list', 'post': 'create'}), name='culture_list'),
    path('culture/<int:pk>/', CultureView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='culture_detail'),

    path('games', GamesView.as_view({'get': 'list', 'post': 'create'}), name='games_list'),
    path('games/<int:pk>/', GamesView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='games_detail'),

    path('national_clothes', NationalClothesView.as_view({'get': 'list', 'post': 'create'}),
         name='nationalclothes_list'),
    path('national_clothes/<int:pk>/',
         NationalClothesView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='nationalclothes_detail'),

    path('currency', CurrencyView.as_view({'get': 'list', 'post': 'create'}), name='currency_list'),
    path('currency/<int:pk>/', CurrencyView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='currency_detail'),

    path('national_instruments', NationalInstrumentsView.as_view({'get': 'list', 'post': 'create'}),
         name='nationalinstruments_list'),
    path('national_instruments/<int:pk>/',
         NationalInstrumentsView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='nationalinstruments_detail'),

    path('national_food', NationalFoodView.as_view({'get': 'list', 'post': 'create'}), name='nationalfood_list'),
    path('national_food/<int:pk>/', NationalFoodView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='nationalfood_detail'),

]

