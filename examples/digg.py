import scrapemark

print scrapemark.scrape("""
	{*
		<div class='news-summary'>
		<h3><a href='{{ [links].url }}'>{{ [links].title }}</a></h3>
		<p>{{ [links].description }}</p>
		<li class='digg-count'>
		<strong>{{ [links].diggs|int }}</strong>
		</li>
		</div>
	*}
	""",
	url='http://digg.com/')
