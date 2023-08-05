#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
import seaborn as sns

from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval
from digitallab.evaluation.plots.aggregate_plot_skeleton import x_aggregate_plot_skeleton


def ecdf_plot_class(DatabaseCollector):
    class ECDFPlot(x_aggregate_plot_skeleton(DatabaseCollector)):
        def __init__(self, data_retrieval: DataRetrieval):
            super().__init__(data_retrieval)

        def build_axes_without_grid(self):
            super().collect()
            sns.set(style="whitegrid", palette="colorblind", font_scale=self.font_scale)

            ax = sns.ecdfplot(self.data, x=self._xaxis, hue=self._methods_key_print_label,
                              hue_order=self._names_of_comparison_units)

            super()._decorate_axis(ax)

            self.build_legend_for_non_grid(ax)

        def build_axes_with_grid(self):
            super().collect()
            sns.set(style="whitegrid", palette="colorblind", font_scale=self.font_scale)

            facet_grid = sns.FacetGrid(self.data,
                                       col=self._grid_col_key if self._grid_col_label is None else self._grid_col_label,
                                       row=self._grid_row_key if self._grid_row_label is None else self._grid_row_label,
                                       hue=self._methods_key_print_label,
                                       legend_out=True,
                                       sharex=self._sharex,
                                       sharey=self._sharey)
            facet_grid.map(sns.ecdfplot, self._xaxis)
            for axis in np.nditer(facet_grid.axes, flags=["refs_ok"]):
                axis.item().set_xlabel(self._xaxis_label)
            facet_grid.add_legend()

    return ECDFPlot
