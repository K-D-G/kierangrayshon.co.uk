from flask import Flask, render_template, send_from_directory

app=Flask(__name__)

@app.route('/static/<string:folder>/<string:file>')
def static_serve(folder, file):
    print('Executed')
    return send_from_directory('templates', folder+'/'+file)

@app.route('/')
def index():
    return render_template('html/index.html')


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
