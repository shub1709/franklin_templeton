import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import GooglePlayApp
from collections import defaultdict

class AppSearchEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.app_vectors = None
        self.apps_df = None
        self.prefix_index = defaultdict(list)  # ⬅️ new fast prefix cache
        self._index_built = False
        self.build_index()

    def build_index(self):
        """Build search index from database"""
        apps = GooglePlayApp.objects.all()
        if not apps.exists():
            return
        
        # Prepare for vectorization
        data = []
        for app in apps:
            searchable_text = f"{app.app_name} {app.category} {app.genres}".lower()
            data.append({
                'id': app.id,
                'app_name': app.app_name,
                'searchable_text': searchable_text
            })

            # Build prefix index
            name = app.app_name.strip()
            for i in range(1, len(name) + 1):
                prefix = name[:i].lower()
                if len(self.prefix_index[prefix]) < 15:
                    self.prefix_index[prefix].append(name)

        self.apps_df = pd.DataFrame(data)

        # Build TF-IDF vectors
        if len(self.apps_df) > 0:
            self.app_vectors = self.vectorizer.fit_transform(self.apps_df['searchable_text'])

        self._index_built = True

    def get_suggestions(self, query, max_suggestions=5):
        """Get fast autocomplete suggestions using prefix index"""
        if not query or len(query) < 3 or not self._index_built:
            return []
        
        return self.prefix_index.get(query.lower(), [])[:max_suggestions]

    def search(self, query, max_results=10):
        """Search for apps using text similarity"""
        if not query or self.app_vectors is None:
            return GooglePlayApp.objects.none()
        
        # Vectorize query
        query_vector = self.vectorizer.transform([query.lower()])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.app_vectors).flatten()
        
        # Top N indices
        top_indices = similarities.argsort()[-max_results:][::-1]
        app_ids = [self.apps_df.iloc[i]['id'] for i in top_indices if similarities[i] > 0]
        
        # Preserve order in QuerySet
        if app_ids:
            apps = GooglePlayApp.objects.filter(id__in=app_ids)
            app_dict = {app.id: app for app in apps}
            return [app_dict[app_id] for app_id in app_ids if app_id in app_dict]

        return []

# Singleton instance
_search_engine = None

def get_search_engine():
    global _search_engine
    if _search_engine is None:
        _search_engine = AppSearchEngine()
    return _search_engine
