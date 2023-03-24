# Generated by Django 4.0.4 on 2023-03-24 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def set_user_to_first_user_for_null_user_notes(apps, schema_editor):
    Note = apps.get_model('notes', 'Note')
    User = apps.get_model(settings.AUTH_USER_MODEL)

    first_user = User.objects.first()
    if first_user:
        Note.objects.filter(user__isnull=True).update(user=first_user)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0004_alter_note_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(set_user_to_first_user_for_null_user_notes),
    ]