#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Wrapper modules to display matplotlib plots."""

__name__    = 'qom.ui.figure'
__authors__ = ['Sampreet Kalita']
__created__ = '2020-06-16'
__updated__ = '2020-09-17'

# dependencies
from matplotlib.lines import Line2D
import logging
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# module logger
logger = logging.getLogger(__name__)

class Plotter2D():
    """Class containing various 2D plot scenarios.

    Attibutes
    ---------
    axes : :class:`matplotlib.axes.Axes`
        Axes for the figure.

    cbar : :class:`matplotlib.colorbar.Colorbar`
        Colorbar for 2D color figures.

    head : :class:`matplotlib.lines.Line2D`
        Line to indicate the point of processing.

    plot : :class:`matplotlib.*`
        Variable plot classes depending on the type of figure.

    plot_type : str
        Type of plot:
            contour: Contour plot.
            contourf: Filled contour plot.
            line: Line plot.
            lines: Multi-line plot.
            pcolormesh: Color plot.
            scatter: Scatter plot.
            scatters: Multi-scatter plot.
    """

    # class attributes
    axes = None
    cbar = None
    head = None
    plot = None
    plot_type = 'line'

    def __init__(self, plot_params, X=None, Y=None, Z=None):
        """Class constructor for Plotter2D.
        
        Args:
            plot_params (list): Parameters of the plot.
            X (:class:`qom.utils.axis.StaticAxis`): X-axis data.
            Y (:class:`qom.utils.axis.StaticAxis`): Y-axis data.
            Z (:class:`qom.utils.axis.StaticAxis`): Z-axis data.
        """
        
        # initialize plot
        plt.show()
        self.axes = plt.gca()
        self.axes.set_xlim(X.values[0], X.values[-1])

        # plot type
        self.plot_type = plot_params['type']

        # if line plot
        if self.plot_type == 'line':
            self.plot = Line2D([], [], color=plot_params['color'], linestyle=plot_params['linestyle'])
            self.head = Line2D([], [], color=plot_params['color'], linestyle=plot_params['linestyle'], marker='o')
            self.axes.add_line(self.plot)
            self.axes.add_line(self.head)

        # if multi-line plot
        if self.plot_type == 'lines':
            self.plot = [Line2D([], [], color=Z.colors[i], linestyle=Z.linestyles[i]) for i in range(len(Z.values))]
            self.head = [Line2D([], [], color=Z.colors[i], linestyle=Z.linestyles[i], marker='o') for i in range(len(Z.values))]
            [self.axes.add_line(self.plot[i]) for i in range(len(Z.values))]
            [self.axes.add_line(self.head[i]) for i in range(len(Z.values))]
            plt.legend(Z.legends, loc='best')

        # if scatter plot
        if self.plot_type == 'scatter':
            self.plot = self.axes.scatter([], [], s=plot_params['size'], c=plot_params['color'])

        # TODO: handle multi-scatter
            
        # if pcolormesh plot
        if self.plot_type == 'pcolormesh':
            self.axes.set_ylim(Y.values[0], Y.values[-1])

            mX, mY = np.meshgrid(X.values, Y.values)
            if 'color_grad' in plot_params:
                if plot_params['color_grad'] == 'br_light':
                    cmap = sns.diverging_palette(250, 15, s=75, l=40, n=9, center='light', as_cmap=True)
                if plot_params['color_grad'] == 'rb_light':
                    cmap = sns.diverging_palette(15, 250, s=75, l=40, n=9, center='light', as_cmap=True)
                if plot_params['color_grad'] == 'gr_light':
                    cmap = sns.diverging_palette(150, 15, s=75, l=40, n=9, center='light', as_cmap=True)
            self.plot = self.axes.pcolormesh(mX, mY, Z.values, shading='gouraud', cmap=cmap)
            self.cbar = plt.colorbar(self.plot)

        # TODO: handle contour plots

        # setup plot
        self.set_params(plot_params)

    def set_params(self, plot_params):
        """Function to set plot parameters.
        
        Parameters
        ----------
        plot_params : list
            Parameters of the plot.
        """

        # font sizes
        plt.rcParams.update({'font.size': 12})
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        # legends
        if 'legend' in plot_params:
            if type(plot_params['legend']) == list:
                plot_params['legend'] = [r'' + ele for ele in plot_params['legend']]
            else:
                plot_params['legend'] = [r'' + plot_params['legend']]
            plt.legend(plot_params['legend'], loc='best')

        # title
        if 'title' in plot_params:
            plt.title(plot_params['title'])

        # labels
        if 'x_label' in plot_params:
            plt.xlabel(r'' + plot_params['x_label'], fontsize=16)
        if 'y_label' in plot_params:
            plt.ylabel(r'' + plot_params['y_label'], fontsize=16)

        # limits
        if 'x_lim' in plot_params:
            plt.xlim(plot_params['x_lim'][0], plot_params['x_lim'][1])
        if 'y_lim' in plot_params:
            plt.ylim(plot_params['y_lim'][0], plot_params['y_lim'][1])

        # ticks
        plt.ticklabel_format(axis='both', style='plain')

    def update(self, X=None, Y=None, Z=None, head=True, hold=False):
        """Function to update plot.
        
        Parameters
        ----------
        X : list
            X-axis data.
            
        Y : list
            Y-axis data.
            
        Z : list
            Z-axis data.

        head : boolean
            Option to display the head for line-type plots.

        hold : boolean
            Option to hold the plot.
        """

        if self.plot_type == 'line':
            self.plot.set_xdata(X.values)
            self.plot.set_ydata(Y.values)
            if head and len(X.values) != X.size:
                self.head.set_xdata(X.values[-1:])
                self.head.set_ydata(Y.values[-1:])
            else:
                self.head.set_xdata([])
                self.head.set_ydata([])
            # handle NaN values
            temp = [y if y == y else 0 for y in Y.values]
            self.axes.set_ylim(min(Y.values), max(Y.values))
                
        if self.plot_type == 'lines':
            minis = []
            maxis = []
            num = len(Y.values)
            for j in range(num):
                self.plot[j].set_xdata(X.values[j])
                self.plot[j].set_ydata(Y.values[j])
                if head and len(X.values[j]) != X.size[1] and len(X.values[j]) != 0:
                    self.head[j].set_xdata(X.values[j][-1:])
                    self.head[j].set_ydata(Y.values[j][-1:])
                else:
                    self.head[j].set_xdata([])
                    self.head[j].set_ydata([])
                # calculate minimum and maximum values
                if len(Y.values[j]) != 0:
                    # handle NaN values
                    temp = [y if y == y else 0 for y in Y.values[j]]
                    minis.append(min(temp))
                    maxis.append(max(temp))
            self.axes.set_ylim(min(minis), max(maxis))

        if self.plot_type == 'scatter':
            XY = np.c_[X.values, Y.values]
            self.plot.set_offsets(XY)
            # handle NaN values
            temp = [y if y == y else 0 for y in Y.values]
            self.axes.set_ylim(min(Y.values), max(Y.values))
        
        if self.plot_type == 'pcolormesh':
            rave = np.ravel(Z.values)
            self.plot.set_array(rave)
            # handle NaN values
            temp = [z if z == z else 0 for z in rave]
            self.plot.set_clim(vmin=min(temp), vmax=max(temp))
            self.cbar.set_ticks(np.linspace(min(temp), max(temp), 11))
            self.cbar.ax.set_autoscale_on(True)
            self.cbar.draw_all()

        # draw data
        plt.draw()

        # display plot
        if hold:
            plt.show()
        else:
            plt.pause(1e-9)