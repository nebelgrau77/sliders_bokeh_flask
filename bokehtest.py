from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure

from bokeh.embed import components
from bokeh.resources import INLINE

def bokeh_test():

    #output_file("js_on_change.html")

    x = [x*0.005 for x in range(0, 200)]
    y = x
    lw = 5
    
    test_source = ColumnDataSource(data=dict(x=x, y=y))

    plot = Figure(plot_width=400, plot_height=400)
    plot.line(x='x', y='y', line_width=lw, source=test_source)
    
    callback = CustomJS(args=dict(source=test_source), code="""
        var data = source.data;
        var f = cb_obj.value
        var x = data['x']
        var y = data['y']
        
        for (var i = 0; i < x.length; i++) {
            y[i] = f
        }

        source.change.emit();
    """)  

    slider = Slider(start=0.1, end=5, value=1, step=.2, title="power")
    slider.js_on_change('value', callback)

    layout = column(slider, plot)
    
    #grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    #get the resources from the figure components
    script, div = components(layout)

    return script, div, js_resources, css_resources