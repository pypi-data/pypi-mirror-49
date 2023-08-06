from flask import request
import secrets


def load_jinja_functions(app):
    def field_text(name,default,label=None):
        label = label or name
        default = request.form.get(name,default)
        return f'{label}:<br><input type="text" name="{name}" value="{default}">'

    def field_select(name,list,label=None):
        label = label or name
        default = request.form.get(name,list[0])
        html = f'{label}:<br><select name="{name}" id="{name}">'
        for ele in list:
            html += f'<option value="{ele}">{ele}</option>'
        html += '</select>'
        html += f'<script type="text/javascript">document.getElementById("{name}").value = "{default}";</script>'
        return html
    
    def field_checkbox(name,label=None):
        label = label or name
        default = request.form.get(name,'false')
        html = f'<input type="checkbox" name="{name}" id="{name}" value="true">{label}<br>'
        html += f'<script type="text/javascript">document.getElementById("{name}").checked = {default};</script>'
        return html

    def field_submit(label='Submit'):
        return f'<input type="submit" value="{label}">'

    def load_vega():
        return '''
    <script src="https://cdn.jsdelivr.net/npm/vega@5.4.0"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@3.3.0"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@4.2.0"></script>
    '''

    def altair_chart(json):
        code = secrets.token_hex(6)
        html = f'<div id="{code}"></div><br>'
        html += f'<script type="text/javascript">vegaEmbed("#{code}", {json});</script>'
        return html

    
    app.jinja_env.globals.update(field_text=field_text)
    app.jinja_env.globals.update(field_select=field_select)
    app.jinja_env.globals.update(field_checkbox=field_checkbox)
    app.jinja_env.globals.update(field_submit=field_submit)
    app.jinja_env.globals.update(load_vega=load_vega)
    app.jinja_env.globals.update(altair_chart=altair_chart)


