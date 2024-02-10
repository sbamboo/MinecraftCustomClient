from flavorFunctions import scrapeMinorVerLinks,scrapeUniversals,_joinForgeListings,_removeAdFocLinkPrefixDict

import requests

prefix = "> "
forgeUrl = "https://files.minecraftforge.net/net/minecraftforge/forge"

stdlist = {}

webcontent = requests.get(forgeUrl).text
scrapedPages = scrapeMinorVerLinks(webcontent,forgeUrl)

universals = scrapeUniversals(prefix,scrapedPages)

if universals != None and universals != {}:
    frgListings = _joinForgeListings(stdlist,universals)
    print( _removeAdFocLinkPrefixDict(frgListings) ) 