#Importing Scrapy 
import scrapy

#Defining class for spider, including starting URLs and base URL
class metacriticspider(scrapy.Spider):
    name = "metacriticspider"
    start_urls = [
        "https://www.metacritic.com/browse/games/release-date/new-releases/ps5/date",
        "https://www.metacritic.com/browse/games/release-date/new-releases/ps4/date",
        "https://www.metacritic.com/browse/games/release-date/new-releases/xbox-series-x/date",
        "https://www.metacritic.com/browse/games/release-date/new-releases/xbox-one/date",
        "https://www.metacritic.com/browse/games/release-date/new-releases/switch/date",
        "https://www.metacritic.com/browse/games/release-date/new-releases/pc/date",
        "https://www.metacritic.com/browse/games/release-date/new-releases/ios/date"
    ]
    base_url = "https://www.metacritic.com"

    #Define custome setting to provide output in csv file. 
    custom_settings = {
        "FEED_FORMAT": "csv",
        "FEED_URI": "metacritic.csv"
    }
    #Define function to loop through individual games' links to extract title, URL, and game details. 
    def parse(self, response):
        for game_link in response.xpath("//td[@class='clamp-summary-wrap']/a"):
            game_url = self.base_url + game_link.attrib["href"]
            title = game_link.css(".//h3/text()").get().strip()
            platform = response.url.split("/")[-3].upper()
            yield scrapy.Request(game_url, callback=self.parse_game, meta={"title": title, "platform": platform})
    
        #Identify next page linkation 
        next_page_link = response.xpath("//a[contains(@class, 'next')]/@href")
        if next_page_link:
            next_page_url = self.base_url + next_page_link.get()
            yield scrapy.Request(next_page_url, callback=self.parse)

    #Define function to extract title and genres from response and create dictionary containing titles and genres. 
    def parse_game(self, response):
        title = response.xpath("normalize-space(//h1/text())").get()
        genres = response.xpath("//li[contains(@class,'product_genre')]/span/text()")
        yield {
            "title": title,
            "genres": genres.getall(),
        }
