import os
from bs4 import BeautifulSoup
from project import *

html_1 = """
<ul><li><a href="/wiki/Abelsonite" title="Abelsonite">Abelsonite</a></li>
<li><a href="/wiki/Abenakiite-(Ce)" title="Abenakiite-(Ce)">Abenakiite-(Ce)</a></li>
<li><a href="/wiki/Abernathyite" title="Abernathyite">Abernathyite</a></li>
<li><a href="/wiki/Abhurite" title="Abhurite">Abhurite</a></li>
<li><a href="/wiki/Abramovite" title="Abramovite">Abramovite</a></li>
<li><a href="/wiki/Abswurmbachite" title="Abswurmbachite">Abswurmbachite</a></li>
<li><a href="/wiki/Acanthite" title="Acanthite">Acanthite</a></li>
<li><a href="/wiki/Achavalite" class="mw-redirect" title="Achavalite">Achavalite</a></li>
<li><a href="/wiki/Azurite" title="Azurite">Azurite</a></li></ul></div>
<dl><dd>Varieties that are not valid species:</dd></dl>
<ul><li><a href="/wiki/Adamantine_spar" title="Adamantine spar">Adamantine spar</a> (variety of corundum)</li>
<li><a href="/wiki/Agate" title="Agate">Agate</a> (variety of chalcedony and quartz)</li>
<li><a href="/wiki/Alabaster" title="Alabaster">Alabaster</a> (variety of gypsum)</li>
<li><a href="/wiki/Anyolite" title="Anyolite">Anyolite</a> (metamorphic rock - zoisite, ruby, and hornblende)</li>
<li><a href="/wiki/Beryl#Aquamarine_and_maxixe" title="Beryl">Aquamarine</a> (light blue variety of beryl)</li>
<li><a href="/wiki/Argentite" title="Argentite">Argentite</a> (high temperature form of acanthite)</li>
<li><a href="/wiki/Avalite" class="mw-redirect" title="Avalite">Avalite</a> (chromian variety of illite)</li>
<li><a href="/wiki/Aventurine" title="Aventurine">Aventurine</a> (variety of quartz)</li></ul>
"""

html_2 = """
<table class="infobox"><tbody><tr><th colspan="2" class="infobox-above" style="color:black; background-color: #8BAFDA">Abelsonite</th></tr><tr><td colspan="2" class="infobox-image"><a href="/wiki/File:Abelsonite_-_Green_River_Formation,_Uintah_County,_Utah,_USA.jpg" class="image"><img alt="Abelsonite - Green River Formation, Uintah County, Utah, USA.jpg" src="//upload.wikimedia.org/wikipedia/commons/thumb/0/09/Abelsonite_-_Green_River_Formation%2C_Uintah_County%2C_Utah%2C_USA.jpg/220px-Abelsonite_-_Green_River_Formation%2C_Uintah_County%2C_Utah%2C_USA.jpg" decoding="async" width="220" height="165" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/0/09/Abelsonite_-_Green_River_Formation%2C_Uintah_County%2C_Utah%2C_USA.jpg/330px-Abelsonite_-_Green_River_Formation%2C_Uintah_County%2C_Utah%2C_USA.jpg 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/0/09/Abelsonite_-_Green_River_Formation%2C_Uintah_County%2C_Utah%2C_USA.jpg/440px-Abelsonite_-_Green_River_Formation%2C_Uintah_County%2C_Utah%2C_USA.jpg 2x" data-file-width="600" data-file-height="450" /></a><div class="infobox-caption">Abelsonite from the <a href="/wiki/Green_River_Formation" title="Green River Formation">Green River Formation</a>, Uintah County, Utah, US</div></td></tr><tr><th colspan="2" class="infobox-header" style="color:black; background-color: #8BAFDA">General</th></tr><tr><th scope="row" class="infobox-label">Category</th><td class="infobox-data"><a href="/wiki/Organic_minerals" class="mw-redirect" title="Organic minerals">Organic minerals</a></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Chemical_formula" title="Chemical formula">Formula</a><br /><style data-mw-deduplicate="TemplateStyles:r886047488">.mw-parser-output .nobold{font-weight:normal}</style><span class="nobold">(repeating unit)</span></th><td class="infobox-data">C<sub>31</sub>H<sub>32</sub>N<sub>4</sub>Ni<sup id="cite_ref-handbook_1-0" class="reference"><a href="#cite_note-handbook-1">&#91;1&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/List_of_mineral_symbols" title="List of mineral symbols">IMA symbol</a></th><td class="infobox-data">Abl<sup id="cite_ref-2" class="reference"><a href="#cite_note-2">&#91;2&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Nickel%E2%80%93Strunz_classification" title="Nickel–Strunz classification">Strunz classification</a></th><td class="infobox-data">10.CA.20</td></tr><tr><th scope="row" class="infobox-label">Dana classification</th><td class="infobox-data">50.4.9.1</td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Crystal_system" title="Crystal system">Crystal system</a></th><td class="infobox-data"><a href="/wiki/Triclinic" class="mw-redirect" title="Triclinic">Triclinic</a></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Space_group" title="Space group">Space group</a></th><td class="infobox-data">P<span style="text-decoration:overline;">1</span> (No. 2)<sup id="cite_ref-FOOTNOTEHummerNollHazenDowns20171129–1132_3-0" class="reference"><a href="#cite_note-FOOTNOTEHummerNollHazenDowns20171129–1132-3">&#91;3&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Crystal_structure#Unit_cell" title="Crystal structure">Unit cell</a></th><td class="infobox-data">a = 8.508, b = 11.185 Å<br />c = 7.299&#160;[Å], α = 90.85°<br />β = 114.1°, γ = 79.99° <br />Z&#160;=&#160;1<sup id="cite_ref-handbook_1-1" class="reference"><a href="#cite_note-handbook-1">&#91;1&#93;</a></sup></td></tr><tr><th colspan="2" class="infobox-header" style="color:black; background-color: #8BAFDA">Identification</th></tr><tr><th scope="row" class="infobox-label">Color</th><td class="infobox-data">Pink-purple, dark greyish purple, pale purplish red, reddish brown</td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Cleavage_(crystal)" title="Cleavage (crystal)">Cleavage</a></th><td class="infobox-data">Probable on {11<span style="text-decoration:overline;">1</span>}<sup id="cite_ref-handbook_1-2" class="reference"><a href="#cite_note-handbook-1">&#91;1&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Fracture_(mineralogy)" title="Fracture (mineralogy)">Fracture</a></th><td class="infobox-data">Fragile<sup id="cite_ref-webmin_4-0" class="reference"><a href="#cite_note-webmin-4">&#91;4&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Mohs_scale_of_mineral_hardness" class="mw-redirect" title="Mohs scale of mineral hardness">Mohs scale</a> <link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r886047488"/><span class="nobold">hardness</span></th><td class="infobox-data">2&#8211;3</td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Lustre_(mineralogy)" title="Lustre (mineralogy)">Luster</a></th><td class="infobox-data">Adamantine, sub-metallic</td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Streak_(mineralogy)" title="Streak (mineralogy)">Streak</a></th><td class="infobox-data">Pink</td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Transparency_and_translucency" title="Transparency and translucency">Diaphaneity</a></th><td class="infobox-data">Semitransparent<sup id="cite_ref-handbook_1-5" class="reference"><a href="#cite_note-handbook-1">&#91;1&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Specific_gravity" class="mw-redirect" title="Specific gravity">Specific gravity</a></th><td class="infobox-data">1.45</td></tr><tr><th scope="row" class="infobox-label">Optical properties</th><td class="infobox-data">Biaxial<sup id="cite_ref-handbook_1-3" class="reference"><a href="#cite_note-handbook-1">&#91;1&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Ultraviolet" title="Ultraviolet">Ultraviolet</a> <a href="/wiki/Fluorescence" title="Fluorescence">fluorescence</a></th><td class="infobox-data">Non-fluorescent<sup id="cite_ref-webmin_4-1" class="reference"><a href="#cite_note-webmin-4">&#91;4&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label"><a href="/wiki/Absorption_spectroscopy" title="Absorption spectroscopy">Absorption spectra</a></th><td class="infobox-data">Strong reddish brown to reddish black<sup id="cite_ref-handbook_1-4" class="reference"><a href="#cite_note-handbook-1">&#91;1&#93;</a></sup></td></tr><tr><th scope="row" class="infobox-label">References</th><td class="infobox-data"><sup id="cite_ref-mindat_5-0" class="reference"><a href="#cite_note-mindat-5">&#91;5&#93;</a></sup></td></tr></tbody></table>
"""

# Test processing of start url

soup = BeautifulSoup(html_1, 'html.parser')
uls = soup.find_all("ul")

def test_are_varieties():
    assert are_varieties(uls[0]) == False
    assert are_varieties(uls[1]) == True

def test_extract_minerals():
    minerals = extract_minerals(uls[0])
    assert minerals[0] == "https://en.wikipedia.org/wiki/Abelsonite"


def test_extract_varieties():
    varieties = extract_varieties(uls[1])
    assert varieties[0]['name'] == 'Adamantine spar'
    assert varieties[0]['url'] == 'https://en.wikipedia.org/wiki/Adamantine_spar'

# Test processing of mineral

url = os.path.join(os.path.dirname(__file__), "andradite.html")


with open(url, "r") as f:
    soup = BeautifulSoup(f, 'html.parser')


def test_get_chemistry_html():
    infobox = soup.find("table", class_="infobox")
    assert get_chemistry_html(infobox) == "Ca<sub>3</sub>Fe<sub>2</sub>(SiO<sub>4</sub>)<sub>3</sub>"


def test_varieties_from_box():
    infobox = soup.find("table", class_="infobox")
    v = varieties_from_box(infobox)
    assert v[0]['name'] == "Demantoid"

def test_friendlystring():
    infobox = soup.find("table", class_="infobox")
    v = varieties_from_box(infobox)
    assert friendlystring(v) == "Demantoid (transparent light to dark green to yellow-green), Melanite (opaque black), Topazolite (None)"


def test_mineral_data():
    m = mineral_data(soup)
    assert m['name'] == "Andradite"
    assert m['chemistry html'] == "Ca<sub>3</sub>Fe<sub>2</sub>(SiO<sub>4</sub>)<sub>3</sub>"
    assert m['Strunz class'] == "9.AD.25"
    assert m['varieties'][0]['name'] == "Demantoid"
    assert m['IMA Symbol'] == 'Adr'

def test_removal_of_footnotes():
    soup = BeautifulSoup(html_2, 'html.parser')
    assert get_infobox_value(soup.find(string="IMA symbol")) == 'Abl'
    assert get_chemistry_html(soup) == 'C<sub>31</sub>H<sub>32</sub>N<sub>4</sub>Ni'