import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.models import GooglePlayApp, ExistingReview

class Command(BaseCommand):
    help = 'Load data from CSV files'
    
    def handle(self, *args, **options):
        # Load Google Play Store apps
        apps_file = os.path.join(settings.BASE_DIR, 'googleplaystore.csv')
        if os.path.exists(apps_file):
            df_apps = pd.read_csv(apps_file)
            
            for _, row in df_apps.iterrows():
                app, created = GooglePlayApp.objects.get_or_create(
                    app_name=row['App'],
                    defaults={
                        'category': row['Category'],
                        'rating': row['Rating'] if pd.notna(row['Rating']) else None,
                        'reviews_count': int(str(row['Reviews']).replace(',', '')) if pd.notna(row['Reviews']) else 0,
                        'size': str(row['Size']),
                        'installs': str(row['Installs']),
                        'app_type': str(row['Type']),
                        # 'price': float(row['Price']) if pd.notna(row['Price']) else 0,
                        'price': float(str(row['Price']).replace('$', '').strip()) if pd.notna(row['Price']) else 0,
                        'content_rating': str(row['Content Rating']),
                        'genres': str(row['Genres']),
                        'last_updated': str(row['Last Updated']),
                        'current_version': str(row['Current Ver']),
                        'android_version': str(row['Android Ver']),
                    }
                )
                if created:
                    self.stdout.write(f'Created app: {app.app_name}')
        
        # Load existing reviews
        reviews_file = os.path.join(settings.BASE_DIR, 'googleplaystore_user_reviews.csv')
        if os.path.exists(reviews_file):
            df_reviews = pd.read_csv(reviews_file)
            
            for _, row in df_reviews.iterrows():
                try:
                    app = GooglePlayApp.objects.get(app_name=row['App'])
                    if pd.notna(row['Translated_Review']):
                        review, created = ExistingReview.objects.get_or_create(
                            app=app,
                            review_text=str(row['Translated_Review']),
                            defaults={
                                'sentiment': str(row['Sentiment']) if pd.notna(row['Sentiment']) else 'Neutral',
                                'sentiment_polarity': float(row['Sentiment_Polarity']) if pd.notna(row['Sentiment_Polarity']) else 0.0,
                                'sentiment_subjectivity': float(row['Sentiment_Subjectivity']) if pd.notna(row['Sentiment_Subjectivity']) else 0.0,
                            }
                        )
                        if created:
                            self.stdout.write(f'Created review for: {app.app_name}')
                except GooglePlayApp.DoesNotExist:
                    self.stdout.write(f'App not found: {row["App"]}')
                except Exception as e:
                    self.stdout.write(f'Error processing review: {e}')
        
        self.stdout.write(self.style.SUCCESS('Data loading completed!'))