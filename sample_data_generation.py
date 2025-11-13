import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import json

fake = Faker()
Faker.seed(42)
random.seed(42)

# --- USERS ---
ce_countries = [
    'AT', # Austria
    'HR', # Croatia
    'CZ', # Czech Republic
    'DE', # Germany
    'HU', # Hungary
    'LT', # Lithuania
    'PL', # Poland
    'SK', # Slovakia
    'SI', # Slovenia
    'CH', # Switzerland
    'LI'  # Liechtenstein
]
age_groups = ['TEENAGER', 'YOUNG', 'ADULT', 'SENIOR']
account_types = ['FREEMIUM', 'PREMIUM']

users = []
for i in range(220):
    email = fake.unique.email()
    country = random.choice(ce_countries)
    age_group = random.choices(age_groups, weights=[0.2, 0.3, 0.4, 0.1])[0]
    account_type = random.choices(account_types, weights=[0.5, 0.5])[0]
    users.append([email, country, age_group, account_type])

users_df = pd.DataFrame(users, columns=['id', 'country', 'age_group', 'account_type'])
users_df.to_csv('input-sample/users.csv', index=False)

# --- TRACKS ---
genres = ['Pop', 'Rap', 'HipHop', 'Rock', 'Jazz', 'Classical', 'EDM', 'Country']
artists = [fake.unique.name() for _ in range(60)]
tracks = []
for i in range(220):
    track_id = fake.unique.bothify(text='??###????####')
    artist = random.choice(artists)
    genre = random.choice(genres)
    duration = random.randint(90, 300)
    release_year = random.randint(2000, 2024)
    tracks.append([track_id, artist, genre, duration, release_year])

tracks_df = pd.DataFrame(tracks, columns=['Id', 'artist', 'genre', 'duration_seconds', 'release_date'])
tracks_df.to_csv('input-sample/tracks.csv', index=False)

# --- PLAYS ---
plays = []
start_date = datetime(2020, 1, 1)
today = datetime.today()
date_range_days = (today - start_date).days

# Helper to get all months between start and end
months = []
cur = start_date.replace(day=1)
while cur <= today:
    months.append(cur)
    if cur.month == 12:
        cur = cur.replace(year=cur.year + 1, month=1)
    else:
        cur = cur.replace(month=cur.month + 1)

# For each user, for each month, generate multiple plays for a few tracks
for user in users_df.itertuples(index=False):
    user_country = user.country
    for month_start in months:
        # Pick 2-4 random tracks for this user in this month
        tracks_this_month = tracks_df.sample(random.randint(2, 4))
        for track in tracks_this_month.itertuples(index=False):
            # Generate 2-5 plays for this track in this month
            for _ in range(random.randint(2, 5)):
                play_duration = random.randint(5, min(track.duration_seconds, 180))
                # Pick a random day in this month
                days_in_month = (month_start.replace(month=month_start.month % 12 + 1, year=month_start.year + (month_start.month // 12)) - month_start).days if month_start != months[-1] else (today - month_start).days + 1
                play_day = random.randint(0, days_in_month - 1)
                play_date = month_start + timedelta(days=play_day)
                # Only generate plays up to today
                if play_date > today:
                    continue
                plays.append({
                    "user_id": user.id,
                    "track_id": track.Id,
                    "play_duration_seconds": play_duration,
                    "play_date": play_date.strftime('%Y-%m-%d')
                })

with open('input-sample/plays.jsonl', 'w') as f:
    for row in plays:
        f.write(json.dumps(row) + "\n")

print("Sample data generated in ../input-sample/")