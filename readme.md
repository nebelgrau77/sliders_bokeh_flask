### ideas
__First view__: sliders for the KPIs, menu choose "product". Choosing the "product" sets the sliders into the positions of the current KPIs, and the chart shows the score.
Moving the sliders changes the score. Needs a RESET button to show the original value, or show the original value and the new value (better). - DONE

__Second view__: as above, but with all the details, not single KPIs.

useful examples: 
* https://docs.bokeh.org/en/latest/docs/gallery/periodic.html
* https://demo.bokeh.org/movies

Sliders work with JS callback, but it's a bit hacky. With proper use of string formatting it is still possible to maintain the modular approach where the weights, colors etc. can be quickly updated. 

__NEW__:
Added "birthday color generator", scaled to cover the whole RGB gamut. 

_NOTE_: it does not account for shorter months, i.e. it's possible to choose "February, 30".

TO DO:   
* further improve modularity of the JS code if possible
* add CRUD interface to be able to add, update or remove records.
* add a machine learning-based app that will guess the origin of the car based on supplied parameters

