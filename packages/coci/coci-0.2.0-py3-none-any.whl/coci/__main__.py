import os
import sys
import pickle
import numpy as np
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def progress_bar(barname, rate):
    '''
    :param barname:
    :param rate:
    :return:
    '''
    num = int(rate/0.05) + 1
    bar = ('#' * num).ljust(20, '-')
    sys.stdout.write(f'\r{barname} : [{bar}] {rate*100:.2f}%')

def get_sensitivity_ranges(x, split_num):
    '''

    :param x:
    :param split_num:
    :return:
    '''

    min_x = x.min(axis=0)
    max_x = x.max(axis=0)

    minmax = np.vstack([min_x, max_x]).T

    sensitivity_ranges = []

    len_x = x.shape[1]
    cnt = 1

    for row in minmax:

        progress_bar("Loading sensitivity ranges: {}/{}".format(cnt, len_x), cnt/len_x)
        cnt += 1

        min_ = row[0]
        max_ = row[1]

        sensitivity_ranges.append(np.linspace(min_, max_, num=split_num))

    print()

    return sensitivity_ranges


class TreeExplainer():

    def __init__(self, model):
        '''

        :param model:
        '''

        self._model = model

        self.palette = sns.diverging_palette(255, 0, sep=1, n=3)
        self.cmap = sns.diverging_palette(255, 0, as_cmap=True)

        self._x = None
        self._y = None
        self._sensitivities = None
        self._idx = None
        self._sample_size = None

        self.feature_names = None


    def sensitivity(self, x, feature_names=None, split_num=2, sample_size=None):
        '''

        :param x:
        :param feature_names:
        :param split_num:
        :param sample_size:
        :return:
        '''

        self._split_num = split_num

        if sample_size is None:
            if len(x) <= 900:
                self._sample_size = len(x)
            else:
                self._sample_size = 900
        else:
            self._sample_size = sample_size

        idx = np.random.permutation(len(x))[:int(self._sample_size/self._split_num)]

        self._x = x[idx]

        if feature_names is not None:
            assert x.shape[1] == len(feature_names), "feature_name has different length from x features length"
            self.feature_names = feature_names
        else:
            self.feature_names = np.arange(x.shape[1])

        self._y = self._model.predict(self._x)

        self.sensitivity_ranges = get_sensitivity_ranges(self._x, self._split_num)

        self.sensitivity_analysis()

    def sensitivity_analysis(self):
        '''

        :return:
        '''

        _sensitivities = []

        cnt = 1
        len_x = self._x.shape[1]

        for col in range(len_x):

            if len(self.sensitivity_ranges[col]) != 0:

                progress_bar("Analyzing sensitivity: {}/{}".format(cnt, len_x), cnt / len_x)
                cnt += 1

                lis_x = []
                lis_y = []

                importance = self._model.feature_importance()

                if importance[col] == 0:
                    pass
                else:
                    for sr in self.sensitivity_ranges[col]:
                        tmp_x = self._x.copy()

                        delta_x = sr - tmp_x[:, col]

                        tmp_x[:, col] = sr

                        delta_y = self._model.predict(tmp_x) - self._y

                        lis_x += list(delta_x)
                        lis_y += list(delta_y)

                _sensitivities.append(np.array([lis_x, lis_y]))

        # sort by mean delta y
        y_mean = np.array([abs(s[1]).mean() for s in _sensitivities])
        y_mean[np.isnan(y_mean)] = 0

        self.idx = y_mean.argsort()[::-1]
        self._sensitivities = _sensitivities

    def summary_plot(self, max_display=10):
        '''

        :param max_display:
        :return:
        '''

        if max_display is None:
            max_display = len(self.idx)

        fig, ax = plt.subplots(figsize=(10, max_display * 3))

        x = []
        y = []
        hue = []

        for id_ in self.idx[:max_display]:

            s = self._sensitivities[id_]

            hue_norm = ((s[0] + abs(s[0].min())) / (s[0].max() + abs(s[0].min()))) - 0.5

            x += list(s[1].astype('float'))
            y += list(np.full(len(s[1]), fill_value=self.feature_names[id_] + str(hue_norm.max()) + ' ' + str(hue_norm.min())))
            hue += list(hue_norm)

        sns.swarmplot(
            x=x, y=y,
            hue=hue,
            palette=self.palette,
        )

        fig.set_size_inches(10, max_display)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ## create colorbar ##
        plt.legend('')
        divider = make_axes_locatable(plt.gca())
        ax_cb = divider.new_horizontal(size="1%", pad=0.05)
        fig.add_axes(ax_cb)
        cb1 = matplotlib.colorbar.ColorbarBase(ax_cb, cmap=self.cmap, ticks=[0, 1], orientation='vertical')
        cb1.ax.set_yticklabels(['Low', 'High'])
        cb1.set_label('Feature Value Changes')
        plt.show()























