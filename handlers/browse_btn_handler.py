import io, adsk.core, json
from ..common.util import log, ui, spline
from mimetypes import init

def browse_btn_handler(args: adsk.core.HTMLEventArgs):
    global ui, spline

    browser_input = args.browserCommandInput

    if (args.action == 'click' and args.data == 'browseBtn'):
        dlg = ui.createFileDialog()
        dlg.title = 'Open NoLimits Spline CSV'
        dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
        if (dlg.showOpen() != adsk.core.DialogResults.DialogOK):

            browser_input.sendInfoToHTML('reset', '{}')
            return

        filename = dlg.filename
        with io.open(filename, 'r', encoding='utf-8-sig') as f:
            # First line is the header row
            line = f.readline()

            # Get first actual line of data
            line = f.readline()

            spline.left = []
            spline.right = []
            spline.center = []

            while line:
                add_point(line.split('\t'))
                line = f.readline()
        
        if (spline.center.count):
            browser_input.sendInfoToHTML('update', json.dumps({'count': len(spline.center)}))
            

def add_point(point):
    global spline

    c_point = [float(i) for i in point[1:4]]
    l_point = [float(i) for i in point[7:10]]

    spline.center.append(to_point3ds(c_point))
    spline.left.append(to_point3ds([a + b for a, b in zip(c_point, l_point)]))
    spline.right.append(to_point3ds([a - b for a, b in zip(c_point, l_point)]))

def to_point3ds(coord):
    return adsk.core.Point3D.create(coord[0], -coord[1], coord[2])