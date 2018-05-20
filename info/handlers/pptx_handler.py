import json
import datetime
import os
import calendar
import datetime as dt

# imports - don't remove any of these, even if they seem as if they aren't being used

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_AUTO_SIZE, MSO_VERTICAL_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.dml import *

from WWPHSSinfo.settings import BASE_DIR


def create_pptx(data):
    template = Presentation(os.path.join(BASE_DIR, 'template.pptx'))
    #print(transform_data(data))

    title_slide_layout = template.slide_layouts[6]
    title_slide = template.slides.add_slide(title_slide_layout)

    shapes = title_slide.shapes
    d = datetime.datetime.strptime(data['board']['timestamp'].split('+')[0], '%Y-%m-%d %H:%M:%S.%f').date()
    shapes.title.text = str(d)

    return template
