import os

ARTICLES_HOME = os.environ.get('ARTICLES_HOME') if os.environ.get('ARTICLES_HOME') else 'articles'
TEMPLATES_HOME = os.environ.get('TEMPLATES_HOME') if os.environ.get('TEMPLATES_HOME') else 'templates'
INDEX_TEMPLATE = os.environ.get('INDEX_TEMPLATE') or os.path.join(TEMPLATES_HOME, 'index_template.html')
INDEX_PAGE = os.environ.get('INDEX_PAGE') or os.path.join(TEMPLATES_HOME, 'index.html')
