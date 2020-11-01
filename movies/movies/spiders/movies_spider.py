import scrapy

# Título = //td[@class="titleColumn"]/a/text()
# Año = //td[@class="titleColumn"]/span[@class="secondaryInfo"]/text()
# Calificación = //td[contains(@class, "imdbRating")]/strong/text()
# Thumbnail = //td[@class="posterColumn"]/a/img/@src

class MoviesSpider(scrapy.Spider):
  name="movies"
  start_urls=[
    "https://www.imdb.com/chart/top/"
  ]
  custom_settings = {
    'FEEDS':{
      'movies.json': {
        "format": "json",
        "encoding": "utf8",
        "indent": 4,
      }
    }
  }

  def parse(self, response):
    titles = response.xpath('//td[@class="titleColumn"]/a/text()').getall()
    anios = response.xpath('//td[@class="titleColumn"]/span[@class="secondaryInfo"]/text()').getall()
    calificaciones = response.xpath('//td[contains(@class, "imdbRating")]/strong/text()').getall()
    thumbnails = response.xpath('//td[@class="posterColumn"]/a/img/@src').getall()

    for i in range(len(titles)):
      raw_thumbnail = thumbnails[i]
      thumbnail = raw_thumbnail[:raw_thumbnail.rfind("@")] + "@.jpg"
      yield {
        "titles": titles[i],
        "anios": anios[i].replace('(','').replace(')',''),
        "calificaciones": calificaciones[i],
        "thumbnails": thumbnail,
      }