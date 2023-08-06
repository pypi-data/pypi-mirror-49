"""This module provides out-of-the box plots to analyse models whee titles, axes labels, additional information is automatically 
added to the resuling figures from the information stored in the repository. 
"""

import logging
import numpy as np
import pandas as pd
import pailab.analysis.plot_helper as plot_helper  # pylint: disable=E0611
from pailab.ml_repo.repo_store import RepoStore, LAST_VERSION
from pailab.ml_repo.repo import NamingConventions, MLObjectType  # pylint: disable=E0611,E0401
from pailab import RepoInfoKey

has_plotly = True
try:
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    from plotly import tools
    import plotly.graph_objs as go
except ImportError:
    has_plotly = False

logger = logging.getLogger(__name__)

init_notebook_mode(connected=True)


def measure_by_parameter(ml_repo, measure_name, param_name, data_versions=None, training_param=False):
    '''[summary]

    Args:
        :param ml_repo ([type]): [description]
        :param measure_name ([type]): [description]
        :param param_name ([type]): [description]
        :param data_versions ([type], optional): Defaults to None. [description]
        :param training_parm (bool, optional): If True, training parameters are used otherwise model parameter (default is False)
    '''

    x = plot_helper.get_measure_by_parameter(
        ml_repo, measure_name, param_name, data_versions, training_param)
    data = []
    model_label_annotations = []
    for k, measures in x.items():
        data_name = str(NamingConventions.Data(
            NamingConventions.EvalData(NamingConventions.Measure(measure_name))))
        data_versions = set()

        for measure in measures:
            data_versions.add(measure['data_version'])
            if 'model_label' in measure:
                model_label_annotations.append(dict(x=measure[param_name], y=measure['value'], xref='x', yref='y', text=measure['model_label'],
                                                    showarrow=True,
                                                    arrowhead=2,
                                                    # ax=0,
                                                    # ay=-30
                                                    ))
        measures = pd.DataFrame(measures)
        for d_version in data_versions:
            # if True:
            df = measures.loc[measures['data_version'] == d_version]
            text = ["model version: " + str(x['model_version']) + '<br>' +
                    data_name + ': ' + str(x['data_version']) + '<br>'
                    + 'train_data: ' + str(x['train_data_version'])
                    for index, x in df.iterrows()]

            if True:  # len(x) > 1:
                plot_name = k + ': ' + str(d_version)
            # else:
            #    plot_name = data_name + ': ' + str(d_version)
            data.append(
                go.Scatter(
                    x=df[param_name],
                    y=df['value'],
                    text=text,
                    name=plot_name,
                    mode='markers'
                )

            )

    layout = go.Layout(
        title='measure by parameter',
        annotations=model_label_annotations,
        xaxis=dict(title=param_name),
        yaxis=dict(title=NamingConventions.Measure(
            measure_name).values['measure_type'])
    )
    # IPython notebook
    # py.iplot(data, filename='pandas/basic-line-plot')
    fig = go.Figure(data=data, layout=layout)
    #return fig
    iplot(fig)  # , filename='pandas/basic-line-plot')


def projection(ml_repo, left, right, n_steps = 100, model = None, labels = None,  output_index = None, direction = None):
    logger.info('Start projection with ' + str(n_steps) + ' steps.')
    x = plot_helper.project(ml_repo, model, labels, left, right, output_index=output_index, n_steps= n_steps)
    training = ml_repo.get_names(MLObjectType.TRAINING_DATA) #use training data to get output name
    output_name = ml_repo.get(training[0]).y_coord_names[0]
    data = []
    x_data = [0.0 + float(i)/float(n_steps-1) for i in range(n_steps) ]
    for k,v in x.items():
        data.append(
                    go.Scatter(
                        x=x_data,
                        y=v,
                        name=k
                    )
        )
    layout = go.Layout(
        title='projection',
        xaxis=dict(title='steps'),
        yaxis=dict(title=output_name)
    )
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

def measure_history(ml_repo, measure_name):

    x = plot_helper.get_measure_history(
        ml_repo, measure_name)
    data = []
    model_label_annotations = []
    for k, measures in x.items():
        data_name = str(NamingConventions.Data(
            NamingConventions.EvalData(NamingConventions.Measure(measure_name))))
        data_versions = set()

        for measure in measures:
            data_versions.add(measure['data_version'])
            if 'model_label' in measure:
                model_label_annotations.append(dict(x=str(measure['datetime']), y=measure['value'], xref='x', yref='y', text=measure['model_label'],
                                                    showarrow=True,
                                                    arrowhead=2,  # 1
                                                    # ax=,
                                                    # ay=-30
                                                    ))
        measures = pd.DataFrame(measures)
        for d_version in data_versions:
            # if True:
            df = measures.loc[measures['data_version'] == d_version]
            text = ["model version: " + str(x['model_version']) + '<br>' +
                    data_name + ': ' + str(x['data_version']) + '<br>'
                    + 'train_data: ' + str(x['train_data_version'])
                    for index, x in df.iterrows()]

            if True:  # len(x) > 1:
                plot_name = k + ': ' + str(d_version)
            # else:
            #    plot_name = data_name + ': ' + str(d_version)
            data.append(
                go.Scatter(
                    x=df['datetime'],
                    y=df['value'],
                    text=text,
                    name=plot_name,
                    mode='markers'
                )
            )

    layout = go.Layout(
        title='measure history',
        annotations=model_label_annotations,
        xaxis=dict(title='t'),
        yaxis=dict(title=NamingConventions.Measure(
            measure_name).values['measure_type'])
    )
    # IPython notebook
    # py.iplot(data, filename='pandas/basic-line-plot')
    fig = go.Figure(data=data, layout=layout)

    iplot(fig)  # , filename='pandas/basic-line-plot')


def _histogram(plot_dict, n_bins = None, histnorm = 'percent'):
    layout = go.Layout(
        title=plot_dict['title'],
        xaxis=dict(title=plot_dict['x0_name']),
        barmode='overlay'
    )
    plot_data = []
    opacity = 1.0
    if len(plot_dict['data'].keys()) > 1:
        opacity = 0.5
    for k, x in plot_dict['data'].items():
        text = ''
        for l, w in x['info'].items():
            text += l + ':' + str(w) + '<br>'
        if 'label' in x.keys():
            k = x['label'] + ', ' + k
        if n_bins is None:
            plot_data.append(go.Histogram(x=x['x0'],
                                        text=text,
                                        name=k,
                                        opacity=opacity,
                                        histnorm=histnorm))
        else:
            plot_data.append(go.Histogram(x=x['x0'],
                                        text=text,
                                        name=k,
                                        opacity=opacity, 
                                        nbinsx = n_bins,
                                        histnorm=histnorm))
                                        
    fig = go.Figure(data=plot_data, layout=layout)

    iplot(fig)  # , filename='pandas/basic-line-plot')


def histogram_model_error(ml_repo, models, data_name, y_coordinate=None, data_version=LAST_VERSION, n_bins = None,  start_index = 0, end_index = -1):
    """Plot histogram of differences between predicted and real values.

    The method plots histograms between predicted and real values of a certain target variable for reference data and models. 
    The reference data is described by the data name and the version of the data (as well as the targt variables name). The models can be described
    by 
    - a dictionary of model names to versions (a single version number, a range of versions or a list of versions)
    - just a model name (in this case the latest version is used)

    Args:
        :param ml_repo ([type]): [description]
        :param models ([type]): [description]
        :param data_name (str or list of str): [description]
        :param y_coordinate ([type], optional): Defaults to None. [description]
        :param data_version ([type], optional): Defaults to LAST_VERSION. [description]

    Examples:
        Plot histograms for errors in the variable mickey_mouse on the dataset my_test_data for the latest version of model_1 and all versions of model_2. 

        >>> histogram_model_error(repo, models = {'model_1': ['latest'], 'model_2': ('first','latest')}, 
            data_name = 'my_test_data', y_coordinate='mickey_mouse')

        Plot histogram for error of latest version of model_2 on the latest version of my_test_data. Note that the plot would be empty if the latest version of model_2
        has not yet been evaluated on the latest version of my_test_data.

        >>> histogram_model_error(repo, models = 'model_2', data_name = 'my_test_data', y_coordinate='mickey_mouse')


    """

    plot_dict = plot_helper.get_pointwise_model_errors(
        ml_repo, models, data_name, y_coordinate, start_index=start_index, end_index=end_index)
    _histogram(plot_dict, n_bins)


def scatter_model_error(ml_repo, models, data_name, x_coordinate, y_coordinate=None, start_index = 0, end_index = -1):
    '''[summary]

    Args:
        :param ml_repo ([type]): [description]
        :param models ([type]): [description]
        :param data_name ([type]): [description]
        :param x_coordinate ([type]): [description]
        :param y_coordinate ([type], optional): Defaults to None. [description]
        :param data_version ([type], optional): Defaults to LAST_VERSION. [description]
    '''

    plot_dict = plot_helper.get_pointwise_model_errors(
        ml_repo, models, data_name, y_coordinate, x_coord_name=x_coordinate, start_index=start_index, end_index=end_index)

    layout = go.Layout(
        title=plot_dict['title'],
        xaxis=dict(title=plot_dict['x0_name']),
        yaxis=dict(title=plot_dict['x1_name'])
    )
    plot_data = []
    for k, x in plot_dict['data'].items():
        text = ''
        for l, w in x['info'].items():
            text += l + ':' + str(w) + '<br>'
        if 'label' in x.keys():
            k = x['label'] + ', ' + k
        plot_data.append(go.Scatter(x=x['x0'],
                                    y=x['x1'],
                                    text=text,
                                    name=k,
                                    mode='markers'))

    # IPython notebook
    # py.iplot(data, filename='pandas/basic-line-plot')
    fig = go.Figure(data=plot_data, layout=layout)

    iplot(fig)  # , filename='pandas/basic-line-plot')


def histogram_data(ml_repo, data, x_coordinate, y_coordinate=None, n_bins = None,  start_index = 0, end_index = -1):
    '''[summary]

    Args:
        ml_repo ([type]): [description]
        data ([type]): [description]
        x_coordinate ([type]): Defaults to None. [description]
        y_coordinate ([type], optional): Defaults to None. [description]

    Raises:
        Exception: [description]
    '''
    plot_dict = plot_helper.get_data(ml_repo, data, x_coordinate, start_index=start_index, end_index=end_index)
    _histogram(plot_dict, n_bins=n_bins)

def histogram_data_conditional_error(ml_repo, models, data, x_coordinate, y_coordinate = None,  
                                    start_index = 0, end_index = -1, percentile = 0.1, n_bins = None):
    """Plots the distribution of input data along a given axis for the largest absolute pointwise errors in comparison to the distribution of all data.
    
    Args:
        ml_repo (MLRepo): repository
        models (str, list of str): definition of latest model/models used for plotting beneath the labeled models
        data (str): name of dataset used for plotting
        x_coordinate (str): name of x coordinate for which the distribution will be plotted
        y_coordinate (str, optional): Name of y-coordinate for which the error is determined. Defaults to None (use first y-coordinate).
        start_index (int, optional): Defaults to 0. Startindex of data.
        end_index (int, optional): Defaults to -1. Endindex of data.
        percentile (float, optional): Defaults to 0.1. Percentage of largest absolute errors used.
        n_bins ([type], optional): Defaults to None. Number of bin of histogram.
    """

    tmp = plot_helper.get_pointwise_model_errors(
        ml_repo, models, data, y_coordinate, x_coord_name=x_coordinate, start_index = 0, end_index = -1)
    
    plot_data = {}
    for k,x in tmp['data'].items():
        abs_err = np.abs(x['x1'])
        sorted_indices = np.argsort(abs_err)
        i_start = int( (1.0-percentile)*len(sorted_indices))
        indices = sorted_indices[i_start:]
        data = {'x0': x['x0'][indices], 'info': x['info']}
        if 'label' in x.keys():
            plot_data[x['label']+':'+str(percentile)] = data
            plot_data[x['label']] = {'x0': x['x0'][start_index:end_index], 'info': x['info']}
        else:
            plot_data[k+':'+str(percentile)] = data
            plot_data[k] = {'x0': x['x0'][start_index:end_index], 'info': x['info']}
    plot_dict = {'data': plot_data, 'title': '', 'x0_name':x_coordinate}
    _histogram(plot_dict, n_bins=n_bins)

def _ice_plotly(ice_results, ice_points = None, height = None, width = None, ice_results_2 = None, clusters = None):
    data = []
    if ice_points is None:
        ice_points = range(ice_results.ice.shape[0])
    if clusters is not None:
        ice_points_tmp = []
        for i in ice_points:
            if ice_results.labels[i] in clusters:
                ice_points_tmp.append(i)
        _ice_plotly(ice_results, ice_points=ice_points_tmp, ice_results_2 = ice_results_2, height=height, width=width)
        return

    # plot ice curves
    for i in ice_points:
        data.append(go.Scatter(x=ice_results.x_values, y = ice_results.ice[i,:], name = ice_results.data_name + '[' + str(ice_results.start_index +i) + ',:]'))
        if ice_results_2 is not None:
            data.append(go.Scatter(x=ice_results_2.x_values, y = ice_results_2.ice[i,:], name = 'model2, ' + ice_results.data_name + '[' + str(ice_results.start_index +i) + ',:]'))
    layout = go.Layout(
        title='ICE, model: ' + ice_results.model + ', version: ' + ice_results.model_version,
        xaxis=dict(title=ice_results.x_coord_name),
        yaxis=dict(title=ice_results.y_coord_name),
        height = height,
        width = width
    )
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)  # , filename='pandas/basic-line-plot')


def _ice_clusters_plotly(ice_results, height = None, width = None, ice_results_2= None, clusters = None):
    data = []
    if clusters is None:
        clusters = range(ice_results.cluster_centers.shape[0])
    # plot ice cluster curves
    for i in clusters:
        data.append(go.Scatter(x=ice_results.x_values, y = ice_results.cluster_centers[i,:], name = 'cluster ' + str(i)))
    if ice_results_2 is not None:
        cluster_averages = ice_results.compute_cluster_average(ice_results_2)
        for i in clusters:
            data.append(go.Scatter(x=ice_results.x_values, y = cluster_averages[i,:], name = 'average ' + str(i)))

    layout = go.Layout(
        title='ICE clusters, model: ' + ice_results.model + ', version: ' + ice_results.model_version,
        xaxis=dict(title=ice_results.x_coord_name),
        yaxis=dict(title=ice_results.y_coord_name),
        height = height,
        width = width
    )
    #fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('Plot 1', 'Plot 2',
    #                                                      'Plot 3', 'Plot 4'))#, layout = layout)
    #fig['layout'].update(title='ICE, model: ' + ice_results.model + ', version: ' + ice_results.model_version, xaxis=dict(title=ice_results.x_coord_name),
    #    yaxis=dict(title=ice_results.y_coord_name),
    #    height = height,
    #    width = width)
    fig = go.Figure(data=data, layout=layout)
    #fig.append_trace(data,1,1)
    iplot(fig)  # , filename='pandas/basic-line-plot')


def ice(ice_results, height = None, width = None, ice_points = None, ice_results_2 = None, clusters = None):
    if ice_results_2 is not None:
        ice_results._validate_for_comparison(ice_results_2)
    if has_plotly:
        _ice_plotly(ice_results, height=height, width=width, ice_points = ice_points, ice_results_2 = ice_results_2, clusters = clusters)
    else:
        raise Exception("Plot methods for matplotlib have not yet been implemented.")
     
def ice_clusters(ice_results, height = None, width = None, ice_results_2 = None, clusters = None):
    """Plot the cluster centers from functional clustering of ICE curves.
    
    Args:
        ice_results (ICE_Result): Result from calling the method interpretation.compute_ice with functional clustering.
        height (int, optional): Height of resulting figure. Defaults to None.
        width (int, optional): Width of resulting figures. Defaults to None.
        ice_results_2 (ICE_Result, optional): Result from an ICE computation for a different model (version). Here, the result does not need to contain functional clustering.
            If specified, the ICE curves in this result are clustered according to the clustering of the other results. Defaults to None.
        clusters (iterable of int): Defines the clusters that will be plot. If None, all clusters will be plot. Default to None.

    Raises:
        Exception: If ice_results_2 was computed on a different data (version) or with different start_index, and exception is thrown.
    """
    if ice_results.cluster_centers is None:
        raise Exception('No clusters have yet been computed. Call compute_ice with clusering_param to compute clusters.')

    if has_plotly:
        _ice_clusters_plotly(ice_results, height=height, width=width, ice_results_2=ice_results_2, clusters = clusters)
    else:
        raise Exception("Plot methods for matplotlib have not yet been implemented.")
    
def ice_diff(ice_results, ice_results_2, n_curves=10, ord = 2, height = None, width = None):
    """[summary]
    
    Args:
        ice_results ([type]): [description]
        ice_results_2 ([type]): [description]
        n_curves (int, optional): [description]. Defaults to 10.
        ord (int, optional): Defines the norm to be used to measure distance between two ICE curves, see numpy's valid strings for ord in linalg.norm [description]. Defaults to 2.
        
    """
    ice_results._validate_for_comparison(ice_results_2)
    if n_curves > ice_results.ice.shape[0]:
        raise Exception('Number of desired curves exceeds number of all curves.')
    tmp = ice_results.ice - ice_results_2.ice
    distance = np.linalg.norm(ice_results.ice - ice_results_2.ice, ord = ord, axis = 1)
    indices = [i for i in range(ice_results.ice.shape[0])]
    tmp = sorted(zip(distance, indices))
    ice_points = [tmp[i][1] for i in range(n_curves)]
    if has_plotly:
        _ice_plotly(ice_results, height=height, width=width, ice_points = ice_points, ice_results_2 = ice_results_2)
    else:
        raise Exception("Plot methods for matplotlib have not yet been implemented.")
    

