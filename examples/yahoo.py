from scrapemark import scrape

groups = scrape("""
	<a href='{@
		<table class='ygrp-grps'>
		{*
			<td class='ygrp-g'>
			{* <img src='{{ [].is_manager|bool }}' /> *}
			<a href='{{ [].url|abs }}'>{{ [].title }}</a>
			</td>
		*}
		</table>
	@}'>click here</a>
	""",
	url='https://login.yahoo.com/config/login',
	post={
		'login': 'username',
		'passwd': 'pw',
		'.done': 'http://groups.yahoo.com/'
	})

for group in groups:
	print group
