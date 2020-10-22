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

So there will be a slider to choose between "brand A" and "brand B".\
In the database only the product name and the points for various parameters will be stored: the calculation of the overall score is dynamic, on request.\
Therefore the query will return two point values, that will feed the chart (actually a number in a square).\
These values will also be the starting values for the sliders.\
Color of the box depends on the value (eg. red below 4, yellow below 7, otherwise green).

_The second square will have the value calculated from the sliders._The

This all works so far, except for the value calculated from the sliders. It seems that the bokeh server is needed for the callbacks to work correctly.

