# Web Scraping Mineral Data from Wikipedia (CS50P Final Project)
In my final project of the [CS50’s Introduction to Programming with Python](https://www.edx.org/course/cs50s-introduction-to-programming-with-python) online course from Harvard / edx, I am scraping mineral data from [Wikipedia](https://en.wikipedia.org/wiki/Main_Page) using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#), [requests](https://pypi.org/project/requests/) and regular expressions.


## Motivation
I wanted a list with mineral data including chemistry and Strunz class that can be used with a free license. I couldn't find anything like that on the web.

## Description
The script crawls the links in [https://en.wikipedia.org/wiki/List_of_minerals](https://en.wikipedia.org/wiki/List_of_minerals) and collects the following data (as long it can find it), cleans it and saves it to `minerals.csv`:

- name (title on Wikipedia)
- url (on Wikipedia)
- category
- chemistry as plain text
- chemistry as html
- IMA Symbol
- Strunz class
- crystal system
- crystal class (as text, point group, H-M symbol, respectively)
- color
- cleavage
- Mohs scale
- streak
- Specific gravity
- luster
- habit
- varieties
- summary (first paragraph on Wikipedia)

The second output file `varieties.csv` contains the basic info about varieties found on the list of minerals.

## Data cleaning
The script cleans the data slightly:
- Remove footnotes
- Remove linebreaks
- Remove links, any `<style>` and `<span>` tags and any attributes `class="foo"` and `style="bar"` in the "chemistry html" field
- Remove `{\displaystyle ... }` from alt attribute of img
- If "crystal class" data was within "crystal system" (i.e. not in a seperate table cell), move it to "crystal class".
- Move point group symbol / H-M symbol from "crystal class" into separate columns. On Wikipedia, this is usually in the form of "Prismatic (2/m)" or "4/mmm - Ditetragonal dipyramidal". I don't catch deviations.
- On Wikipedia, Strunz class may contain extra info such as "9.DG.05 (10 ed) 8/F.18.40 (8 ed)". Only return valid Strunz classes, using the latest edition.


## Limitations
- For most data the script relies on the existance of an info-box: On Wikipedia sites without info-box, most data fields will be empty.
- Sometimes wikipedia uses svg images for formulas or crystal class, the script only gets the alt attribute of the img and that might be useless and broken.
- Fields with numbers may be cluttered with additional text and can't be simply converted to int. Examples: Mohs scale of "2 - 3 - Gypsum-Calcite" or "3+1⁄2", gravity of "3.859 calculated; 3.8–3.9 measured".
- Beware of "cubic or tetragonal" etc. in crystal class. 
- Messy data: Crystal class may be "Ditetragonal dipyramidal 4/mmm (4/m 2/m 2/m) -" or "Unknown space group" or even "aluminium arsenite".
- Major changes on Wikipedia might break the script.


## Result
A version of the resulting [minerals.csv](https://raw.githubusercontent.com/florianneukirchen/scrape_mineral_data/main/minerals.csv) is included in the repository. Feel free to use it under the terms of [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License), Data © Wikipedia editors and contributors.
## Requirements
- BeautifulSoup
- requests


## Usage
Run in the terminal:
```
python project.py
```
### Unit tests
For unit tests, run:
```
pytest test.project.py
```
Note that the file andradite.html is used by the tests.

## License
The source code is under [MIT license](https://github.com/florianneukirchen/scrape_mineral_data/blob/main/LICENSE), the scraped data is © Wikipedia editors and contributors, [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License).

## Functions

### main()
Parses Wikipedias List of Minerals with BeautifulSoup, calls extract_minerals() or extract_varieties() to extract links, calls get_mineral() on each mineral link and saves results to CSV.

### are_varieties(ul)
Helper function to be used on Wikipedias List of Minerals to decide whether extract_minerals() or extract_varieties() should be called.

Returns True if the ul is preceded by dl tag. On the wikipedia list of minerals, the lists of varietes are preceded by:
```html
<dl><dd>Varieties that are not valid species:</dd></dl>
```
### extract_minerals(ul)
Extract all links to mineral wikipedia sites from an html `<ul>` list and returns them as a python list.

### extract_varieties(ul)
Extract varieties data from Wikipedias list of minerals.

### get_mineral(url)
Get html with request, parse it with BeautifulSoup, process it by calling mineral_data() and return mineral as dict.

### mineral_data()
Get the data from the html of a Wikipedia mineral site; notably from the info box with a call to get_infobox_value(). Also clean the data.

### get_infobox_value()
Takes a html tag such as `<th>`, searches for the corresponding `<td>` tag and returns the value within this tag.

### varieties_from_box()
Get varieties from infobox, return list.

### get_chemistry_html()
Get cleaned version of the chemistry as HTML.

### helper_html()
Helper function used by get_chemistry_html().

Return empty string if tag has `class="reference"`, return text of `<a>`, else decode tag and return result.

### get_summary()
Return cleaned version of first paragraph of the Wikipedia article.

### friendlystring()
Take list of dictionaries and turn it into a string that can be used in CSV files. Used for varieties.
