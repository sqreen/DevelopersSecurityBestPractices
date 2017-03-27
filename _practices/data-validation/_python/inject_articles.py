from app import COLLECTION

# Inject some articles in python and security categories
COLLECTION.insert({'title': 'Running js in python', 'category': 'python'})
COLLECTION.insert({'title': 'How to safely store password', 'category': 'security'})

# And inject an article in the draft category that shouldn't be shown
COLLECTION.insert({'title': 'My secret draft', 'category': 'drafts'})
