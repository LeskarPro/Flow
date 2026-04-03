import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_budget_limit', models.DecimalField(
                    blank=True,
                    decimal_places=2,
                    help_text='Monthly budget limit for expenses',
                    max_digits=10,
                    null=True,
                    validators=[django.core.validators.MinValueValidator(0)],
                )),
                ('currency', models.CharField(
                    choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('BGN', 'BGN')],
                    default='EUR',
                    max_length=3,
                )),
                ('email_notifications', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='profile',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
