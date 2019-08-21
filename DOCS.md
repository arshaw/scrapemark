
# Scrapemark Docs

ScrapeMark is analagous to a [regular expression](http://docs.python.org/library/re.html) engine. A ‘pattern’ with special syntax is applied to the HTML being scraped. If the pattern correctly matches, captured values are returned.

ScrapeMark’s pattern syntax is simpler than regular expression syntax and is optimized for use with HTML. Also, better utilities are provided for structuring and modifying captured text before being returned.

Internally, ScrapeMark compiles a pattern down to a set of regular expressions, making it very fast, faster than any DOM-based approach. Also, ScrapeMark patterns are more expressive and maintainable than DOM-traversal code.


## Module Contents

### `scrapemark.**user_agent`

`"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3"`

## ScrapeMarkPattern Objects

### `ScrapeMarkPattern.scrape(html=None, url=None, get=None, post=None, headers=None, cookie_jar=None)`

Same behavior as `scrapemark.scrape()`


## Pattern Syntax

A pattern contains PLAIN OLD HTML, in addition to some special markup. The HTML in the pattern must match up with the HTML being scraped. This is done in a relaxed fasion:

### Anectors and siblings can be omitted

The pattern `<li><a></a></li>` will match `<li><span><a>some text</a></span></li>`

The pattern `<hr /><p/>` will match `<hr /><input /><p>my paragraph</p>`

### Tag attributes can be omitted or ordered differently (AND quotes...)

The pattern `<a></a>` will match `<a href='page.html'></a>`

The pattern `<input id='email' type='text' />` will match `<input type='text' id='email' />`

### Whitespace and case are relaxed

The pattern `<title>My Site</title>` will match `< TITLE >  MY   SITE </TITLE>`

Newlines, tabs, and spaces are all considered the same

### Text only needs to partially match

The pattern `<a>link</a>` will match `<a>the link name</a>`

The pattern `<div class='red'></div>` will match `<div class='big red juicy'></div>`

However, minimal whitespace must be maintained: `hello friend` will NOT match `hellofriend`

Special markup is used to extract information from the HTML. This special markup can be located in the top level of the pattern, as a child of an HTML tag, or within an HTML attribute.

### `{{ variablename }}`

Captures an area of text, stripping HTML markup. This value gets returned, in some form, when `scrapemark.scrape()` is called and the pattern matches. Can be used within a tag:

```html
<title>{{ pagetitle }}</title>
```

Or within an attribute value:

```html
<div class='person-{{ id }}' />
```

By default, a call to `scrapemark.scrape()` returns a dictionary of all the captured names and values. Optionally, you may use dot-notation to organize your result into nested dictionaries:

```html
<a href='{{ link.url }}'>{{ link.name }}</a>
```

You may also accumulate a list by surrounding a variable name with square brackets. The dictionary resulting from a call to `scrapemark.scrape()` would have the key ‘paragraphs’ pointing to a list of strings:

```html
<p>{{ [paragraphs] }}</p><p>{{ [paragraphs] }}</p>
```

To access your captured values more quickly, if variablename is omitted, the result of `scrapemark.scrape()` will change types:

`<title>{{ }}</title>` — will return a string

`<p>{{ [] }}</p><p>{{ [] }}</p>` — will return a list of strings

### `{* subpattern *}`

Makes subpattern optional and/or repeatable. In effect, subpattern is applied as many times as possible to the enclosing area of HTML. Can be used in tandem with captured lists. Consider the following HTML:

```html
<a href='home.html'>Home</a>
<a href='about.html'>About Us</a>
<a href='blog.html'>Blog</a>
```

The pattern:

```html
{* <a>{{ [linknames] }}</a> *}
```

would yield the python dictionary result:

```py
{'linknames': ['Home', 'About Us', 'Blog']}
```

This can be used in combination with dot-notation. For example, the pattern:

```html
{* <a href='{{ [links].url }}'>{{ [links].title }}</a> *}
```

would yield the python dictionary result:

```py
{'links': [
  {'url': 'home.html', 'title': 'Home'},
  {'url': 'about.html', 'title': 'About Us'},
  {'url': 'blog.html', 'title': 'Blog'}
]}
```

### `{@ subpattern @}`

Temporarily captures an area of text, which is assumed to be a URL. Visits this URL and applies *subpattern* to it. Here is an example pattern:

```html
<a href='{@
  <title>{{ page.title }}</title>
  <body>{{ page.text }}</body>
@}'>{{ page.linktitle }}</a>
```

The URL is always implicitly converted to an absolute URL before the sub-page is requested. The original *cookie_jar* from `scrapemark.scrape()` is used in this request. Be careful about using this technique within repeatable regions!

### `{# comment #}`

Write a comment in your pattern. Nothing is executed.


## Filters

Filters can modify the type and value of captured text. In the case of the `{{ }}` tag, filters take the following form:

```
{{ variablename|filter1|filter2|filter3 }}
```

The value is sequentially processed by all the filters before being returned by `scrapemark.scrape()`. In the case of the `{@ @}` tag, filters take the following form:

```
{@|filter1|filter2|filter3 subpattern @}
```

The filters modify the URL to be used in the request. This is useful if you have a URL as a javascript string and you want to unescape slashes. Here is a list of available filters:

- `unescape` - uses `str.decode('string_escape')` on the input
- `abs` - given a URL, makes it absolute (the `{@ @}` tag already implicitly does this)
- `int`/`float`/`bool` - changes the object’s type using `int()`, `float()`, and `bool()`. Conversion errors are suppressed.
- `html` - prevents the default behavior of HTML markup being stripped from the captured text


## Idiosyncrasies

### Empty Attributes

An empty attribute in a pattern will check for the **existence** of that attribute in the HTML. For example, the following pattern:

```html
<span style='' />
```

would match the HTML:

```html
<span style='color:red'></span>
```

### Adjacent Special Markup

When special markup tags lie next to eachother, both are equally applied to the enclosing area of HTML. In other words, a second special tag does not merely ‘resume’ where a first left off. For example, the following pattern:

```html
<div>
  {* <div class='post'></div> *}
  {* <div class='image'></div> *}
</div>
```

would match *all* the image/post divs in the HTML:

```html
<div>
  <div class='image'>...</div>
  <div class='post'>...</div>
  <div class='image'>...</div>
</div>
```

This is also a convenient way to do two actions at once. For example, the following form would both capture a URL’s text and visit it’s HTML:

```html
<a href='{{ variablename }}{@ subpattern @}'></a>
```

### If `{@ @}` doesn’t match

If the subpattern within a `{@ @}` special tag does not match, the outer pattern fails too. This is protective behavior. Consider the following pattern for fetching and scraping the first link on a page:

```html
<a href='{@ <div id='content'>{{ content }}</div> @}' />
```

Ordinarily, if the format of the subpage was changed and `<div id='content'>` no longer existed, every `<a>` tag would be sequentially visited until a match was found. However, this behavior is short-circuited.
