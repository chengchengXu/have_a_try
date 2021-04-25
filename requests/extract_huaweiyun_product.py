# coding: utf-8

import requests as rq
from bs4 import BeautifulSoup
import re
import csv


def get_url():
    return 'https://www.huaweicloud.com/product/'


def extract_url_content(url):
    product_content = dict()
    r = rq.get(url)
    soup = BeautifulSoup(r.content.decode(), 'html.parser')
    # print(r.content.decode())
    # print(soup.prettify())

    # divs = soup.find_all(attrs={"class": "v6-section v6-section-product-overview product-overview-type"})
    # print(divs)
    # print(len(divs))
    for div in soup.find_all(attrs={"class": "v6-section v6-section-product-overview product-overview-type"}):
        title_name = div['bi_parent_name'].strip()
        title_desc = div.find('p', attrs={"class": "v6-section-subtitle"})
        title_desc = title_desc.string.strip() if title_desc else ""
        # print(title_name)
        # print(title_desc)

        sections = div.find_all('div', attrs={"class": re.compile(r"product-overview-type-title.*")})
        projects = div.find_all('div', attrs={"class": re.compile(r"tab-content-list-item cf.*")})
        # print(len(sections), len(projects))
        # print(sections)
        # print(projects)
        dict_section = dict()
        for section, mult_project in zip(sections, projects):
            # print(section)
            # print(mult_project)
            # print(section.contents[0])
            # print(mult_project)
            dict_project = dict()
            for project in mult_project.find_all('div', attrs={"class": "product-introduce"}):
                if 'href' not in project.a.attrs:
                    continue
                project_link = project.a['href'].strip()
                spans = project.find_all('span', attrs={"class": "p-i-name"})
                project_name = ' | '.join([n.string.strip() for n in (spans if spans else []) if n.string])
                p = project.find('p', attrs={"class": "js-title"})
                project_desc = p.string.strip() if p else ""
                # print(project_name)
                # print(project_desc)
                # print(project_link)
                dict_project[(project_name, project_desc)] = project_link

            dict_section[section.contents[0]] = dict_project

        product_content[(title_name, title_desc)] = dict_section

    return product_content


def output_product_content(product_content):
    file_path = 'test.csv'
    list_content = [['title name', 'title description', 'section name', 'project name', 'project description', 'project link']]
    for (t_name, t_desc), sections in product_content.items():
        list_content.extend([[t_name, t_desc, "", "", ""]])
        for s_name, projects in sections.items():
            list_content.extend([["", "", s_name, "", ""]])
            for (p_n, p_d), p_link in projects.items():
                list_content.extend([["", "", "", p_n, p_d, p_link]])

    with open(file_path, mode='w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        wr.writerows(list_content)

    return file_path


def main():
    url = get_url()
    product_content = extract_url_content(url)
    file_path = output_product_content(product_content)
    print(file_path)


if __name__ == '__main__':
    main()
