from django.conf import settings
from django.core.urlresolvers import get_mod_func
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

def code_highlighter(content):
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import LEXERS, get_lexer_by_name
    from BeautifulSoup import BeautifulSoup

    # a tuple of known lexer names
    _lexer_names = reduce(lambda a,b: a + b[2], LEXERS.itervalues(), ())

    # default formatter
    _formatter = HtmlFormatter(cssclass='codehighlight')
    soup = BeautifulSoup(content)
    for tag in soup.findAll('pre'):
        lexer_name = tag.get('class')
        if lexer_name and lexer_name in _lexer_names:
            lexer = get_lexer_by_name(lexer_name, stripnl=True, encoding='UTF-8')
            tag.replaceWith(highlight(tag.renderContents(), lexer, _formatter))
    
    return force_unicode(soup)

def simple_replace(content):
    from BeautifulSoup import BeautifulSoup
    soup=BeautifulSoup(content)
    for rep in settings.MARKUP_SIMPLE_REPLACE:
        for tag in soup.findAll(rep['element']):
            if tag.get('class') == rep['klass']:
                tag.replaceWith(rep['replace_with'] % { 'content' : tag.renderContents()})
    return unicode(soup)

def markup_chain(content):
    for filter in settings.MARKUP_CHAIN:
        mod_name, func_name = get_mod_func(filter)
        filter_func = getattr(__import__(mod_name, {}, {}, ['']), func_name)
        content = filter_func(content)
    return content

