import datetime
from django.db import migrations, models
import django.db.models.deletion
from page.utils import top_level


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_path', models.CharField(db_index=True, help_text=' - absolute path, excluding the domain name. Example: "/some/path"', max_length=200, unique=True, verbose_name='redirect from')),
                ('new_path', models.CharField(blank=True, help_text=' - either an absolute path (as above) or a full URL starting with "http(s)://"', max_length=200, verbose_name='redirect to')),
                ('usage_count', models.PositiveIntegerField(blank=True, default=0, editable=False, null=True)),
                ('last_used', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('author', models.CharField(blank=True, max_length=150, null=True)),
                ('slug', models.SlugField(max_length=75, verbose_name='URL slug')),
                ('active', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('parent', models.ForeignKey(blank=True, limit_choices_to=top_level, null=True, on_delete=django.db.models.deletion.SET_NULL, to='page.Page', verbose_name='Section')),
            ],
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['parent__slug', 'slug']},
        ),
        migrations.AlterModelOptions(
            name='redirect',
            options={'ordering': ['old_path']},
        ),
    ]
