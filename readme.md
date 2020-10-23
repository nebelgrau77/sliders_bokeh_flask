### ideas

__First view__: 6 sliders for the KPIs, one menu to choose "product". Choosing the "product" sets the sliders into the positions of this dealer's KPIs, and the chart shows the score.
Moving the sliders changes the score. Needs a RESET button to show the original value, or show the original value and the new value (better).

__Second view__: as above, but with all the details, not single KPIs.

useful examples: 
* https://docs.bokeh.org/en/latest/docs/gallery/periodic.html
* https://demo.bokeh.org/movies

Start with a simple example: two "products", eg. brand A TV and brand B TV. 
* The parameters are price (rated from 1 to 10) and quality, also from 1 to 10. 
* Price impact on the score is 60%, quality 40%. So the overall score is\
   _price * 0.6 + quality * 0.4_

Sliders work with JS callback, but it's very hacky. It loses all the modular approach where the weights, colors etc. can be quickly updated. 
In order to restore this, an idea is to use one JS code block with formatting, restoring at least partially the modular idea. 

Not sure how this can work with other elements, e.g. query selected from a menu, etc.

