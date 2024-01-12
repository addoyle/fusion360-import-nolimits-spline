import adsk.core
import json
import xml.etree.ElementTree as ET
from ....common.util import log, ui, command_inputs
from ..state import supports


def browse_btn_handler(args: adsk.core.HTMLEventArgs):
    if (args.action == 'click' and args.data == 'browseBtn'):
        open_xml(args.browserCommandInput)


def activated_handler(args: adsk.core.CommandEventArgs):
    if (not len(supports.structures)):
        open_xml(args.command.commandInputs.itemById('supportsXmlBtn'))


def open_xml(browser_input: adsk.core.BrowserCommandInput):
    dlg = ui.createFileDialog()
    dlg.title = 'Open NoLimits Supports XML'
    dlg.filter = 'XML Files (*.xml);;All Files (*.*)'
    if (dlg.showOpen() != adsk.core.DialogResults.DialogOK):
        browser_input.sendInfoToHTML('reset', '{}')
        supports.clear()
    else:
        tree: ET.ElementTree = ET.parse(dlg.filename)
        xml_root = tree.getroot()

        supports.clear()
        add_support_strucs(xml_root.find('supports'))

        if (len(supports.structures)):
            browser_input.sendInfoToHTML('update', json.dumps(
                {'msg': f'{len(supports.structures)} structures'}))

        # for struc in supports.structures:
        #     log(f'{struc}')


def add_support_struc(struc):
    if struc.tag == 'prefab':
        # We don't care about the other stuff in prefabs, just the atomization
        add_support_strucs(struc.find('atomization').find('supports'))
    elif struc.tag == 'rasc':
        supports.add_rail_support_connector(struc)
    elif struc.tag == 'freenode':
        supports.add_free_node(struc)
    elif struc.tag == 'footernode':
        supports.add_footer(struc)
    elif struc.tag == 'beam':
        supports.add_beam(struc)
    else:
        log(f'Unsupported struc: {struc.tag}')


def add_support_strucs(strucs):
    for struc in strucs:
        add_support_struc(struc)
