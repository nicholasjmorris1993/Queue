import re
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot


def production(times, stations):
    line = Production()
    line.work(times, stations)
    line.plots()

    return line

class Production:
    def work(self, times, stations):
        # initialize the work stations
        workers = list()
        for _ in range(stations):
            if len(times) > 0:
                workers.append(times.pop(0))

        # send the work through the stations
        workers = np.array(workers)
        cycle_times = list()
        cycle_time = 0
        self.total_time = 0
        working = True
        while working:
            self.total_time += 1
            cycle_time += 1
            workers -= 1
            complete = np.where(workers <= 0)[0]
            for idx in complete:
                if len(times) > 0:
                    workers[idx] = times.pop(0)
                    cycle_times.append(cycle_time)
                    cycle_time = 0
            working = np.any(workers > 0)

        # save the cycle times
        self.cycle_time = pd.DataFrame({
            "Output": np.arange(len(cycle_times)) + 1,
            "Cycle Time": cycle_times,
        })

    def plots(self):
        # plot the cycle times
        self.histogram(
            self.cycle_time, 
            x="Cycle Time", 
            bins=20, 
            title="Histogram On Cycle Time", 
            font_size=16,
        )

    def histogram(self, df, x, bins=20, vlines=None, title="Histogram", font_size=None):
        bin_size = (df[x].max() - df[x].min()) / bins
        fig = px.histogram(df, x=x, title=title)
        if vlines is not None:
            for line in vlines:
                fig.add_vline(x=line)
        fig.update_traces(xbins=dict( # bins used for histogram
                size=bin_size,
            ))
        fig.update_layout(font=dict(size=font_size))
        title = re.sub("[^A-Za-z0-9]+", "", title)
        plot(fig, filename=f"{title}.html")
