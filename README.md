
**NOTE**: This project is no longer maintained! [more info](http://blog.arshaw.com/1/post/2013/03/reflecting-on-scrapemark.html)

# Scrapemark

Scrapemark is a super-convenient way to [scrape webpages](http://en.wikipedia.org/wiki/Web_scraping) in Python.

It utilizes an HTML-like markup language to extract the data you need. You get your results as plain old Python lists and dictionaries. Scrapemark internally utilizes [regular expressions](http://en.wikipedia.org/wiki/Regular_expression) and is super-fast.

As an example, here is a way you could scrape all the links on the Digg homepage in one fell swoop:

```py
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
```

- [See more examples &raquo;](EXAMPLES.md)
- [View the documentation &raquo;](DOCS.md)
- [Download &raquo;](https://github.com/arshaw/scrapemark/releases)
