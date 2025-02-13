from django.db import migrations
from django.utils.crypto import get_random_string

def add_permission(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model('contenttypes', 'ContentType') 

    ct = ContentType.objects.get_for_model(Group)

    Permission.objects.create(codename ='is_pi', name ='Is a PI', content_type = ct)

class Migration(migrations.Migration):

    dependencies = [
        ('slims', '0005_migration_user_groups')
    ]

    operations = [
        migrations.RunPython(add_permission),
    ]
