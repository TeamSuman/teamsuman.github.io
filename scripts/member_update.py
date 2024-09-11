import numpy as np
import json
def add_mem(name, desig, sub, img, mail, tw, fb, linkedin, style = 1, interest = ""):
    """
        This function generates a formatted HTML snippet for a team member's card.

      Parameters:
      name (str): The name of the team member.
      desig (str): The designation of the team member.
      img (str): The URL of the team member's image.
      mail (str): The URL of the team member's Facebook profile.
      tw (str): The URL of the team member's Twitter profile.
      insta (str): The URL of the team member's Instagram profile.
      linkedin (str): The URL of the team member's LinkedIn profile.
      Returns:
      str: A formatted HTML snippet for the team member's card.
      """
    if style == 1:
        return f"""                <div class="col-md-6 col-lg-3">
                    <div class="guide-item">
                        <div class="guide-img">
                            <div class="guide-img-efects">
                                <img src="{img}" class="img-fluid w-100 rounded-top" alt="Image">
                            </div>
                            <div class="guide-icon rounded-pill p-2">
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="mailto:{mail}"><i
                                        class="fa fa-envelope"></i></a>
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="{tw}"><i
                                        class="fab fa-twitter"></i></a>
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="{fb}"><i
                                        class="fab fa-facebook"></i></a>
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="{linkedin}"><i
                                        class="fab fa-linkedin-in"></i></a>
                            </div>
                        </div>
                        <div class="guide-title text-center rounded-bottom p-4">
                            <div class="guide-title-inner" style="margin-top:10px;">
                            <p class="mb-0">{desig}</p>
                            <h4 class="mt-0">{name}</h4>
                            <p class="mb-0">{interest}</p>
                            </div>
                        </div>
                    </div>
                </div>"""
    else:
        return f"""                    <div class="col-lg-4 col-md-6">
                        <div class="blog-item">
                            <div class="blog-img">
                                <div class="blog-img-inner">
                                    <img class="img-fluid w-100 rounded-top" src="{img}" alt="Image">
                                </div>
                            </div>
                            <div class="blog-content border border-top-0 rounded-bottom p-4">
                                <p class="mb-3">{desig}/{sub}</p>
                                <a href="#" class="h4">{name}</a>
                                <p class="my-3">{interest}</p>
                                <div class="guide-icon rounded-pill p-2" style="display: flex; margin: auto; text-align: center; justify-content: center;">
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="mailto:{mail}"><i
                                        class="fa fa-envelope"></i></a>
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="{fb}"><i
                                        class="fab fa-facebook-f"></i></a>
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="{tw}"><i
                                        class="fab fa-twitter"></i></a>
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="{linkedin}"><i
                                        class="fab fa-linkedin-in"></i></a>
                                </div>
                                                            </div>
                        </div>
                    </div>"""

def add_alumni(name, desig, role,  img, mail ):

    return f"""                <div class="col-md-5 col-lg-3">
                    <div class="guide-item">
                        <div class="guide-img">
                            <div class="guide-img-efects text-center">
                                <img src="{img}" class="img-fluid w-100" alt="Image" style="max-height:250px; object-fit:cover;">
                            </div>
                            <div class="guide-icon rounded-pill p-2">
                                <a class="btn btn-square btn-primary rounded-circle mx-1" href="{mail}"><i
                                        class="fa fa-envelope"></i></a>
                            </div>
                        </div>
                        <div class="guide-title text-center rounded-bottom p-4">
                            <div class="guide-title-inner">
                                <p class="mb-0 mt-2"><strong style="color:black;margin:auto; padding:auto;">Role: </strong>{role}</p>
                                <h4 class="mt-0">{name}</h4>
                                <p class="mb-0"><strong style="color:red;">Current: </strong>{desig}</p>
                            </div>
                        </div>
                    </div>
                </div>"""
                

def return_head_tail(mem_type, style = 1):
    if style == 1:
        section_head = f"""<div class="container-fluid guide py-2">
                <div class="container py-2">
                    <div class="mx-auto text-center mb-5" style="max-width: 900px;">
                        <h5 class="section-title px-3">{mem_type}</h5>
                    </div>
                    <div class="row g-4 justify-content-center">"""
    else: 
        section_head = f""" <div class="container-fluid blog py-5">
            <div class="container py-5">
                <div class="mx-auto text-center mb-5" style="max-width: 900px;">
                    <h5 class="section-title px-3">{mem_type}</h5>
                </div>
                <div class="row g-4 justify-content-center">"""

    section_tail = """</div></div></div>"""
    return section_head, section_tail

infos = json.load(open('./info/team.json'))
template = open('./templates/team_template.html').readlines()

header = template[:277]
tail = template[277:]

full_html = "" + ''.join(header)
for item in infos:
    head = ""
    if item == 'alumni':
        section_head, section_tail = return_head_tail('Alumni')
        head += section_head
        for mem in infos[item]:
            head += add_alumni(mem['name'], mem['desig'], mem['role'], mem['img'], mem['mail'])
        head += section_tail
    elif item == 'others':
        section_head, section_tail = return_head_tail('Others')
        head += section_head
        for mem in infos[item]:
            head += add_mem(mem['name'], mem['desig'], mem['img'], '#', '#', '#', '#')
        head += section_tail
    elif item == 'phd':
        section_head, section_tail = return_head_tail('PhD Scholars', style=2)
        head += section_head
        for mem in infos[item]:
            head += add_mem(name = mem['name'], desig = mem['desig'], sub = mem['sub'],
                            img = mem['img'], mail = mem['mail'], tw = mem['tw'], fb = mem['fb'],
                            linkedin = mem['linkedin'], style = 2, interest=mem['interest'])
        head += section_tail
    elif item == 'postdoc':
        section_head, section_tail = return_head_tail('Postdoctoral Fellows')
        head += section_head
        for mem in infos[item]:
            head += add_mem(name = mem['name'], desig = mem['desig'], sub = "",
                            img = mem['img'], mail = mem['mail'], tw = mem['tw'], fb = mem['fb'],
                            linkedin = mem['linkedin'], style = 1, interest=mem['interest'])
        head += section_tail
    elif item == 'project':
        section_head, section_tail = return_head_tail('Project Students')
        head += section_head
        if len(infos[item]):
            for mem in infos[item]:
                head += add_mem(name = mem['name'], desig = mem['desig'] , sub = "",
                                img = mem['img'], mail = mem['mail'], tw = mem['tw'], fb = mem['fb'],
                                linkedin = mem['linkedin'], style = 1, interest = mem['interest'])
        else:
            head += """
                            <div class="col-md-6 col-lg-3">
                    <div class="guide-item">
                        <div class="guide-img">
                            <div class="guide-img-efects">
                                <img src="./img/avatar_scholar_128.png" class="img-fluid w-100 rounded-top" alt="Image">
                            </div>
                        </div>
                        <div class="guide-title text-center rounded-bottom p-4">
                            <div class="guide-title-inner" style="margin-top:10px;">
                                <p class="mb-0">Project</p>
                                <h4 class="mt-0">Fname Lname</h4>
                                <p class="mb-0"></p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-6" style="margin: auto;">
                    <div class="guide-item">
                        <h4 class="mt-0 mb-5">Currently, we have no project students, but we'd love to collaborate with
                            you! If you're interested in working with us,
                            please reach out. For more details, click the link below.</h4>
                        <a class="btn-hover-bg btn btn-primary rounded-pill text-white py-3 px-5" href="positions.html">
                            Oportunities</a>
                    </div>
                </div>
            """
            
        head += section_tail
    full_html += head
full_html += ''.join(tail)

with open('team.html', 'w') as f:
    f.write(full_html)