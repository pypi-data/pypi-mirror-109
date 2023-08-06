#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc

from digitallab.evaluation.data_processing.all_experiments_database_collector import AllExperimentsDatabaseCollector
from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval
from digitallab.evaluation.plots.plot_skeleton import PlotSkeleton


def aggregate_plot_skeleton_class(DatabaseCollector):
    class AggregatePlotSkeleton(PlotSkeleton, DatabaseCollector, abc.ABC):
        def __init__(self, data_retrieval: DataRetrieval):
            PlotSkeleton.__init__(self)
            DatabaseCollector.__init__(self, data_retrieval)
            self._names_of_comparison_units = []

        @abc.abstractmethod
        def build_axes_with_grid(self):
            pass

        @abc.abstractmethod
        def build_axes_without_grid(self):
            pass

        def build_legend_for_non_grid(self, axes):
            if self._legend_is_hidden:
                axes.legend('', frameon=False)
            else:
                legend_handles = axes.get_legend().legendHandles
                axes.legend(legend_handles, self._names_of_comparison_units, bbox_to_anchor=(1.05, 1), loc=2,
                            borderaxespad=0.)

        def build_legend_for_grid(self, axes):
            pass

        def collect(self):
            DatabaseCollector.collect(self)
            rename_dict = dict()
            rename_dict[self._methods_key] = self._methods_key_print_label
            if self._grid_row_label is not None:
                rename_dict[self._grid_row_key] = self._grid_row_label
            if self._grid_col_label is not None:
                rename_dict[self._grid_col_key] = self._grid_col_label
            self.data.rename(columns=rename_dict, inplace=True)

            return self.data

    return AggregatePlotSkeleton


def y_aggregate_plot_skeleton_class(DatabaseCollector):
    class YAggregatePlotSkeleton(aggregate_plot_skeleton_class(DatabaseCollector), abc.ABC):
        def __init__(self, data_retrieval: DataRetrieval):
            super().__init__(data_retrieval)
            self._yaxis = None

        def set_yaxis(self, key, label):
            self._yaxis = key
            self._yaxis_label = label
            return self

        def set_value_of_interest(self, key, y_axis_label):
            self.set_yaxis(key, y_axis_label)
            return self

        def _assert(self):
            assert self._yaxis and self._yaxis_label, "You have to call 'set_yaxis' or " \
                                                      "'set_value_of_interest' before calling 'process'."

        def collect(self):
            self._assert()
            super().collect()

            return self.data

        @abc.abstractmethod
        def build_axes_without_grid(self):
            pass

    return YAggregatePlotSkeleton


def x_aggregate_plot_skeleton(DatabaseCollector):
    class XAggregatePlotSkeleton(aggregate_plot_skeleton_class(DatabaseCollector), abc.ABC):
        def __init__(self, data_retrieval: DataRetrieval):
            super().__init__(data_retrieval)
            self._xaxis = None

        def set_xaxis(self, key, label):
            self._xaxis = key
            self._xaxis_label = label
            return self

        def set_value_of_interest(self, key, x_axis_label):
            self.set_xaxis(key, x_axis_label)
            return self

        def _assert(self):
            assert self._xaxis and self._xaxis_label, "You have to call 'set_yaxis' or " \
                                                      "'set_value_of_interest' before calling 'process'."

        def collect(self):
            self._assert()
            super().collect()

            return self.data

        @abc.abstractmethod
        def build_axes_without_grid(self):
            pass

    return XAggregatePlotSkeleton


def xy_aggregate_plot_skeleton(DatabaseCollector):
    class XYAggregatePlotSkeleton(y_aggregate_plot_skeleton_class(DatabaseCollector), abc.ABC):
        def __init__(self, data_retrieval: DataRetrieval):
            super().__init__(data_retrieval)
            self._xaxis = None

        def _assert(self):
            assert self._xaxis and self._xaxis_label, "You have to call 'set_xaxis' before calling 'process'."

        def set_xaxis(self, key, label):
            self._xaxis = key
            self._xaxis_label = label
            return self

        def set_value_of_interest(self, key, axis_label, axis: str = "y"):
            if axis == "x":
                return self.set_xaxis(key, axis_label)
            elif axis == "y":
                return super().set_value_of_interest(key, axis_label)
            else:
                assert isinstance(axis, str), "The parameter 'axis' must be a string."
                raise KeyError("The value " + axis + " is not supported for 'axis'.")

        def collect(self):
            self._assert()
            super().collect()

            return self.data

        @abc.abstractmethod
        def build_axes_without_grid(self):
            pass

    return XYAggregatePlotSkeleton
