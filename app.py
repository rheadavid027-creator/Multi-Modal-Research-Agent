from tools import web_search , scrape_url

res = web_search.invoke("what do you mean by riya")

urls = [line.replace("URL: ", "").strip() 
        for line in res.split("\n") 
        if line.startswith("URL:")]

scraped_data = []

for url in urls:
    scraped_data.append(scrape_url.invoke(url))

# print(res)
print(scraped_data)
