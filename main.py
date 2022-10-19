from flask import Flask, render_template, send_file
from constants import*
import markdown
import os
import json

app=Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

@app.route('/')
def index():
    return render_template('html/index.html', name='index')

@app.route('/projects')
def projects():
    project_names=[]
    for file in os.listdir("projects"):
        if file.endswith(".json"):
            project_names.append(file.removesuffix('.json'))
    return render_template('html/projects.html', project_names=project_names, name='projects')

@app.route('/projects/<path:path>')
def get_project(path):
    with open(f'projects/{path}.json', 'r') as f:
        data=json.loads(f.read())
    with open(f'projects/{path}.code', 'r') as f:
        code=f.read()
    return render_template(f'html/project_template.html', name='projects',
                            project_title=data["project_title"], language=data["language"],
                            code=code, description=data["description"], link=data["link"])

@app.route('/documents/<path:path>')
def documents(path):
    #directory=os.path.join(app.root_path, 'documents')
    #return send_from_directory(directory=directory, filename=path)
    return send_file(f'documents/{path}', as_attachment=True)

@app.errorhandler(404)
def not_found(e):
    return render_template('html/error_pages/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    with open('error_log.txt', 'a') as f:
        f.write('=========ERROR=========')
        f.write(str(e))
        f.write('=========ERROR=========')
    return render_template('html/error_pages/500.html'), 500

if __name__=='__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
