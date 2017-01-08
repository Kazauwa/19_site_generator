import os
import json
import jinja2
import settings
from markdown import markdownFromFile


def load_config():
    with open('config.json', 'r') as json_data:
        config = json.load(json_data)
    return config


def get_article_savepath_and_slug(template_source):
    path, name = os.path.split(template_source)
    name = name.replace('.md', '.html')
    path = os.path.join(settings.TEMPLATES_HOME, path)
    path = os.path.join(settings.TEMPLATES_HOME, name)
    return path, name


def wrap_in_base_template(article_html):
    head_wrap = '{% extends "base.html" %}\n{% block content %}\n'
    foot_wrap = '\n{% endblock %}'
    with open(article_html, 'r') as original_template:
        content = original_template.read()
    with open(article_html, 'w') as modified_template:
        modified_template.write(head_wrap + content + foot_wrap)


def render_jinja_html(template_path, **context):
    template_path, template_name = os.path. split(template_path)
    loader = jinja2.FileSystemLoader(template_path)
    environment = jinja2.Environment(loader=loader)
    template = environment.get_template(template_name)
    template = template.render(context)
    return template


def save_rendered_template(savepath, template):
    with open(savepath, 'w') as writer:
        writer.write(template)


if __name__ == '__main__':
    config = load_config()

    articles_list = config['articles']
    topics_list = config['topics']

    for article in articles_list:
        article_output, article['slug'] = get_article_savepath_and_slug(article['source'])
        article_source = os.path.join('articles', article['source'])
        markdownFromFile(input=article_source, output=article_output)
        wrap_in_base_template(article_output)
        article_template = render_jinja_html(article_output)
        save_rendered_template(savepath=article_output, template=article_template)

    index_template = render_jinja_html(settings.INDEX_TEMPLATE,
                                       articles=articles_list,
                                       topics=topics_list)
    save_rendered_template(savepath=settings.INDEX_PAGE, template=index_template)
