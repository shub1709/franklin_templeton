import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import GooglePlayApp
import re

class AppSearchEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.app_vectors = None
        self.apps_df = None
        self._build_index()
    
    def _build_index(self):
        """Build search index from database"""
        apps = GooglePlayApp.objects.all()
        if not apps.exists():
            return
        
        # Create DataFrame for vectorization
        data = []
        for app in apps:
            searchable_text = f"{app.app_name} {app.category} {app.genres}".lower()
            data.append({
                'id': app.id,
                'app_name': app.app_name,
                'searchable_text': searchable_text
            })
        
        self.apps_df = pd.DataFrame(data)
        
        # Build TF-IDF vectors
        if len(self.apps_df) > 0:
            self.app_vectors = self.vectorizer.fit_transform(self.apps_df['searchable_text'])
    
    def get_suggestions(self, query, max_suggestions=5):
        """Get autocomplete suggestions"""
        if not query or len(query) < 3 or self.apps_df is None:
            return []
        
        query_lower = query.lower()
        suggestions = []
        
        for _, row in self.apps_df.iterrows():
            app_name = row['app_name']
            if query_lower in app_name.lower():
                suggestions.append(app_name)
                if len(suggestions) >= max_suggestions:
                    break
        
        return suggestions
    
    def search(self, query, max_results=10):
        """Search for apps using text similarity"""
        if not query or self.app_vectors is None:
            return GooglePlayApp.objects.none()
        
        # Vectorize query
        query_vector = self.vectorizer.transform([query.lower()])
        
        # Calculate similarity
        similarities = cosine_similarity(query_vector, self.app_vectors).flatten()
        
        # Get top results
        top_indices = similarities.argsort()[-max_results:][::-1]
        app_ids = [self.apps_df.iloc[i]['id'] for i in top_indices if similarities[i] > 0]
        
        # Return QuerySet preserving order
        if app_ids:
            apps = GooglePlayApp.objects.filter(id__in=app_ids)
            # Preserve order
            app_dict = {app.id: app for app in apps}
            return [app_dict[app_id] for app_id in app_ids if app_id in app_dict]
        
        return []

# Initialize search engine instance
# search_engine = AppSearchEngine()


# ✅ Lazy initialization
_search_engine = None

def get_search_engine():
    global _search_engine
    if _search_engine is None:
        _search_engine = AppSearchEngine()
        _search_engine.build_index()
    return _search_engine