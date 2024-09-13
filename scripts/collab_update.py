import json

def add_collab(name, desig, univ,  img):

    return f"""            <div class="testimonial-item text-center rounded pb-4">
                <div class="testimonial-comment rounded p-5">
                </div>
                <div class="testimonial-img p-1">
                    <img src="{img}" class="img-fluid rounded-circle" alt="{name}">
                </div>
                <div style="margin-top: -35px;">
                    <h5 class="mb-0">{name}</h5>
                    <p class="mb-0">{desig}
                        <br> {univ}
                    </p>
                </div>
            </div>"""
                

def return_head_tail():

    section_head = """<div class="container-fluid testimonial py-5">
    <div class="container py-5">
        <div class="mx-auto text-center mb-5" style="max-width: 900px;">
            <h5 class="section-title px-3">Colaborators</h5>
            <h1 class="mb-0">National/international colaborators</h1>
        </div>
        <div class="testimonial-carousel owl-carousel">"""

    section_tail = """</div></div></div>"""
    return section_head, section_tail

infos = json.load(open('./info/colab.json'))
template = open('./index.html').readlines()

for i, line in enumerate(template):
    if "<!-- Collaborator Start -->" in line:
        header = template[:i+1]
        tail = template[i+2:]
full_html = "" + ''.join(header)
for item in infos:
    head = ""

    section_head, section_tail = return_head_tail()
    head += section_head
    for mem in infos[item]:
        head += add_collab(mem['name'], mem['desig'], mem['univ'], mem['img'])
    head += section_tail

full_html += head
full_html += ''.join(tail)

with open('index.html', 'w') as f:
    f.write(full_html)