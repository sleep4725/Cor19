from pyecharts.charts import Bar
import altair as alt
import pandas as pd

class ECharts():

    @classmethod
    def barCharts(cls, datas):
        bar_ = Bar()
        bar_._use_theme()
        # x축
        xAxis = [i["national"] for i in datas]
        # y축
        yAxis = [i["confirmer"] for i in datas]
        bar_.add_xaxis(xaxis_data=xAxis)
        bar_.add_yaxis(y_axis=yAxis, series_name="die", color="blue")
        bar_.render()

    @classmethod
    def barGraph(cls, datas):
        data = pd.DataFrame(
            {
                "국가"  : [i["national" ] for i in datas],
                "확진자": [i["confirmer"] for i in datas]
            }
        )

        bar = alt.Chart(data).mark_bar().encode(x='국가', y='확진자')
        bar.save("test.html")