import json
import re

import requests
from bs4 import BeautifulSoup


def getAuthorProfileData():
    try:
        url = "https://scholar.google.co.in/citations?hl=en&user=dcj-bnsAAAAJ&view_op=list_works&sortby=pubdate&pagesize=80"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        author_results = {"name": soup.select_one("#gsc_prf_in").text}
        author_results["position"] = soup.select_one("#gsc_prf_inw+ .gsc_prf_il").text
        author_results["email"] = soup.select_one("#gsc_prf_ivh").text
        author_results["departments"] = soup.select_one("#gsc_prf_int").text
        for el in soup.select("#gsc_a_b .gsc_a_t"):
            try:
                year = re.findall(r"\d+", el.select_one(".gs_oph").text)[0]
            except Exception:
                year = ""
            article = {
                "title": el.select_one(".gsc_a_at").text,
                "link": "https://scholar.google.com"
                + el.select_one(".gsc_a_at")["href"],
                "authors": el.select_one(".gsc_a_at+ .gs_gray").text,
                "publication": el.select_one(".gs_gray+ .gs_gray").text,
                "year": year,
            }
            # print(el.text)
            articles.append(article)
        for i in range(len(articles)):
            articles[i] = {k: v for k, v in articles[i].items() if v and v != ""}
        cited_by = {"table": [{}]}
        cited_by["table"][0]["citations"] = {
            "all": soup.select_one("tr:nth-child(1) .gsc_rsb_sc1+ .gsc_rsb_std").text
        }
        cited_by["table"][0]["citations"]["since_2017"] = soup.select_one(
            "tr:nth-child(1) .gsc_rsb_std+ .gsc_rsb_std"
        ).text
        cited_by["table"].append({})
        cited_by["table"][1]["h_index"] = {
            "all": soup.select_one("tr:nth-child(2) .gsc_rsb_sc1+ .gsc_rsb_std").text
        }
        cited_by["table"][1]["h_index"]["since_2017"] = soup.select_one(
            "tr:nth-child(2) .gsc_rsb_std+ .gsc_rsb_std"
        ).text
        cited_by["table"].append({})
        cited_by["table"][2]["i_index"] = {
            "all": soup.select_one("tr~ tr+ tr .gsc_rsb_sc1+ .gsc_rsb_std").text
        }
        cited_by["table"][2]["i_index"]["since_2017"] = soup.select_one(
            "tr~ tr+ tr .gsc_rsb_std+ .gsc_rsb_std"
        ).text
        # print(author_results)
        # print(articles)
        # print(cited_by['table'])
        return articles
    except Exception as e:
        print(e)


data = getAuthorProfileData()
with open("../info/data.json", "w") as f:
    json.dump(data, f)
