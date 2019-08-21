
# Scrapemark Examples

Most of the time, you’ll be doing something like this:

```py
from scrapemark import scrape

scrape("""
  your pattern here
  """,
  url='http://someurl.com/')
```

However, for the sake of these examples, we will be passing the html argument to scrapemark.scrape(). The html argument will have the following string value:

```html
<html>
<head>
<title>The Site Title :: The Page Title</title>
<META HTTP-EQUIV=REFRESH CONTENT="1; URL=http://otherurl.com/">
</head>
<body>

<ul id='nav' class='section'>
<li><span><a href='home.html'>Home</a></span></li>
<li><span><a href='about.html'>About</a></span></li>
<li><span><a href='photos.html'>Photos</a></span></li>
</ul>

<div id='content' class='section'>
Look at these data points
<table>
<tr><th>Day</th><th>Test 1</th><th>Test 2</th></tr>
<tr><td>1</td><td>5.6</td><td>24.5</td></tr>
<tr><td>2</td><td>1.1</td><td>12.8</td></tr>
<tr><td>3</td><td>2.4</td><td>5.67</td></tr>
</table>
</div>

<div id='footer' class='section'>
<a href='disclaimer.html'>Disclaimer</a> | <a href='contact.html'>Contact</a>
</div>

</body>
</html>
```

**scrape some text:**

```py
scrape("""
  <title>:: {{ page_title }}</title>
  """,
  html)

# will get...
{'page_title': 'The Page Title'}
```

**scrape some text (quick version):**

```py
scrape("""
  <title>:: {{ }}</title>
  """,
  html)

# will get...
'The Page Title'
```

**loop over certain divs, scrape a list:**

```py
scrape("""
  <body>
  {*
    <div class='section' id='{{ [section_ids] }}' />
  *}
  </body>
  """,
  html)

# will get...
{'section_ids': ['nav', 'content', 'footer']}
```

**scrape text before a certain element:**

```py
scrape("""
  <div id='content'>
  {{ before_table }}
  <table />
  </div>
  """,
  html)

# will get...
{'before_table': 'Look at these data points'}
```

**scrape a column from a table (as a list of ints):**

```py
scrape("""
  <table>
  <tr />
  {*
    <tr>
    <td>{{ [day_numbers]|int }}</td>
    </tr>
  *}
  </table>
  """,
  html)

# will get...
{'day_numbers': [1, 2, 3]}
```

**scrape the entire table with nested loops and dot-notation:**

```py
scrape("""
  <table>
  <tr />
  {*
    <tr>
    <td>{{ [days].number|int }}</td>
    {*
      <td>{{ [days].[points]|float }}</td>
    *}
    </tr>
  *}
  </table>
  """,
  html)

# will get...
{'days': [
  {'number': 1, 'points': [5.6, 24.5]},
  {'number': 2, 'points': [1.1, 12.8]},
  {'number': 3, 'points': [2.4, 5.67]}
]}
```

**preserve HTML when you scrape:**

```py
scrape("""
  <div id='footer'>{{ footer|html }}</div>
  """,
  html)

# will get...
{'footer': "<a href='disclaimer.html'>Disclaimer</a> | <a href='contact.html'>Contact</a>"}
```

**visit another page and scrape it:**

```py
scrape("""
  <head>
  <meta http-equiv='refresh' content='url={@
    <title>{{ title }}</title>
  @}'/>
  </head>
  """,
  html)

# will get...
{'title': 'whatever the title of http://otherurl.com/ is'}
```