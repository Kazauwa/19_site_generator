import os
import json
import jinja2
import settings
from markdown import markdownFromFile


def load_config():
    with open('config.json', 'r') as json_data:
        config = json.load(json_data)
    return config


def get_article_savepath(source):
    path, name = os.path.split(source)
    path = os.path.join(settings.TEMPLATES_HOME, path)
    name = name.replace('.md', '.html')
    path = os.path.join(settings.TEMPLATES_HOME, name)
    return path, name


def wrap_in_base_template(article_html):
    head_wrap = '{% extends "base.html" %}\n{% block content %}\n'
    foot_wrap = '\n{% endblock %}'
    with open(article_html, 'r') as original:
        content = original.read()
    with open(article_html, 'w') as modified:
        modified.write(head_wrap + content + foot_wrap)


def render_jinja_html(template_path, **context):
    template_path, template_name = os.path. split(template_path)
    loader = jinja2.FileSystemLoader(template_path)
    environment = jinja2.Environment(loader=loader)
    template = environment.get_template(template_name)
    template = template.render(context)
    return template
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_path)
    ).get_template(template_name).render(context)


def save_rendered_template(template_path, template):
    with open(template_path, 'w') as writer:
        writer.write(template)


if __name__ == '__main__':
    config = load_config()

    articles_list = config['articles']
    articles_sources = [article['source'] for article in articles_list]
    topics_list = config['topics']

    for article in articles_list:
        output, article['slug'] = get_article_savepath(article['source'])
        source = os.path.join('articles', article['source'])
        markdownFromFile(input=source, output=output)
        wrap_in_base_template(output)
        template = render_jinja_html(output)
        save_rendered_template(output, template)

    index_template = render_jinja_html(settings.INDEX_TEMPLATE,
                                       articles=articles_list,
                                       topics=topics_list)
    save_rendered_template(settings.INDEX_PAGE, index_template)
