import os
from os.path import dirname, exists, join
from uuid import uuid4

import htmlmin
import yaml
from IPython.display import display, HTML
from css_html_js_minify import css_minify

from reportlib.utils.mailing import send_email
from reportlib.utils.pandas.styler import Styler
from reportlib.utils.templating import template_loader


class Generator:
    template_name = 'base/base.html'
    styles = ['base/styles.css', 'styles.css']

    def __init__(self, options):
        self.context = {
            'title': '',
            'extras': {},
            'tables': [],
        }
        self.options = options
        self.attactments = []

    def add_table(self, style, context=None):
        context = context or {}
        self.context['tables'].append({
            'style': style,
            'context': context,
        })
        
    def add_grouped_table(self, tables):
        for i, table in enumerate(tables):
            if isinstance(table, Styler):
                table = {'style': table}
            if 'context' not in table:
                table['context'] = {}
            if i > 0:
                table['context']['skip_table_open_tag'] = True
            if i < len(tables) - 1:
                table['context']['skip_table_close_tag'] = True
            self.context['tables'].append(table)
        
    def _load_styles(self):
        self.context['styles'] = []
        for path in self.styles:
            for template_folder in template_loader.env.loader.searchpath:
                _path = join(template_folder, path)
                if exists(_path):
                    with open(_path, 'r') as f:
                        css = f.read()
                        css = css_minify(css)
                        self.context['styles'].append(css)
                    break

    def run(self):
        self.template = template_loader.get_template(self.template_name)
        self._load_styles()
      
        html_string = self.render_html()
        display(HTML(html_string))

        self.write_to_file(html_string)
        self.send_email(html_string)

    def write_to_file(self, html_string):
        output_path = self.options.get('HTML_OUTPUT_PATH')
        if output_path:
            output_path = os.path.abspath(output_path)
            os.makedirs(dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_string)

    def send_email(self, html_string):
        email_cfg_path = self.options.get('EMAIL_CONFIG_PATH')
        email_env = self.options.get('EMAIL_ENV')
        if email_cfg_path and email_env:
            with open(email_cfg_path, 'r') as f:
                email_cfgs = yaml.load(f, Loader=yaml.FullLoader)
            if email_env in email_cfgs:
                email_cfg = email_cfgs[email_env]
                email_cfg['subject'] = email_cfg['subject'].format(uuid4=uuid4(), **self.options)
                send_email(email_cfg, html_string)
            else:
                print(f"ERROR: email_env = {email_env} not exists. Available env: {' '.join(email_cfgs.keys())}")

    def render_html(self):
        html_string = self.template.render(self.context)
        html_string = htmlmin.minify(
            html_string,
            remove_comments=True,
            remove_empty_space=True,
            reduce_boolean_attributes=True,
            reduce_empty_attributes=True,
            remove_optional_attribute_quotes=True,
            convert_charrefs=True,
        )
        return html_string

