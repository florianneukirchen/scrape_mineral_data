import requests
import re
import csv
import time
import os
from bs4 import BeautifulSoup, Tag


# Use Wikipedias List of all minerals as starting point
START_URL = "https://en.wikipedia.org/wiki/List_of_minerals"
BASE_URL = "https://en.wikipedia.org"
OUTFILE = "minerals.csv"

# Item in the last list to break the loop
FINAL = "Zinalsite"


def main():
    if os.path.exists(OUTFILE):
        yn = input("Do you want to overwrite existing file [y|n]? ")
        if not yn == "y":
            os.exit()

    html = requests.get(START_URL)
    soup = BeautifulSoup(html.text, "html.parser")

    # Get all <ul> tags, but skip the first 2 because
    # they only contain site navigation

    uls = soup.find_all("ul")[2:]

    # Now we have different ul lists:
    # - those with links to minerals,
    # - those with varieties
    # - Extras such as "See also" and wikipedia navigation after "Z"

    varieties = []
    minerals = []

    for ul in uls:
        if are_varieties(ul):
            varieties.extend(extract_varieties(ul))
        else:
            minerals.extend(extract_minerals(ul))

        if ul.find(text=FINAL):
            # This was the last list we are interested in
            break
    # Write varieties to CSV
    fieldnames = ["name", "url", "description"]
    with open("varieties.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for v in varieties:
            writer.writerow(v)

    # Scrape mineral data and save it to CSV
    fieldnames = [
        "name",
        "url",
        "category",
        "chemistry",
        "chemistry html",
        "IMA Symbol",
        "Strunz class",
        "crystal system",
        "crystal class",
        "crystal class symbol",
        "H-M symbol",
        "color",
        "cleavage",
        "mohs",
        "streak",
        "gravity",
        "luster",
        "habit",
        "varieties",
        "summary",
    ]
    with open(OUTFILE, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for url in minerals:
            print("Fetch", url)
            min = get_mineral(url)

            # Replace varieties dictionary with a CSV friendly string
            if "varieties" in min:
                min["varieties"] = friendlystring(min["varieties"])

            # Make sure all fieldnames exist as keys
            for fn in fieldnames:
                if not fn in min:
                    min[fn] = ""

            writer.writerow(min)

            # Be nice and sleep 0.5 seconds
            time.sleep(0.5)


def are_varieties(ul):
    """
    Return True if the ul is preceded by dl tag.

    On the wikipedia list of minerals, the lists
    of varietes are preceded by:
    <dl><dd>Varieties that are not valid species:</dd></dl>
    However the previous sibling is '\n', we need to go back
    two steps.

    The previous of the previous sibling might be None and
    None.name would raise an AttributeError.
    """

    try:
        return ul.previous_sibling.previous_sibling.name == "dl"
    except AttributeError:
        return False


def extract_minerals(ul):
    """
    Extract links to mineral wikipedia sites from an <ul> list
    and return a python list.
    """

    urls = []

    for link in ul.find_all("a"):
        url = BASE_URL + link["href"]
        urls.append(url)

    return urls


def extract_varieties(ul):
    """Extract varieties data from the start url"""
    varieties = []
    for li in ul.find_all("li"):
        variety = {}
        variety["name"] = li.a["title"]
        variety["url"] = BASE_URL + li.a["href"]
        # li.text includes the text in the link, get rid of this and of the ( )
        variety["description"] = li.text
        varieties.append(variety)
    return varieties


def get_mineral(url):
    """Get html, process it and return mineral"""
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    mineral = mineral_data(soup)
    mineral["url"] = url

    return mineral


def mineral_data(soup):
    """Get mineral data from soup"""
    mineral = {}
    mineral["name"] = soup.find(id="firstHeading").text
    mineral["summary"] = get_summary(soup)

    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return mineral

    mineral["category"] = get_infobox_value(infobox.find(string="Category"))
    mineral["chemistry"] = get_infobox_value(infobox.find(string="Formula"))
    mineral["chemistry html"] = get_chemistry_html(infobox)
    mineral["IMA Symbol"] = get_infobox_value(infobox.find(string="IMA symbol"))
    mineral["Strunz class"] = get_infobox_value(
        infobox.find(string=re.compile("Strunz"))
    )
    mineral["crystal system"] = get_infobox_value(infobox.find(string="Crystal system"))
    mineral["crystal class"] = get_infobox_value(infobox.find(string="Crystal class"))
    mineral["color"] = get_infobox_value(infobox.find(string="Color"))
    mineral["cleavage"] = get_infobox_value(infobox.find(string="Cleavage"))
    mineral["mohs"] = get_infobox_value(infobox.find(string=re.compile("Mohs")))
    mineral["streak"] = get_infobox_value(infobox.find(string=re.compile("Streak")))
    mineral["gravity"] = get_infobox_value(infobox.find(string="Specific gravity"))
    mineral["luster"] = get_infobox_value(infobox.find(string="Luster"))
    mineral["habit"] = get_infobox_value(infobox.find(string="Crystal habit"))
    mineral["varieties"] = varieties_from_box(infobox)

    # Crystal system should be only one word, not "Orthorhombic Dipyramidal class" or "Triclinic Unknown space group"
    if len(mineral["crystal system"].split()) > 1:
        if mineral["crystal class"] == "":
            mineral["crystal class"] = mineral["crystal system"].split(" ", 1)[1]
            mineral["crystal class"] = re.sub(r" ?class", "", mineral["crystal class"])
        mineral["crystal system"] = mineral["crystal system"].split()[0]

    # Clean Strunz class
    if len(mineral["Strunz class"].split()) > 1:
        mineral["Strunz class"] = mineral["Strunz class"].split()[0]
    mineral["Strunz class"] = re.sub(r"\(.*\)", "", mineral["Strunz class"])

    # Move H-M symbol from crystal class into its own column
    mineral['H-M symbol'] = ""
    matches1 = re.search(r" ?\(same H[–-]M [Ss]ymbol\)", mineral['crystal class'])
    matches2 = re.search(r"^(.*) ?H[–-]M [Ss]ymbol:? ?(.*)$", mineral['crystal class'])
    if matches1:
        mineral['crystal class'] = re.sub(r" ?\(same H[–-]M [Ss]ymbol\)", "", mineral['crystal class']).strip()
        matches3 = re.search(r"(\(.*\))", mineral['crystal class'])
        if matches3:
            mineral['H-M symbol'] = matches3.group(1).strip()
        else:
            mineral['H-M symbol'] = mineral['crystal class']
    elif matches2:
        mineral['crystal class'] = matches2.group(1).strip()
        mineral['H-M symbol'] = matches2.group(2).strip()

    mineral['H-M symbol'] = mineral['H-M symbol'].lstrip("(").rstrip(")")

    # Separate crystal class and symbol
    # It is usually in the form "Prismatic (2/m)" or "4/mmm - Ditetragonal dipyramidal"
    # But may be "3m" or "Unkown space group"
    mineral['crystal class symbol'] = ""
    matches1 = re.search(r"^([A-Za-z ]*) \(([1-9/m ]*)\)$", mineral['crystal class'])
    matches2 = re.search(r"^([1-9/m ]*) [-–] ([A-Za-z ])$", mineral['crystal class'])
    if matches1:
        mineral['crystal class symbol'] = matches1.group(2).strip()
        mineral['crystal class'] = matches1.group(1).strip()
    elif matches2:
        mineral['crystal class symbol'] = matches1.group(1).strip()
        mineral['crystal class'] = matches1.group(2).strip()
    else:
        matches3 = re.search(r"^[1-9/m ]$", mineral['crystal class'])
        if matches3:
            mineral['crystal class symbol'] = mineral['crystal class']
            mineral['crystal class'] = ""

    return mineral


def get_infobox_value(tag):
    """
    Takes a html tag such as <th>, searches for the corresponding <td> tag
    and returns the value within this tag.
    """
    if not tag:
        return ""
    else:
        s = tag.parent.find_next("td").text
        # Remove footnotes such as in 'Adr[1]'
        s = re.sub(r"\[[0-9]]*\]", "", s)
        # Remove {\displaystyle ... }
        s = re.sub(r"\{displaystyle.*\}", "", s)
        # Remove newline
        s = re.sub(r"\n", "", s)
        return s


def varieties_from_box(infobox):
    """Get varieties from infobox, return list."""
    varieties = []
    tag = infobox.find(string=re.compile("[v|V]arieties"))
    if not tag:
        return []
    tag = tag.parent
    if tag.name == "td":
        return []
    while True:
        tag = tag.find_next("th")
        if not tag:
            break
        if not "class" in tag.attrs:
            break
        if not "infobox-label" in tag["class"]:
            break
        description = tag.find_next("td").string
        varieties.append({"name": tag.string, "description": description})

    return varieties


def get_chemistry_html(infobox):
    """Get cleaned version of the chemistry as HTML"""
    tag = infobox.find(string="Formula")
    if not tag:
        return ""
    tag = tag.parent.find_next("td")
    contents = tag.contents

    # Get rid of <span> tags
    for c in contents:
        if c.name == "span":
            contents = c.contents
            break

    s = "".join([helper_html(i) if type(i) is Tag else i for i in contents])
    # remove class and style attributes
    s = re.sub(r' ?class=".*"', '', s)
    s = re.sub(r' ?style=".*"', '', s)
    s = s.replace(" ", "")
    return s


def helper_html(tag):
    """Return empty string if tag has class="reference", return text of a, else decode tag"""
    if tag.name == "a":
        return tag.text

    try:
        if "reference" in tag["class"]:
            return ""
    except KeyError:
        pass

    return tag.decode()


def get_summary(soup):
    """Return cleaned version of first paragraph"""
    p = soup.p.text.strip()
    # Remove footnotes
    p = re.sub(r"\[[0-9]]*\]", "", p)
    # Remove {\displaystyle ... }
    p = re.sub(r"\{displaystyle.*\}", "", p)
    # Remove newline
    p = re.sub(r"\n", "", p)
    return p


def friendlystring(varieties):
    """
    Take list of dictionaries and turn it into a string
    that can be used in CSV files
    """

    varieties = [f"{v['name']} ({v['description']})" for v in varieties]
    return ", ".join(varieties)


if __name__ == "__main__":
    main()
