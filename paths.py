# -*- coding: utf-8 -*-
import os

SCRIPT_DIR = os.path.dirname(__file__)
GRAPH_DIR = os.path.join(SCRIPT_DIR, 'Graphs_for_seenopsis')
HTML_DIR = os.path.join(SCRIPT_DIR, 'html_data')

if not os.path.isdir(GRAPH_DIR):
    os.makedirs(GRAPH_DIR)
    
HTML_TEMPLATE_FILE_PATH =  os.path.join(HTML_DIR, 'html_template.html')
HTML_BODY_FILE_PATH = os.path.join(HTML_DIR, 'html_body.html')

with open(HTML_TEMPLATE_FILE_PATH, "r") as f:
    HTML_TEMPLATE_STR = f.read()
    
with open(HTML_BODY_FILE_PATH, "r") as f:
    HTML_BODY_STR = f.read()