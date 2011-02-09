from scrapemark import scrape

links = scrape("""
	<tr(2)>
	{*
		<tr><td(2)>
		<a href='{{ [].url|abs }}'>{{ [].title }}</a>
		</td></tr>
		<tr><td>
		<span>{{ [].points|int }} point</span>
		<a(1)>{{ [].comments|int }} comment</a>
		</td></tr>
	*}
	</tr>
	""",
	url='http://news.ycombinator.com/')
	
for link in links:
	print link
