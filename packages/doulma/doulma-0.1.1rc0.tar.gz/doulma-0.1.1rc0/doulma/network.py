import aiohttp
from requests.compat import quote
from bs4 import BeautifulSoup


async def search_wikipedia(query: str, session: aiohttp.ClientSession) -> dict:
    """
    search_wikipedia
    ~~~~~~~~~~~~~~~~

    Async Function to look up a Wikipedia Article

    :param query: Query to search
    :param session: Your aiohttp.ClientSession()
    :return: A Dictionary containing retrieved Information
    """
    async with session.get(
            f"https://en.wikipedia.org/w/index.php?search={quote(query.title())}"
            "&title=Special:Search&fulltext=Search") as search_response:
        search_response = await search_response.text()

    search_soup = BeautifulSoup(search_response, 'html.parser')

    try:
        obj1 = search_soup.find('ul', class_="mw-search-results").contents[0].contents[0].contents[0]
        obj2 = search_soup.find('ul', class_="mw-search-results").contents[1].contents[0].contents[0]
    except AttributeError:
        return {"title": "Nothing", "description": "Can't find Anything", "image": "img", "found": False,
                "url": f"https://en.wikipedia.org/wiki/Potato"}

    search_results = [
        ["https://en.wikipedia.org" + obj1.get('href'), obj1.get('title')],
        ["https://en.wikipedia.org" + obj2.get('href'), obj2.get('title')]
    ]

    chosen_result = search_results[0]

    # Second Part

    paragraphs = []

    async with session.get(
            f"https://en.wikipedia.org/w/index.php?title={quote(chosen_result[1])}"
            "&printable=yes#bodyContent") as response:
        response = await response.text()

    soup = BeautifulSoup(response, 'html.parser')

    try:
        img = "https:" + soup.find(name="a", class_="image").contents[0].get('src')
    except AttributeError:
        img = "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/" \
              "Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png"

    if img == 'https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Disambig_gray.svg/30px-Disambig_gray.svg.png':
        chosen_result = search_results[1]

        async with session.get(
                f"https://en.wikipedia.org/w/index.php?title={quote(chosen_result[1])}&printable=yes#bodyContent"
        ) as response:
            response = await response.text()

        soup = BeautifulSoup(response, 'html.parser')

    if soup.find(name="div", class_="mw-parser-output") is None:
        return {"title": "Nothing", "description": "Can't find Anything", "image": "img", "found": False,
                "url": f"https://en.wikipedia.org/wiki/Potato"}

    for child in soup.find(name="div", class_="mw-parser-output").contents:
        if child.name == "p":
            nice_list = []
            for a_string in child.strings:
                nice_list.append(a_string)

            if ''.join(nice_list).strip() == "":
                pass

            if len(''.join(nice_list).strip()) <= 2:
                pass

            else:
                paragraphs.append(child)
        else:
            pass

    names = []

    for name in paragraphs[0].strings:
        names.append(name)

    uhm_just_footer = []
    for footer_thing in soup.find(name="li", attrs={'id': 'footer-info-lastmod'}).strings:
        uhm_just_footer.append(footer_thing)

    try:
        img = "https:" + soup.find(name="a", class_="image").contents[0].get('src')
    except AttributeError:
        img = "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/" \
              "Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png"

    return {"title": chosen_result[1], "description": ''.join(names), "image": img, "found": True,
            "url": f"https://en.wikipedia.org/wiki/{quote(chosen_result[1])}",
            "updated_at": ''.join(uhm_just_footer).strip().replace('\xa0', '')}


async def search_urban(query: str, session: aiohttp.ClientSession):
    """
    search_urban
    ~~~~~~~~~~~~

    Async Function to retrieve a certain Definition from Urban Dictionary

    :param query: Query to look up in UrbanDictionary
    :param session: Your aiohttp.ClientSession()
    :return: A Dictionary containing the Definition
    """
    async with session.get(f"https://www.urbandictionary.com/define.php?term={quote(query)}") as response:
        html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    try:
        definition = soup.find(name='div', class_="def-panel")

        result = {
            "word": definition.contents[1].contents[0].string.strip(),
            "url": "https://www.urbandictionary.com" + definition.contents[1].contents[0]['href'],
            'definition': definition.contents[2].text.replace('\r', '\n').strip(),
            'example': definition.contents[3].text.replace('\r', '\n').strip(),
            'footer': definition.contents[4].text.strip(),
            'upvotes': definition.contents[5].contents[0].contents[0].contents[0].contents[0].contents[
                0].text.strip(),
            'downvotes': definition.contents[5].contents[0].contents[0].contents[0].contents[0].contents[
                1].text.strip(),
            'found': True
        }

    except:
        result = {'found': False}

    return result
