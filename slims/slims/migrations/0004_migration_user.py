from django.db import migrations
from django.utils.crypto import get_random_string

def import_users(apps, schema_editor):
    SlimsUser = apps.get_model("slims", "User")
    User = apps.get_model("auth", "User")
    duplicate_users = []
    users = []
    used_logins = set()
    for u in SlimsUser.objects.all():
        username = u.login.lower().strip()
        if username in used_logins:
            duplicate_users.append(username)
            continue
        password = u.password or get_random_string(length=32)
        users.append(User(pk=u.pk, username=username, email=username, password=password, first_name=u.firstname, last_name=u.lastname))
        used_logins.add(username)
    User.objects.bulk_create(users, 100)
    print('{} duplicate users ignored: {}'.format(len(duplicate_users), ', '.join(duplicate_users)))
    

class Migration(migrations.Migration):

    dependencies = [
        ('slims', '0003_alter_runlane_group')
    ]

    operations = [
        migrations.RunPython(import_users),
    ]
