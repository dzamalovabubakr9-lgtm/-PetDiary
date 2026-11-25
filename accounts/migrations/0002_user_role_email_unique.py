from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial')]
    operations = [
        migrations.AddField(
            model_name='user', name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('admin', 'Администратор')], db_index=True, default='user', max_length=10),
        ),
        migrations.AlterField(
            model_name='user', name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
    ]
