import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_seed_goals'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='savingsgoal',
            name='user',
            field=models.ForeignKey(
                blank=True,
                help_text='Owner of this savings goal',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='savings_goals',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
