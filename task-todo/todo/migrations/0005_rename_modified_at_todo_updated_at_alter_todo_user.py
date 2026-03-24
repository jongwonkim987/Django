# Generated manually

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_alter_comment_message_alter_comment_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # modified_at → updated_at (컬럼명 변경)
        migrations.RenameField(
            model_name='todo',
            old_name='modified_at',
            new_name='updated_at',
        ),
        # user FK에서 null=True 제거 (기존 null 데이터 없음 확인됨)
        migrations.AlterField(
            model_name='todo',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
