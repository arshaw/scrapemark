import re
from pygments.lexer import Lexer, DelegatingLexer, RegexLexer, bygroups, \
     include, using, this
from pygments.token import Error, Punctuation, \
     Text, Comment, Operator, Keyword, Name, String, Number, Other, Token

class ScrapeMarkLexer(RegexLexer):

    name = 'ScrapeMark'
    aliases = ['scrapemark']
    flags = re.M | re.S
    tokens = {
        'root': [
            (r'[^{*@]+', Other),
            (r'\{\{', Comment.Preproc, 'var'),
            (r'\{\*', Comment.Preproc),
            (r'\{\@', Comment.Preproc, 'gotofilters'),
            (r'[*@]\}', Comment.Preproc),
            (r'[{*@]', Other)
        ],
        'var': [
            (r'\s+', Text),
            (r'\}\}', Comment.Preproc, '#pop'),
            include('varnames')
        ],
        'varnames': [
            (r'(\|)(\s*)([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Operator, Text, Name.Function)),
            (r'[a-zA-Z][a-zA-Z0-9_]*', Name.Variable),
            (r'\.[a-zA-Z0-9_]+', Name.Variable),
            (r'([{}()\[\]+\-*/,:]|[><=]=?)', Operator)
        ],
        'gotofilters': [
        	(r'(\|)(\s*)([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Operator, Text, Name.Function)),
        	(r'\s+', Text, '#pop'),
        ]
    }
        
