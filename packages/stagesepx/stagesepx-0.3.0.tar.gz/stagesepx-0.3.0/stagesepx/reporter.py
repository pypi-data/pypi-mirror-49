import typing
import numpy as np
from jinja2 import Markup, Template
from base64 import b64encode
import cv2
from pyecharts.charts import Line, Bar, Page
from pyecharts import options as opts
from loguru import logger

from stagesepx.classifier import ClassifierResult
from stagesepx import toolbox

TEMPLATE = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>stagesep-x report :)</title>
</head>
<body>
    <h1>stagesep-x report</h1>
    
    {% if dir_link_list %}
        <h2>Raw Pictures</h2>
            <ul>
                {% for each_link in dir_link_list %}
                    <li>
                        <a href="{{ each_link }}">{{ each_link }}</a>
                    </li>
                {% endfor %}
            </ul>
    {% endif %}
    
    {% if thumbnail_list %}
        <h2>Thumbnail</h2>
            <ul>
                {% for name, each_thumbnail in thumbnail_list %}
                    <li>
                        <h3> {{ name }} </h3>
                        <img src="data:image/png;base64,{{ each_thumbnail }}"/>
                    </li>
                {% endfor %}
            </ul>
    {% endif %}
    
    <h2>Charts</h2>
    <div>
        {{ chart }}
    </div>
</body>
</html>
<body>

</body>
</html>
'''


class Reporter(object):
    def __init__(self):
        self.dir_link_list: typing.List[str] = list()
        self.thumbnail_list: typing.List[typing.Tuple[str, str]] = list()

    def add_dir_link(self, data_path: str):
        self.dir_link_list.append(data_path)

    def add_thumbnail(self, name: str, pic_object: np.ndarray):
        buffer = cv2.imencode(".png", pic_object)[1].tostring()
        b64_str = b64encode(buffer).decode()
        self.thumbnail_list.append((name, b64_str))

    @staticmethod
    def _draw_line(data_list: typing.List[ClassifierResult]) -> Line:
        # draw line chart
        x_axis = [str(i.timestamp) for i in data_list]
        y_axis = [i.stage for i in data_list]

        line = Line()
        line.add_xaxis(x_axis)
        line.add_yaxis("stage",
                       y_axis,
                       is_step=True,
                       is_symbol_show=True)
        line.set_global_opts(
            title_opts=opts.TitleOpts(title='Trend'),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis', axis_pointer_type='cross'),
        )
        return line

    @staticmethod
    def _draw_bar(data_list: typing.List[ClassifierResult]) -> Bar:
        # draw bar chart
        bar = Bar()
        x_axis = sorted(list(set([i.stage for i in data_list])))
        y_axis = list()
        offset = data_list[1].timestamp - data_list[0].timestamp
        for each_stage_name in x_axis:
            each_stage = sorted([i for i in data_list if i.stage == each_stage_name], key=lambda x: x.frame_id)
            time_cost = each_stage[-1].timestamp - each_stage[0].timestamp + offset
            y_axis.append(time_cost)

        bar.add_xaxis(x_axis)
        bar.add_yaxis('time cost', y_axis)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="Time Cost"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
        logger.debug(f'time cost: {dict(zip(x_axis, y_axis))}')
        return bar

    def draw(self,
             data_list: typing.List[ClassifierResult],
             report_path: str = None):
        # draw
        line = self._draw_line(data_list)
        bar = self._draw_bar(data_list)

        # merge charts
        page = Page()
        page.add(line)
        page.add(bar)

        # insert extras
        template = Template(TEMPLATE)
        template_content = template.render(
            chart=Markup(page.render_embed()),
            dir_link_list=self.dir_link_list,
            thumbnail_list=self.thumbnail_list,
        )

        # save to file
        if not report_path:
            report_path = f'{toolbox.get_timestamp_str()}.html'
        with open(report_path, "w") as fh:
            fh.write(template_content)
        logger.info(f'save report to {report_path}')
