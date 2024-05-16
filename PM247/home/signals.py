from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from home.models import Engineer_Availability

@receiver(post_migrate)
def add_view_engineers_today_permission(sender, **kwargs):
    if sender.name == 'home':
        content_type = ContentType.objects.get_for_model(Engineer_Availability)
        Permission.objects.get_or_create(
            codename='view_engineers_today',
            name='Can view engineers available today',
            content_type=content_type,
        )
@receiver(post_migrate)
def view_index_permission(sender, **kwargs):
    if sender.name == 'home':
        content_type = ContentType.objects.get_for_model(Engineer_Availability)
        Permission.objects.get_or_create(
            codename='view_index',
            name='Can view index',
            content_type=content_type,
        )

@receiver(post_migrate)
def view_engr_list_permission(sender, **kwargs):
    if sender.name == 'home':
        content_type = ContentType.objects.get_for_model(Engineer_Availability)
        Permission.objects.get_or_create(
            codename='view_engineer_list',
            name='Can view engineer list',
            content_type=content_type,
        )
        
@receiver(post_migrate)
def view_engr_search_permission(sender, **kwargs):
    if sender.name == 'home':
        content_type = ContentType.objects.get_for_model(Engineer_Availability)
        Permission.objects.get_or_create(
            codename='view_engineer_search',
            name='Can search engineer ',
            content_type=content_type,
        )

