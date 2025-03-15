from django.db import migrations

def add_initial_data(apps, schema_editor):
    UserAccount = apps.get_model("api", "UserAccount")
    Player = apps.get_model("api", "Player")
    Role = apps.get_model("api", "Role")
    Country = apps.get_model("api", "Country")
    League = apps.get_model("api", "League")
    Club = apps.get_model("api", "Club")
    Position = apps.get_model("api", "Position")
    Age = apps.get_model("api", "Age")
    ShirtNumber = apps.get_model("api", "ShirtNumber")

    # tworzymy przykładowe role
    admin_role = Role.objects.create(rola="Admin")
    user_role = Role.objects.create(rola="User")

    # tworzymy przykładowych użytkowników
    user1 = UserAccount.objects.create(
        id_role=admin_role, email="admin@gmail.com", login="admin", password="admin123"
    )
    user2 = UserAccount.objects.create(
        id_role=user_role, email="user@gmail.com", login="user", password="user123"
    )

    # tworzymy przykładowe kraje, ligi i kluby
    polska = Country.objects.create(name="Polska", flag_image_path="flags/polska.png")
    premier_league = League.objects.create(name="Premier League", logo_image_path="leagues/premier_league.png")
    la_liga = League.objects.create(name="La Liga", logo_image_path="leagues/la_liga.png")
    fc_barcelona = Club.objects.create(name="FC Barcelona", logo_image_path="clubs/fc_barcelona.png")

    # tworzymy pozycje, wiek i numery koszulek
    striker = Position.objects.create(name="Napastnik", position_image_path="positions/striker.png")
    goalkeeper = Position.objects.create(name="Bramkarz", position_image_path="positions/goalkeeper.png")
    age_36 = Age.objects.create(value=36, age_image_path="ages/36.png")
    age_34 = Age.objects.create(value=34, age_image_path="ages/34.png")
    shirt_9 = ShirtNumber.objects.create(number=9, number_image_path="shirts/9.png")
    shirt_25 = ShirtNumber.objects.create(number=25, number_image_path="shirts/25.png")

    # tworzymy przykładowych piłkarzy
    player1 = Player.objects.create(
        name="Robert Lewandowski",
        country=polska,
        league=la_liga,
        club=fc_barcelona,
        position=striker,
        age=age_36,
        shirt_number=shirt_9,
    )

    player2 = Player.objects.create(
        name="Wojciech Szczęsny",
        country=polska,
        league=la_liga,
        club=fc_barcelona,
        position=goalkeeper,
        age=age_34,
        shirt_number=shirt_25,
    )

class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]
