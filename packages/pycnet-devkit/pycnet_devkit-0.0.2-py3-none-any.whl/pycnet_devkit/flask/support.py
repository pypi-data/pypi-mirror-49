from flask import request, render_template, url_for, render_template_string
from functools import wraps


def form(*args):
    if len(args) == 1:
        return request.form.get(args[0])
    return tuple(request.form.get(a) for a in args)


def templated(template=None, GET_direct=True):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            if GET_direct:
                if request.method == 'GET':
                    return render_template(template_name)
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def view_sitemap(app, sitemap_template=None):
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    routes = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            routes.append({'name': rule.endpoint, 'url': url})
    if sitemap_template is None:
        return render_template_string('''
{%for route in routes%}
<p><a href="{{route['url']}}">{{route['name']}}</a></p>
{%endfor%}
''', routes=routes)
    else:
        return render_template(sitemap_template, routes=routes)
