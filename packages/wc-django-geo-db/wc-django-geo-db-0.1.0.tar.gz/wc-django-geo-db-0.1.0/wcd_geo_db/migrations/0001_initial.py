# Generated by Django 3.2 on 2021-06-08 07:24

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('codes', models.JSONField(default=dict, verbose_name='Codes')),
                ('name', models.TextField(verbose_name='Name')),
                ('path', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), default=list, editable=False, size=None, verbose_name='Hierarchy path')),
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1200, 'Country'), (1410, 'Administrative division: Level 1'), (1420, 'Administrative division: Level 2'), (1430, 'Administrative division: Level 3'), (1440, 'Administrative division: Level 4'), (1450, 'Administrative division: Level 5'), (1600, 'Locality'), (1810, 'Locality division: Level 1'), (1820, 'Locality division: Level 2'), (1830, 'Locality division: Level 3'), (1840, 'Locality division: Level 4'), (1850, 'Locality division: Level 5')], verbose_name='Division level')),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), blank=True, default=list, size=None, verbose_name='Division types')),
            ],
            options={
                'verbose_name': 'Division',
                'verbose_name_plural': 'Divisions',
            },
        ),
        migrations.CreateModel(
            name='Geometry',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, null=True, srid=4326, verbose_name='Location')),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(blank=True, geography=True, null=True, srid=4326, verbose_name='Polygon')),
            ],
            options={
                'verbose_name': 'Geometry',
                'verbose_name_plural': 'Geometries',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('codes', models.JSONField(default=dict, verbose_name='Codes')),
                ('name', models.TextField(verbose_name='Name')),
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), blank=True, default=list, size=None, verbose_name='Route types')),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.division', verbose_name='Division')),
                ('geometry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.geometry', verbose_name='Geometry')),
                ('grouping', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.route', verbose_name='Grouping entity')),
            ],
            options={
                'verbose_name': 'Route',
                'verbose_name_plural': 'Routes',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('codes', models.JSONField(default=dict, verbose_name='Codes')),
                ('name', models.TextField(verbose_name='Name')),
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), blank=True, default=list, size=None, verbose_name='Place types')),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.division', verbose_name='Division')),
                ('geometry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.geometry', verbose_name='Geometry')),
                ('grouping', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.place', verbose_name='Grouping entity')),
                ('route', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.route', verbose_name='Route')),
            ],
            options={
                'verbose_name': 'Place',
                'verbose_name_plural': 'Places',
            },
        ),
        migrations.AddField(
            model_name='division',
            name='geometry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.geometry', verbose_name='Geometry'),
        ),
        migrations.AddField(
            model_name='division',
            name='parent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcd_geo_db.division', verbose_name='Parent entity'),
        ),
    ]
