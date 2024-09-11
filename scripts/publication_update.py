import contextlib
import json
import numpy as np

template = open('./templates/publication_template.html').readlines()
header = template[:84]
tail = template[84:]

start_section = """ 
                        <section id="faq" class="faq section light-background py-5">

        <div class="mx-auto text-center mb-5" style="max-width: 900px;">
            <h5 class="section-title px-3">Publications</h5>
            <h1 class="mb-0">Recently published papers</h1>
            <p class="mb-4">
            Below is a list of papers published by our group in various journals, arranged by publication date, up to 2010. For the complete and updated list, please visit our <a href="https://scholar.google.co.in/citations?hl=en&user=dcj-bnsAAAAJ&view_op=list_works&sortby=pubdate"><strong style="color:red;">Google Scholar</strong></a> page.
            </p>
        </div>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-12" data-aos="fade-up" data-aos-delay="100">
                    <div class="faq-container">
                    
                    """
end_section = """  
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

pub_data = open('./info/data.json')
pub_data = json.load(pub_data)


assemble_year = []
for data in pub_data:
    with contextlib.suppress(Exception):
        assemble_year.append(data['year'])
years = np.sort(np.unique(assemble_year))[::-1]
years = years[np.where(years>'2009')]

temp_year = '2024'

ordered_dict = {str(year): [] for year in years}
for data in pub_data:
    with contextlib.suppress(Exception):
        year = data['year']
        ordered_dict[year].append(data)

def pub_format(title, authors, publication, link):
    return f"""                                    <div class="card my-3">
                                        <h6 class="card-header" style="color:#32821c;">{publication}</h6>
                                        <div class="card-body">
                                            <a href="{link}"><h5 class="card-title">{title}</h5></a>
                                            <p class="card-text">{authors}</p>
                                            <a href="{link}" class="btn btn-primary">Link to article</a>
                                        </div>
                                    </div>"""

year = years[0]
year_start = f""" <div class="faq-item faq-active">
                            <h2>{year}</h2>
                            <div class="faq-content" style="background-color:antiquewhite;">
                                <div class="col-lg-12">
                                
                                """
for item in ordered_dict[year]:
    year_start += pub_format(item['title'], item['authors'], item['publication'], item['link'])
year_start += """    
</div>
                            </div>
                            <i class="faq-toggle bi bi-chevron-right"></i>
                        </div>"""

for year in years[1:]:
    year_start += f"""                        <div class="faq-item">
                            <h2>{year}</h2>
                            <div class="faq-content style="background-color:antiquewhite;">
                                <div class="col-lg-12">"""
    for item in ordered_dict[year]:
        year_start += pub_format(item['title'], item['authors'], item['publication'], item['link'])
    year_start += """    
                    </div>
                            </div>
                            <i class="faq-toggle bi bi-chevron-right"></i>
                            </div>"""

with open('./publication.html', 'w') as f:
    f.write(''.join(header))
    f.write(start_section)
    f.write(year_start)
    f.write(end_section)
    f.write(''.join(tail))