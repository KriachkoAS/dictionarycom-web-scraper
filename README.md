# dictionary.com ipa scraper
## lil description
__Only American ipa__ is getting. Percentage of ipa scraping and aggregation is around 90, while lvl scraping is around 94 (mostly because of no lvl on the page at all). Supposed that there no incorrect aggregated ipas and lvls.  

Core class is consist of fields: ipa, lvl. Field lvl is object with name, img(shown emoji), img_name,ipa is dictionary with pos (part of speech) as key and ipa html string as value. Converting ipa to aggregated html string is available with ipa_to_str method. Fields lvl and ipa (and most inner object fields) is __NOT EXIST__ if was an error while scraping, it is on purpose and __still None__ if other reasons.  
  
Also possible to use word verification with __word__ and __word_filter__ params, second one is supposed to be func with __word__ and __header_of_pagepart__ params returns True\False depends on accaptability of __header_of_pagepart__ as a __word__.  
## install
`pip install dictionarycom-ipa-scraper` or equivalent.
## use
```python
from dictionarycom-ipa-scraper import scraper
  
#some python code with page_html_as_str declaration
  
scraped = scraper.ParsedCode(page_html_as_str, word)
scraped.ipa_as_str() #html string actually
scraped.lvl.name #lvl of complexity

```