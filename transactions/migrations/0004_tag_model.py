import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaction_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Create the Tag model
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Short label, e.g. 'tax-deductible' or 'one-off'", max_length=30)),
                ('color', models.CharField(
                    choices=[
                        ('primary', 'Blue'),
                        ('success', 'Green'),
                        ('danger', 'Red'),
                        ('warning', 'Yellow'),
                        ('info', 'Light Blue'),
                        ('secondary', 'Gray'),
                    ],
                    default='secondary',
                    help_text='Badge colour shown in the UI',
                    max_length=20,
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tags',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        # Unique constraint: same user can't have two tags with the same name
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('user', 'name')},
        ),
        # Add the M2M field on Transaction
        migrations.AddField(
            model_name='transaction',
            name='tags',
            field=models.ManyToManyField(
                blank=True,
                help_text='Optional labels for this transaction',
                to='transactions.tag',
            ),
        ),
    ]
