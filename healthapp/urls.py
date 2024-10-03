from django.urls import path
from healthapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # Add this import
from .views import appointment

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('products', views.products),
    path('search', views.search),
    path('catfilter/<cv>', views.catfilter),
    path('sortbyprice/<sv>', views.sortbyprice),
    path('medsdetail/<pid>',views.medsdetail),
    path('addtocart/<pid>',views.addtocart),
    path('orders',views.viewcart),
    path('remove/<cid>',views.remove),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),

    # **************check up*****************
    path('bmi', views.bmi),
    path('mental', views.mental),
    path('dietnut', views.dietnut),
    path('sleep', views.sleep),
    path('vision', views.vision),

    # **************level up*****************
    path('diet', views.diet),
    path('obasity', views.obasity),
    path('underweight', views.underweight),
    path('mentalhealth', views.mentalhealth),
    path('goals', views.goals),

    # ************** Blog *****************
    path('blogs', views.blogs),
    path('news', views.news),
    path('daily', views.daily),

    # ************** User *****************
    path('login', views.user_login),
    path('register', views.register),
    path('logout', views.user_logout),
   
    # path('appointment', views.appointment),
    path('appointment/', appointment, name='appointment'),
    path('success/', appointment, name='success'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
 
    # *********************profile********************** 
    path('dashboard', views.dashboard),
]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
