MulTithreaded SCRAPER
===================

Hello, welcome you here. This is the mt_scraper library documentation for python version 3.

Description
--------

This is a project of a multithreaded site scraper. Multithreading operation speeds up data collection from Web several times (more than 10 on a normal old work laptop). To use it, you need to redefine the parse method for your needs and enjoy the benefits of multithreading (with all its implementation in Python)

Collecting data in the JSON file, which stores a list of objects (dictionaries) with the collected data.

Application
----------

### Simple application

#### Main Library Usage Scenario

```
import mt_scraper

scraper = mt_scraper.Scraper ()
scraper.run ()
```

As you can see there are only three lines of code

#### What happens when this happens

With this application, you get a data scraper from the pages of the list:
```
url_components_list = [
    'http://example.com/',
    'http://scraper.iamengineer.ru',
    'http://scraper.iamengineer.ru/bad-file.php',
    'http://badlink-for-scarper.ru',
]
```
The last two pages were added to demonstrate the two most common errors when retrieving data from the Internet, these are HTTP 404 - Not Found, and the URL Error: Name: or service not known.

The real URL is obtained by substituting this list into a template:
```
url_template = '{}'
```
Data is accumulated in the file:
```
out_filename = 'out.json'
```
The work is conducted in 5 threads and a task queue of 5 units is created (this has a value, for example, when canceling an operation from the keyboard, the queue length indicates how many tasks were sent for execution):
```
threads_num = 5
queue_len = 5
```
The following is used as a parser function:
```
def parse (self, num, url_component, html):
    '''You must override this method.
    Must return a dictionary or None if parsing the page
    impossible
    '''
    parser = MyDummyHTMLParser ()
    parser.feed (html)
    obj = parser.obj
    obj ['url_component'] = url_component
    return parser.obj
```
DummyParser is a simple version of HTML parser, it is remarkable only because it uses only one standard library and does not require any additional modules.
File dummy_parser.py:
```
from html.parser import HTMLParser

class MyDummyHTMLParser (HTMLParser):
    def __init __ (self):
        super () .__ init __ ()
        self.a_tag = False
        self.h1_tag = False
        self.p_tag = False
        self.obj = {}

    def handle_starttag (self, tag, attrs):
        if tag == 'h1':
            self.h1_tag = True
        elif tag == 'p':
            self.p_tag = True
        elif tag == 'a':
            self.a_tag = True
            for (attr, value,) in attrs:
                if attr == 'href':
                    self.obj ['link'] = value

    def handle_endtag (self, tag):
        if tag == 'h1':
            self.h1_tag = False
        elif tag == 'p':
            self.p_tag = False
        elif tag == 'a':
            self.a_tag = False

    def handle_data (self, data):
        if self.h1_tag:
            self.obj ['header'] = data
        elif self.p_tag and not self.a_tag:
            self.obj ['article'] = data
```
This approach is used only to demonstrate the capabilities of multithreading, in real projects it is recommended to use the lxml or BS libraries, a more advanced application will be shown below in the section "Advanced Application"

