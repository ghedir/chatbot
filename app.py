from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
from scrapy.crawler import CrawlerProcess
from recipes_spider import RecipesSpider
import random



recipe_urls = [
     {"url": "https://www.atelierdeschefs.fr/recettes/29084/sable-aux-agrumes/", "type": "dessert"},
     {"url": "https://www.atelierdeschefs.fr/recettes/13991/roti-de-veau-aux-agrumes/", "type": "plat_principal"},
     {"url": "https://www.atelierdeschefs.fr/recettes/3164/cocktail-florida-aux-agrumes/", "type": "boisson"}
 ]

# Fonction pour effectuer le scraping à l'aide de Scrapy
def scrape_recipe(url):
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',  # Fichier de sortie pour stocker les résultats du scraping
    })

    # Ajoutez votre spider à la processus Scrapy
    process.crawl(RecipesSpider, start_urls=[url])
    process.start()

    # Lisez les résultats à partir du fichier de sortie
    with open('output.json', 'r') as f:
        results = f.read()

    return results
# Liste des URLs des recettes



# Route principale pour afficher la page HTML
@app.route('/')
def index():
    return render_template('chat.html')

# Route pour le chatbot (traitement des questions de l'utilisateur)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('user_input', '')
    recipe_type = request.json.get('recipe_type', '')  # Ajoutez cette ligne pour récupérer le type de recette

    # Exemple simple : si la question contient "recipe", effectuer le scraping
    if 'recipe' in user_input.lower():
        # Choisissez une URL de recette au hasard depuis la liste en fonction du type de recette
        filtered_urls = [recipe['url'] for recipe in recipe_urls if recipe_type in recipe['type']]
        if filtered_urls:
            selected_url = random.choice(filtered_urls)
            results = scrape_recipe(selected_url)
        else:
            results = ["Aucune recette disponible pour le type spécifié."]
    else:
        results = ["Je suis désolé, je ne comprends pas cette question."]

    return jsonify({'response': results})

if __name__ == '__main__':
    app.run(debug=True)
