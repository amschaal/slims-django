from django.db import migrations

def import_user_groups(apps, schema_editor):
    SlimsUser = apps.get_model("slims", "User")
    UserGroupPermission = apps.get_model("slims", "UserGroupPermission")
    UserGroupRole = apps.get_model("slims", "UserGroupRole")
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")

    # Some users exist multiple times in SLIMS, but weren't imported.  Look up by login.
    user_id_lookup = {}
    for u in User.objects.all():
        user_id_lookup[u.username.lower().strip()] = u.id

    user_groups = set()
    for ugp in UserGroupPermission.objects.all().select_related('user'):
        user_id = user_id_lookup[ugp.user.login.lower().strip()]
        user_groups.add((user_id, ugp.group_id))
    for ugr in UserGroupRole.objects.all().select_related('user'):
        user_id = user_id_lookup[ugr.user.login.lower().strip()]
        user_groups.add((user_id, ugr.group_id))
    UserGroupThrough = User.groups.through
    user_group_relations = [
        UserGroupThrough(user_id=user_id, group_id=group_id)
        for user_id, group_id in list(user_groups)
    ]
    UserGroupThrough.objects.bulk_create(user_group_relations, 100)
    print('Added {} user group relations'.format(len(user_groups)))
    

class Migration(migrations.Migration):

    dependencies = [
        ('slims', '0004_migration_user')
    ]

    operations = [
        migrations.RunPython(import_user_groups),
    ]
