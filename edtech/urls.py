from django.contrib import admin
from django.urls import path, include
from home import views as home_views
from tests import views as test_views, api as test_api
from entrance import views as entrance_views
from library import views as lib_views, api as lib_api
from dashboard import views as dash_views
from profiles import views as profile_views
from payment import views as payment_views
from practice import views as practice_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    #home
    path('', home_views._home, name='home'),
    path('nope/', home_views.nope, name='nope'),
    
    # test api
    path('test/submit-answer/<str:key>/<int:answer_id>/<int:option_id>', test_api.post_answer),
    
    # test
    path('test/<str:key>', test_views.test_handler),
    path('quick-test', test_views.quick_test, name='quick-test'),
    path('chapter-quick-test/<int:chapter_id>', test_views.chapter_quick_test),
    path('admission-quick-test/<int:adm_id>', test_views.adm_quick_test),
    path('general-quick-test/<str:metadata_ids>', test_views.general_quick_test),
    path('start-quick-test/<str:key>', test_views.start_quick_test),
    path('all-tests', test_views.all_tests, name='all-tests'),
    
    # library
    path('library/', lib_views.chapter_library, name='library'), 
    path('study/<int:chapter_id>', lib_views.study), 
    path('all-topics/<int:chapter_id>', lib_views.all_topics),
    path('topic/<int:level_id>', lib_views.study_topic),
    
    # library api 
    path('amar-onek-buddhi/<str:gibberish>', lib_api.amar_onek_buddhi), 
    
    # dashbaord
    path('dashboard/', dash_views.dashboard, name='dashboard'),
    path('solved-answer-sheet/<str:key>', dash_views.detailed_report),
    
    # profiles
    path('profile', profile_views.profile, name='profile'),
    path('add-phone-number', profile_views.add_phone_number, name='add-phone-number'),
    path('update-full-name', profile_views.update_full_name, name='update-full-name'),
    path('set-password', profile_views.set_password, name='set-password'),
    
    # entrance
    path('auth-email', entrance_views.auth_email, name='login'),
    path('forgot-password', entrance_views.forgot_password, name='forgot-password'),
    path('auth-pwd/<str:key>', entrance_views.auth_pwd),
    path('auth-codes/<str:code_type>/<str:key>', entrance_views.auth_codes),
    path('logout/', entrance_views.logout, name='logout'),
    
    # payment
    path('upgrade-to-premium', payment_views.upgrade_to_premium, name='upgrade-to-premium'),
    path('purchase/<str:key>', payment_views.purchase_through_link),
    
    # practice
    path('practise', practice_views.practice_home_page, name='practice-home-page'),
    path('practise-chapter/<int:chapter_id>', practice_views.pracrise_chapter),
    path('practise-admission-test-question/<int:adm_id>', practice_views.pracrise_adm),
]
