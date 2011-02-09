from scrapemark import scrape

groups = scrape("""
	<noscript>
	<a href='{@
		location.replace("{@|unescape
			<div id='GHP_compact_my_groups'><table><table>
			{*
				<table><table>
				<a href='{{ [].url|abs }}'>{{ [].title }}</a>
				{* <a href='{{ [].is_manager|bool }}'>manage</a> *}
				</table></table>
			*}
			</table></table></div>
		@}")
	@}'/>
	</noscript>
	""",
	url='https://www.google.com/accounts/ServiceLoginBoxAuth',
	post={
        'continue': 'http://groups.google.com/groups/auth?_done=http%3A%2F%2Fgroups.google.com%2F',
        'service': 'groups2',
        'cd': 'US',
        'hl': 'en',
        'nui': '1',
        'Email': 'email',
        'Passwd': 'pw'
	})
	
for group in groups:
	print group
