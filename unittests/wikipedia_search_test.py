import wikipedia


hits = wikipedia.search('neutrino')
page = wikipedia.page(hits[0], auto_suggest=False)
print(page.content)
