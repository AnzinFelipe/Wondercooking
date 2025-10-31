from django.db import migrations

def criar_alergias_padrao(apps, schema_editor):
    Alergias = apps.get_model('postagens', 'Alergias')
    
    alergias_padrao = [
        'Glúten',
        'Lactose', 
        'Amendoim',
        'Ovo',
        'Frutos do mar',
        'Soja',
        'Nozes',
        'Castanhas',
        'Trigo',
        'Peixe',
        'Mariscos',
        'Sésamo',
    ]
    
    for alergia in alergias_padrao:
        Alergias.objects.get_or_create(alergia=alergia)

def reverse_alergias(apps, schema_editor):
    Alergias = apps.get_model('postagens', 'Alergias')
    Alergias.objects.filter(alergia__in=[
        'Glúten', 'Lactose', 'Amendoim', 'Ovo', 'Frutos do mar',
        'Soja', 'Nozes', 'Castanhas', 'Trigo', 'Leite', 'Peixe',
        'Mariscos', 'Sésamo'
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('postagens', '0002_alergias_perfil_alergia_postagem_alergia'),
    ]

    operations = [
        migrations.RunPython(criar_alergias_padrao, reverse_alergias),
    ]