import io, adsk.core, json
from ....common.util import ui, command_inputs
from ..state import spline

def browse_btn_handler(args: adsk.core.HTMLEventArgs):
    if (args.action == 'click' and args.data == 'browseBtn'):
        open_csv(args.browserCommandInput)


def activated_handler(args: adsk.core.CommandEventArgs):
    if (not spline.count):
        open_csv(args.command.commandInputs.itemById('splineDataBtn'))

def open_csv(browser_input: adsk.core.BrowserCommandInput):
    dlg = ui.createFileDialog()
    dlg.title = 'Open NoLimits Spline CSV'
    dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
    if (dlg.showOpen() != adsk.core.DialogResults.DialogOK):
        browser_input.sendInfoToHTML('reset', '{}')
        spline.clear()
    else:
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
        
        if (len(spline.center)):
            browser_input.sendInfoToHTML('update', json.dumps({'msg': f'{len(spline.center)} points'}))

    # Update point index inputs
    start_point_input: adsk.core.IntegerSpinnerCommandInput = command_inputs['startPoint']
    end_point_input: adsk.core.IntegerSpinnerCommandInput = command_inputs['endPoint']

    if (spline.count):
        if start_point_input.value > spline.count:
            start_point_input.value = 1
        if end_point_input.value > spline.count or end_point_input.value == 1:
            end_point_input.value = spline.count

        # Force trigger value input change handler
        prev = start_point_input.value
        start_point_input.value = 0
        start_point_input.value = prev
    else:
        start_point_input.value = 1
        end_point_input.value = 1

def add_point(point):
    c_point = [float(i) for i in point[1:4]]
    l_point = [float(i) for i in point[7:10]]

    spline.center.append(to_point3ds(c_point))
    spline.left.append(to_point3ds([a + b for a, b in zip(c_point, l_point)]))
    spline.right.append(to_point3ds([a - b for a, b in zip(c_point, l_point)]))

def to_point3ds(coord):
    return adsk.core.Point3D.create(
        # Flip y/z because NL orientation is Y-up, Fusion 360 is Z-up
        coord[0],   # x
        coord[2],   # z
        coord[1]    # y
    )