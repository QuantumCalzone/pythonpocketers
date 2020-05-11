from bs4 import BeautifulSoup
from pythonutils.str_utils import *
import pocket_utils
from pocket_utils import *
import requests

pocket_utils.initialize(__file__)
page = 0
URL = "https://www.gamasutra.com/blogs/expert/page={}".format(page)
pocket_utils.debug = True
stop_if_already_pocketed = True
scrape = True

print("")

while scrape:
    page += 1
    URL = "https://www.gamasutra.com/blogs/expert/page={}".format(page)
    print("loading page {}...".format(page))

    r = requests.get(URL)
    if r.status_code is not 200:
        print("Stopped due to status code error 200")
        scrape = False
        break

    soup = BeautifulSoup(r.content, "html.parser")
    blog_entries = soup.findAll("div", {"class": "blogentry"})

    if len(blog_entries) is 0:
        print("Stopped due to no blog entries found!")
        scrape = False
        break

    for blog_entry in blog_entries:
        tags = ["Gamasutra Expert Blog"]
        tags_map = {"Gamasutra Expert Blog": True}

        title_and_link_class = blog_entry.find("div", {"class": "title"})
        title = title_and_link_class.text
        title = title.replace('\r', '').replace('\n', '')
        link = title_and_link_class.find("a")["href"]
        link = "https://www.gamasutra.com" + link

        if stop_if_already_pocketed:
            link_search = get(search=link)
            if len(link_search[0]["list"]) > 0:
                print("You already pocketed {}".format(link))
                print("Stopping scrape...")
                scrape = False
                break

        author_class = blog_entry.find("div", {"class": "author"})

        extra_tags = []
        extra_tags_classes = author_class.findAll("a")

        for extra_tags_class in extra_tags_classes:
            extra_tags.append(extra_tags_class.text)

        for extra_tag in extra_tags:
            extra_tag = extra_tag.title()
            if extra_tag and extra_tag not in tags_map:
                # extra_tag = extra_tag.encode("utf8")
                extra_tag = extra_tag.replace(",", "")
                extra_tag = strip_non_ascii(extra_tag)
                tags.append(extra_tag)
                tags_map[extra_tag] = True

        tags = ",".join(tags)

        save(link, tags)
    soup.decompose()

print("")
