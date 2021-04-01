# -*- coding: utf-8 -*-

from docx import Document

def load_file(file_path):
    docx_file = Document(file_path)
    # print(docx_file.paragraphs)
    # print(docx_file.sections)
    for paragraph in docx_file.paragraphs:
        print(paragraph.text)

    # The footer and header # 页眉和页脚
    # for section in docx_file.sections:
    #     print(section)
    # for table in docx_file.tables:
    #     print(table.start_type)
    # print(docx_file.tables)
    return docx_file


def extract_title(file_docx):
    return dict()


def gen_output(dict_title, output_file):
    pass


if __name__ == '__main__':
    # get doc and load the content
    # extract the title of every requirement
    # generate the output file of extraction

    file_input = 'C:\\jack\\Work\\Project\\Inner Project\\Auto-Trader\\AT3.2\\AT 3.2.1\\需求说明书 20190524\\temp\\AT 3.2 产品需求说明书.docx'
    file_output = ''

    req_doc = load_file(file_input)
    title_dict = extract_title(req_doc)
    gen_output(title_dict, file_output)
