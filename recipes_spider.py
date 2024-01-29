import scrapy

class RecipesSpider(scrapy.Spider):
    name = 'recipes'
    start_urls = ['https://www.atelierdeschefs.fr/recettes/']

    def parse(self, response):
        # Suivez les liens des recettes depuis la page d'accueil
        recipe_links = response.css('a.recipe-link::attr(href)').getall()
        for recipe_link in recipe_links:
            yield scrapy.Request(url=recipe_link, callback=self.parse_recipe)

        # Suivez le lien de pagination s'il existe
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_recipe(self, response):
        # Définissez ici votre logique de parsing pour extraire les détails de la recette
        recipe_title = response.css('h1.fs-title::text').get()
        ingredients = response.css('div.Line_ingredient_container__E_6Zi::text').getall()
        instructions = response.css('div.Steps_container__lVB7Z::text').getall()

        yield {
            'recipe_title': recipe_title,
            'ingredients': ingredients,
            'instructions': instructions,
        }
