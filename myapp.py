# Data handling
import pandas as pd
import numpy as np

# Bokeh libraries
from bokeh.io import output_file, output_notebook,curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, PanTool
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import figure

# Import data
df_can = pd.read_csv('immigrant.csv')

# Drop kolom yang tidak diperlukan
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)

# Rename nama kolom
df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace=True)

# Casting semua nama kolom menjadi bertipe string
df_can.columns = list(map(str, df_can.columns))

# Buat nama country menjadi index
df_can.set_index('Country', inplace=True)

# add total column
df_can['Total'] = df_can.sum(axis=1)

# Pilih rentang tahun untuk dilakukan visualisasi
years = list(map(str, range(1980, 2014)))
print('data dimensions:', df_can.shape)

# Pilih imigran dari Indonesia yang akan divisualisasikan datanya
df_countries = df_can.loc[['Indonesia'],years].transpose()
df_ind = pd.DataFrame(df_countries.sum(axis=1))
df_ind.reset_index(inplace=True)
df_ind.columns = ["Tahun", "Jumlah_Imigran"]
df_ind["Tahun"] = df_ind["Tahun"].astype(int)

# Konversi data menjadi cds
source = ColumnDataSource(data={
    'Tahun'                : df_ind['Tahun'],
    'Jumlah_Imigran'       : df_ind['Jumlah_Imigran'],
})

# Melakukan pembuatan figur dengan X-axis = Tahun dan Y-axis = Jumlah Imigran
a = figure(title='Jumlah Imigran Asal Indonesia Yang Menetap di Kanada',
                  plot_height=400,
                  plot_width= 700,
                  x_axis_label='Tahun',
                  y_axis_label='Jumlah Imigran')

# Hilangkan logo bokeh dari sidebar
a.toolbar.logo = None

# Pembuatan diagram garis
a.line(x='Tahun', y='Jumlah_Imigran', 
        color='blue', legend_label='Jumlah Imigran',
        source=source)
a.legend.location = 'top_left'

# Pembuatan hover
hov_appl = a.circle(x='Tahun', y='Jumlah_Imigran', source=source ,size=15, alpha=0, hover_fill_color='blue', hover_alpha=0.5)
tooltips = [
            ('Tahun', '@Tahun'),
            ('Jumlah Imigran', '@Jumlah_Imigran'),
           ]
a.add_tools(HoverTool(tooltips=tooltips, renderers=[hov_appl]))

# Pembauatan vertical PanTool
a.add_tools(PanTool(dimensions='height'))

# Pembuatan horizontal PanTool
a.add_tools(PanTool(dimensions='width'))

curdoc().add_root(a)
