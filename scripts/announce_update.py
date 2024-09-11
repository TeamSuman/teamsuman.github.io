import json
news = json.load(open("./info/news.json"))

template = open("./templates/index_template.html", "r").readlines()
header = template[:235]
tailed = template[235:]

def news_format(title, category, content, link, message=None):

    if category=="info":
        return f"""<div class="notification mb-2">
                    <div class="notiglow"></div>
                    <div class="notiborderglow"></div>
                    <div class="notititle">{title}</div>
                    <div class="notibody">{content}</div>
                    <div class="notibody"><p><span style="color:green; font-weight:bold;">{message}</span></p></div>
                </div>"""
    else:
        return f"""<div class="notification mb-2">
                    <div class="notiglow"></div>
                    <div class="notiborderglow"></div>
                    <div class="notititle">{title}</div>
                    <div class="notibody">{content}<a class="link" href="{link}">  Know more!</a></div>
                </div>"""
    
starter = """    <div class="container-fluid packages">
        <div class="container py-5">
            <div class="mx-auto text-center mb-5" style="max-width: 900px;">
                <h5 class="section-title px-3">Announcements</h5>
            </div>
            <div class="packages-carousel owl-carousel">"""
ender = """</div>
        </div>
    </div>"""

my_announcements = "".join(
    news_format(
        news_item["title"],
        news_item["category"],
        news_item["content"],
        news_item["link"] if 'link' in news_item else None,
        news_item['message'] if 'message' in news_item else None
    )
    for news_item in news
)
with open('index.html', 'w') as f:
    f.write(''.join(header))
    f.write(starter)
    f.write(my_announcements)
    f.write(ender)
    f.write(''.join(tailed))