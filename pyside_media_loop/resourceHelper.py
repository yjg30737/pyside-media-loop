import os

def setStyleSheet(widgets: list, style_sheets: list):
    caller_path = os.path.dirname(__file__)

    def getStyleSheetOf(i):
        css_file_path = os.path.join(caller_path, style_sheets[i])
        css_file = open(css_file_path)
        css_code = css_file.read()
        css_file.close()
        return css_code

    if len(style_sheets) == 1:
        for i in range(len(widgets)):
            css_code = getStyleSheetOf(0)
            widgets[i].setStyleSheet(css_code)
    elif len(style_sheets) == 2:
        for i in range(len(widgets)):
            css_code = getStyleSheetOf(i % 2)
            widgets[i % 2].setStyleSheet(css_code)
    else:
        for i in range(len(widgets)):
            css_code = getStyleSheetOf(i)
            widgets[i].setStyleSheet(css_code)