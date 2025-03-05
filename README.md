# dashboard-templates
A repository of dashboard templates, for use in pathogen surveillance activities (especially wastewater-integrated surveillance). 

Each of the subdirectories of this repository includes a fully functional, Plotly Dash based web-ready dashboard, which can be modified as needed for public health use. If you aren't familiar with Plotly Dash, we recommend first working through the [Dash tutorial](https://dash.plotly.com/tutorial). 

For testing purposes, each of these scripts can be run using `python app.py`. However, for real-world deployment purposes you'll want to use a production WSGI server such as gunicorn. 

For examples of fully functional, live wastewater-integrated dashboards, we recommend checking out:
1. [Lone_pine](https://github.com/andersen-lab/lone_pine), which supports the [SEARCH dashboard](https://searchcovid.info/dashboards/wastewater-surveillance/)
2. [NICD Wastewater Dashboard](https://github.com/NICD-Wastewater-Genomics/Wastewater-Dashboard), which supports the [NICD National Wastewater Surveillance Dashboard](https://wastewater.nicd.ac.za/). 