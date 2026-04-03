from django.db import migrations


def create_user_groups(apps, schema_editor):
    """
    Create the two default user groups:
    - Viewer: can only read data (view permissions)
    - Editor: can create, edit and delete data
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    viewer_group, _ = Group.objects.get_or_create(name='Viewer')
    editor_group, _ = Group.objects.get_or_create(name='Editor')

    view_codenames = [
        'view_transaction',
        'view_category',
        'view_savingsgoal',
        'view_profile',
    ]

    editor_codenames = [
        'add_transaction', 'change_transaction', 'delete_transaction', 'view_transaction',
        'add_category', 'change_category', 'delete_category', 'view_category',
        'add_savingsgoal', 'change_savingsgoal', 'delete_savingsgoal', 'view_savingsgoal',
        'view_profile', 'change_profile',
    ]

    viewer_group.permissions.set(
        Permission.objects.filter(codename__in=view_codenames)
    )
    editor_group.permissions.set(
        Permission.objects.filter(codename__in=editor_codenames)
    )


def remove_user_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Viewer', 'Editor']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('transactions', '0001_initial'),
        ('categories', '0001_initial'),
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_groups, remove_user_groups),
    ]
