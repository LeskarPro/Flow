from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(
                blank=True,
                help_text='Profile picture (optional)',
                null=True,
                upload_to='profile_pictures/',
            ),
        ),
    ]
