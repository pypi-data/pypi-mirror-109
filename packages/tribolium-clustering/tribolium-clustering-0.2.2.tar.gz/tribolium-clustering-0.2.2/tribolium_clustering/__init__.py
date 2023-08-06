# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:59:27 2021
Useful Functions all as a library
@author: ryans
"""
from skimage import io # for testing purposes

# 3D image processing----------------------------------------------------------
def resample_isotropic_nodownsample(image_3d,voxelsize_yzx):
    import numpy as np
    import pyclesperanto_prototype as cle
    # we need to select a powerful GPU for this
    cle.select_device("GTX")
    if voxelsize_yzx[2] == voxelsize_yzx[1]:
        voxelsize_yzx = np.array(voxelsize_yzx)
        norm_voxelsize = voxelsize_yzx/voxelsize_yzx[2]
        input_image = cle.push_zyx(image_3d)
        resampled_image = cle.resample(input_image, factor_x=norm_voxelsize[2], 
                                       factor_y=norm_voxelsize[1], factor_z=norm_voxelsize[0])
        image_array = cle.pull_zyx(resampled_image)
        return image_array

def workflow(image, number_of_dilations = 15, number_of_erosions = 9):
    import numpy as np
    import pyclesperanto_prototype as cle    

    gpu_input = cle.push(image)

    # Spot detection
    # After some noise removal/smoothing, we perform a local maximum detection

    # gaussian blur -> needs adjusting, maybe even other filters for preprocessing
    gpu_tophat = cle.top_hat_sphere(gpu_input,radius_x=7, radius_y=7, radius_z=7)
    gpu_blurred = cle.gaussian_blur(gpu_tophat, sigma_x=1, sigma_y=1, sigma_z=2) 
    gpu_input = None
    # detect maxima: instead of a pointslist we get and image with white pixels at the maxima locations
    gpu_detected_maxima = cle.detect_maxima_box(gpu_blurred)
    gpu_tophat = None
    # Spot curation
    # Now, we remove spots with values below a certain intensity and label the remaining spots

    # threshold
    gpu_thresholded = cle.threshold_otsu(gpu_blurred)
    gpu_blurred = None

    # mask
    gpu_masked_spots = cle.mask(gpu_detected_maxima, gpu_thresholded)
    gpu_detected_maxima = None
    gpu_thresholded = None
    # label spots
    gpu_labelled_spots = cle.connected_components_labeling_box(gpu_masked_spots)
    gpu_masked_spots = None
    
    number_of_spots = cle.maximum_of_all_pixels(gpu_labelled_spots)
    print("Number of detected spots: " + str(number_of_spots))
    # retrieve the image to take a look at the maxima in napari
    # label map closing

    flip = cle.create_like(gpu_labelled_spots)
    flop = cle.create_like(gpu_labelled_spots)
    flag = cle.create([1,1,1])
    cle.copy(gpu_labelled_spots, flip)

    for i in range (0, number_of_dilations) :
        cle.onlyzero_overwrite_maximum_box(flip, flag, flop)
        cle.onlyzero_overwrite_maximum_diamond(flop, flag, flip)
    
    gpu_labelled_spots = None
    
    flap = cle.greater_constant(flip, constant= 1)

    for i in range(0, number_of_erosions):
        cle.erode_box(flap, flop)
        cle.erode_sphere(flop, flap)

    gpu_labels = cle.mask(flip, flap)
    flip = None
    flop = None
    flap = None
    flag = None
    
    alllabels = cle.close_index_gaps_in_label_map(gpu_labels)
    gpu_labels = None
    
    labels3d = only3dlabels(alllabels, image)
    alllabels = None
    
    output = cle.pull(labels3d)
    print('Label Numbering Starts at {val}'.format(val = np.min(output[np.nonzero(output)])))
    print('Workflow Completed')
    return output, labels3d

def only3dlabels(gpu_label_image,original_image):
    import pyclesperanto_prototype as cle
    import numpy as np
    
    cleregionprops = cle.statistics_of_background_and_labelled_pixels(original_image, gpu_label_image)

    bboxheight = cleregionprops['bbox_height']
    bboxwidth = cleregionprops['bbox_width']
    bboxdepth = cleregionprops['bbox_depth']
    bboxdiffx = cleregionprops['bbox_max_x'] - cleregionprops['bbox_min_x']
    bboxdiffy = cleregionprops['bbox_max_y'] - cleregionprops['bbox_min_y']
    bboxdiffz = cleregionprops['bbox_max_z'] - cleregionprops['bbox_min_z']
    
    flaglist =[]
    for i in range(int(len(bboxdepth))):
        if (bboxheight[i] <= 1 or bboxdepth[i] <= 1 or bboxwidth[i] <= 1 or 
            bboxdiffx[i] <=1 or bboxdiffy[i]<=1 or bboxdiffz[i] <= 1):
            flaglist.append(1)
        else:
            flaglist.append(0)
            
    flaglist_np = np.array(flaglist)
    
    deletedinstances = np.count_nonzero(flaglist_np)
    
    newflaglist = np.zeros(shape = flaglist_np.shape, dtype= 'uint16')
    count = 1
    for i in range(1, len(flaglist)):
        if (flaglist[i] == 0):
            newflaglist[i] = count
            count = count + 1
        else:
            newflaglist[i] = 0
    gpu_flaglist = cle.push(newflaglist)
    gpu_labels3d = cle.replace_intensities(gpu_label_image,gpu_flaglist)
    gpu_flaglist = None
    gpu_label_image = None
    print('{} deleted Objects'.format(deletedinstances))
    return gpu_labels3d

# 3D Feature Extraction--------------------------------------------------------
# measure characteristics of neighbors for label image
def neighbor_measurements(gpu_labelimage):
    import pyclesperanto_prototype as cle
    cells = cle.push(gpu_labelimage)    
    
    # determine neighbors of cells
    touch_matrix = cle.generate_touch_matrix(cells)

    # ignore touching the background
    cle.set_column(touch_matrix,0,0)
    cle.set_row(touch_matrix,0,0)
    
    # determine distances of all cells to all cells
    pointlist = cle.centroids_of_labels(cells)
    
    gpu_distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)
    
       
    gpu_touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    cle.set_column(gpu_touching_neighbor_count, 0, 0)
    
    return gpu_distance_matrix, gpu_touching_neighbor_count

# getting more sohpisticated topology regionprops (maybe integrate into regionprops without local)
def topology_regionprops(gpu_labelimage, nearest_neigh_list = [4,5,6], local = False):
    
    # Initialisation
    import pyclesperanto_prototype as cle
    import pandas as pd
    
    topology_props = {}
    
    avg_dmap_values = []
    stdev_dmap_values = []
    
    if local:
        loc_avg_dmap_values = []
        loc_stdev_dmap_values = []
    
    for n_count in nearest_neigh_list:
        # calculating the average distance of n nearest neighbours
        temp_avg_distance_map = cle.average_distance_of_n_closest_neighbors_map(gpu_labelimage, n = n_count)
        temp_stdev_distance_map = cle.standard_deviation_of_touching_neighbors_map(temp_avg_distance_map, gpu_labelimage, radius=2)
        
        # getting the values
        temp_avg_dmap_val = cle.read_intensities_from_map(gpu_labelimage, temp_avg_distance_map)
        temp_stdev_dmap_val = cle.read_intensities_from_map(gpu_labelimage, temp_stdev_distance_map)
        
        
        temp_stdev_distance_map = None
        
        #saving in lists for later processing
        avg_dmap_values.append(cle.pull(temp_avg_dmap_val)[0])
        stdev_dmap_values.append(cle.pull(temp_stdev_dmap_val)[0])
        
        if local:
            temp_loc_avg_dmap = cle.mean_of_touching_neighbors_map(temp_avg_distance_map, gpu_labelimage)
            temp_avg_distance_map = None
            temp_loc_stdev_dmap = cle.standard_deviation_of_touching_neighbors_map(temp_loc_avg_dmap, gpu_labelimage, radius=2)
            
            temp_loc_avg_dmap_val = cle.read_intensities_from_map(gpu_labelimage, temp_loc_avg_dmap)
            temp_loc_stdev_dmap_val = cle.read_intensities_from_map(gpu_labelimage, temp_loc_stdev_dmap)
            
            temp_loc_avg_dmap = None
            temp_loc_stdev_dmap = None
            
            loc_avg_dmap_values.append(cle.pull(temp_loc_avg_dmap_val)[0])
            loc_stdev_dmap_values.append(cle.pull(temp_loc_stdev_dmap_val)[0])

    if local:
        for avg_values, stdev_values, i in zip(loc_avg_dmap_values,loc_stdev_dmap_values,nearest_neigh_list):
            topology_props['local avg distance of {} closest points'.format(i)] = avg_values[1:]
            topology_props['local stddev distance of {} closest points'.format(i)] = stdev_values[1:]
            
    else:
        for avg_values, stdev_values, i in zip(avg_dmap_values,stdev_dmap_values,nearest_neigh_list):
            topology_props['avg distance of {} closest points'.format(i)] = avg_values[1:]
            topology_props['stddev distance of {} closest points'.format(i)] = stdev_values[1:]
            
    touch_matrix = cle.generate_touch_matrix(gpu_labelimage)

    # ignore touching the background
    cle.set_column(touch_matrix,0,0)
    cle.set_row(touch_matrix,0,0)
    
    
    # detect touching neighbor count   
    touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    touching_n_count = cle.pull(touching_neighbor_count)[0][1:]
    
    topology_props['touching neighbor count']= touching_n_count
    
    return pd.DataFrame(topology_props)

def add_centroids(regionprops, topologyprops, centroidnamelist = ['centroid-0','centroid-1','centroid-2']):
    import pandas as pd
    
    centroids_list = [regionprops[key] for key in centroidnamelist]
    centroids_list.append(topologyprops)
    top_props_wcentroid = pd.concat(centroids_list, axis = 1)
    
    return top_props_wcentroid

def regionprops_with_neighborhood_data(labelimage,gpu_labelimage,originalimage, n_closest_points_list = [2,3,4]):
    from skimage.measure import regionprops_table
    import pyclesperanto_prototype as cle
    import numpy as np
    # get lowest label index to adjust sizes of measurement arrays
    min_label = int(np.min(labelimage[np.nonzero(labelimage)]))
   
    #  defining function for getting standarddev as extra property
    # arguments must be in the specified order, matching regionprops
    def image_stdev(region, intensities):
        # note the ddof arg to get the sample var if you so desire!
        return np.std(intensities[region], ddof=1)
    
    # get region properties from labels
    regionprops = regionprops_table(labelimage.astype(dtype = 'uint16'), intensity_image= originalimage, 
                                        properties= ('area', 'centroid','feret_diameter_max',
                                        'major_axis_length','minor_axis_length', 'solidity', 'mean_intensity',
                                        'max_intensity', 'min_intensity'),extra_properties=[image_stdev])
    print('Scikit Regionprops Done')
    
    # push labelimage to GPU
    cells = gpu_labelimage
    gpu_labelimage = None
    # determine neighbors of cells
    touch_matrix = cle.generate_touch_matrix(cells)

    # ignore touching the background
    cle.set_column(touch_matrix,0,0)
    cle.set_row(touch_matrix,0,0)
    
    # determine distances of all cells to all cells
    pointlist = cle.centroids_of_labels(cells)
    
    cells = None
    
    # generate a distance matrix
    distance_matrix = cle.generate_distance_matrix(pointlist, pointlist)
    
    # detect touching neighbor count   
    touching_neighbor_count = cle.count_touching_neighbors(touch_matrix)
    cle.set_column(touching_neighbor_count, 0, 0)
    touch_matrix = None

    # conversion and editing of the distance matrix, so that it doesn't break cle.average_distance.....
    viewdist_mat = cle.pull(distance_matrix)
    distance_matrix = None
    
    tempdist_mat = np.delete(viewdist_mat, range(min_label), axis = 0)
    edited_distmat = np.delete(tempdist_mat, range(min_label), axis =1)

    #iterating over different neighbor numbers for avg neighbor dist calculation
    for i in n_closest_points_list:
        distance_of_n_closest_points = cle.pull(cle.average_distance_of_n_closest_points(cle.push(edited_distmat), n=i))[0]
    
        # addition to the regionprops dictionary
        regionprops['avg distance of {val} closest points'.format(val = i)]=distance_of_n_closest_points

    # processing touching neighborcount for addition to regionprops (deletion of background & not used labels)
    touching_neighbor_c = cle.pull(touching_neighbor_count)
    touching_neighbor_count = None
    touching_neighborcount_formated = np.delete(touching_neighbor_c, list(range(min_label)))
    
    # addition to the regionprops dictionary
    regionprops['touching neighbor count']= touching_neighborcount_formated
    print('Regionprops Completed')
    
    # clearing of memory
    touching_neighborcount_formated = None
    touching_neighbor_c = None
    tempdist_mat = None
    edited_distmat = None
    distance_of_n_closest_points = None
    
    return regionprops


# Data Processing----------------------------------------------------------------------------
def standardscaler_for_dataframes(input_df):
    from sklearn import preprocessing
    import numpy as np
    import pandas as pd
    
    # retrieve keys from handed dataframe
    keys = input_df.keys()
    
    # train scaler and process data
    scaler = preprocessing.StandardScaler().fit(input_df)
    scaled = scaler.transform(input_df)
    
    # transposition needed for iteration purposes
    scaled = np.array(scaled).T
    
    #creation of an empty dictionary
    df_scaled = {}
    
    # iteration over keys and scaled columns and filling of the new dictionary
    for i,j in zip(keys, scaled):
        df_scaled[i]=j
    
    # conversion to pandas dataframe
    df_scaled = pd.DataFrame(df_scaled)
    
    return df_scaled

def sscale_with_pretrained_scaler(scaler,df_regprop):
    import numpy as np
    import pandas as pd
    keys = df_regprop.keys()
    scaled = scaler.transform(df_regprop)
    scaled = np.array(scaled).T
    output = {}
    for i,j in zip(keys, scaled):
        output[i]=j
    output = pd.DataFrame(output)
    return output  

def pca_99_expl_var(df_reg_props_scaled):
    from sklearn.decomposition import PCA
    import pandas as pd
    pca = PCA()

    # Separating out the features
    x = df_reg_props_scaled.loc[:, df_reg_props_scaled.keys()].values
    principalComponents = pca.fit_transform(x)

    # getting the explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_expl_var = [sum(explained_variance[:i+1]) for i in range(len(explained_variance))]
    for i,j in enumerate(cumulative_expl_var):
        if j >= 0.99:
            pca_cum_var_idx = i
            break
    
    subset = principalComponents.T[:pca_cum_var_idx+1].T
    subset_headings = ['PC #'+ str(i+1) for i in range(len(subset.T))]
    df_PCA_99 = pd.DataFrame(data = subset, columns = subset_headings)
    
    return df_PCA_99

def fit_pca_and_get_subset_limit(df_regprops):
    from sklearn.decomposition import PCA
    pca = PCA()

    # Separating out the features
    x = df_regprops.loc[:, df_regprops.keys()].values
    pca.fit(x)

    # getting the explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_expl_var = [sum(explained_variance[:i+1]) for i in range(len(explained_variance))]
    for i,j in enumerate(cumulative_expl_var):
        if j >= 0.99:
            pca_cum_var_idx = i
            break
    return pca, pca_cum_var_idx

def transform_PCA_99(pca_pretrained, df_regprops, index):
    import pandas as pd
    x = df_regprops.loc[:, df_regprops.keys()].values
    
    principalComponents = pca_pretrained.transform(x)
    
    subset = principalComponents.T[:index+1].T
    
    subset_headings = ['PC #'+ str(i+1) for i in range(len(subset.T))]
    
    df_PCA_99 = pd.DataFrame(data = subset, columns = subset_headings)
    
    return df_PCA_99

def regprops_to_stdscld_categorised_pca_aslist(df_regprops):
    from sklearn import preprocessing
    from sklearn.decomposition import PCA
    import numpy as np
    import pandas as pd
    
    # retrieve keys from handed dataframe
    keys = df_regprops.keys()
    
    # train scaler and process data
    scaler = preprocessing.StandardScaler().fit(df_regprops)
    scaled = scaler.transform(df_regprops)
    
    # transposition needed for iteration purposes
    scaled = np.array(scaled).T
    
    #creation of an empty dictionary
    df_scaled = {}
    
    # iteration over keys and scaled columns and filling of the new dictionary
    for i,j in zip(keys, scaled):
        df_scaled[i]=j
    
    # conversion to pandas dataframe
    df_scaled = pd.DataFrame(df_scaled)
    
    regpropsshape_stdsc = df_scaled[['area', 'centroid-0','centroid-1',
                                     'centroid-2','feret_diameter_max',
                                     'major_axis_length','minor_axis_length',
                                     'solidity']]
    regpropsintensity_stdsc = df_scaled[['mean_intensity','max_intensity', 
                                         'min_intensity', 'image_stdev',
                                         'centroid-0','centroid-1',
                                         'centroid-2']]
    regpropstopology_stdsc = df_scaled[['touching neighbor count','avg distance of 2 closest points',
                                        'avg distance of 3 closest points',
                                        'avg distance of 4 closest points', 
                                        'centroid-0','centroid-1','centroid-2']]
    
    pca = PCA()

    # Separating out the features
    x = df_scaled.loc[:, df_scaled.keys()].values
    principalComponents = pca.fit_transform(x)

    # getting the explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_expl_var = [sum(explained_variance[:i+1]) for i in range(len(explained_variance))]
    for i,j in enumerate(cumulative_expl_var):
        if j >= 0.99:
            pca_cum_var_idx = i
            break
    
    subset = principalComponents.T[:pca_cum_var_idx+1].T
    subset_headings = ['PC #'+ str(i+1) for i in range(len(subset.T))]
    df_PCA_99 = pd.DataFrame(data = subset, columns = subset_headings)
    namelist = ['Original Regionprops', 'Regionprops Standardscaled', ' Regionprops Topology', 
                'Regionprops Shape', 'Regionprops Intensity', 'Regionprops PCA']
    return [df_regprops,df_scaled,regpropstopology_stdsc,regpropsshape_stdsc,
            regpropsintensity_stdsc, df_PCA_99], namelist

def filterregprops_topology(df_regprops, avg_dist_nn_list = [2,3,4]):
    nn_avg_dist_keys =['avg distance of {} closest points'.format(i) for i in avg_dist_nn_list]
    regpropstopology = df_regprops[['touching neighbor count', 'centroid-0',
                                    'centroid-1','centroid-2']+nn_avg_dist_keys]
    return regpropstopology

def filterregprops_shape(df_regprops):
    regpropsshape = df_regprops[['area', 'centroid-0','centroid-1',
                                 'centroid-2','feret_diameter_max',
                                 'major_axis_length','minor_axis_length',
                                 'solidity']]
    return regpropsshape

def filterregprops_intensity(df_regprops):
    regpropsintensity = df_regprops[['mean_intensity','max_intensity', 
                                     'min_intensity', 'image_stdev', 
                                     'centroid-0','centroid-1',
                                     'centroid-2']]
    return regpropsintensity

# get list of saved regionprops with time index at the end
def get_sorted_list_of_regprops_folder(folderpath, filename_prefix, n_timepoints):
    import pandas as pd
    filelist = [folderpath+filename_prefix+str(i)+'.csv' for i in range(n_timepoints)]
    
    regpropslist = []

    for propname in filelist:
        try:
            regpropslist.append(pd.read_csv(propname))
        except FileNotFoundError:
            pass

    regpropslist = [pd.read_csv(i) for i in filelist]
    try:
        regpropslist = [i.drop('Unnamed: 0', axis = 1) for i in regpropslist]
    except:
        print('No Labels in Regionprops of {}'.format(folderpath))
    try:
        regpropslist = [i.drop('prediction', axis = 1) for i in regpropslist]
    except:
        print('No Predictions in Regionprops of {}'.format(folderpath))
    
    if regpropslist == []:
        print('No FIles Opened')
    
    else:
        return regpropslist

def readcsv_as_cl_input(path):
    import pandas as pd
    csv = pd.read_csv(path)
    
    try:
        csv = csv.drop('Unnamed: 0', axis = 1)
    except:
        print('No Labels in Regionprops of {}'.format(path))
    try:
        csv = csv.drop('prediction', axis = 1)
    except:
        print('No Predictions in Regionprops of {}'.format(path))
    
    return csv
        
def generate_measurement_image(gpu_labelimage , measurementlist, measurement_wo_bkgnd = True):
    import numpy as np
    import pyclesperanto_prototype as cle
    
    if measurement_wo_bkgnd:
        measurementlist_new = np.insert(measurementlist,0,0)    
    else:
        measurementlist_new = measurementlist
        
    # testing the cle functions for generation of outline image and cluster label image
    # first pushing of variables to GPU
    clelist = cle.push(measurementlist_new)

    #generation of cluster label image
    parametric_image = cle.replace_intensities(gpu_labelimage, clelist)
    gpu_labelimage = None
    clelist = None
    
    output = cle.pull(parametric_image)
    parametric_image = None
    
    return output

def local_avg_measurement(measurementlist, gpu_labelimage, measurement_wo_bkgnd = True):
    import numpy as np
    import pyclesperanto_prototype as cle
    
    if measurement_wo_bkgnd:
        measurementlist_new = np.insert(measurementlist,0,0)    
    else:
        measurementlist_new = measurementlist
        
    # testing the cle functions for generation of outline image and cluster label image
    # first pushing of variables to GPU
    clelist = cle.push(measurementlist_new)

    #generation of cluster label image
    parametric_image = cle.replace_intensities(gpu_labelimage, clelist)
    clelist = None
    
    loc_val_img = cle.mean_of_touching_neighbors_map(parametric_image, gpu_labelimage)
    parametric_image = None
    
    temp_loc_val = cle.read_intensities_from_map(gpu_labelimage, loc_val_img)
    
    loc_val = cle.pull(temp_loc_val)[0][1:]
    gpu_labelimage = None
    loc_val_img = None
    temp_loc_val = None
    return loc_val

def local_avg_dataframe(dataframe, gpu_labelimage, measurement_wo_bkgnd = True):
    import pandas as pd
    
    keylist = dataframe.keys()
    new_keylist = ['local avg '+ key for key in keylist]
    measurements = [dataframe[key].tolist() for key in keylist]
    loc_avg_measurements = [local_avg_measurement(measure, gpu_labelimage, measurement_wo_bkgnd = measurement_wo_bkgnd) for measure in measurements]
    gpu_labelimage = None
    loc_avg_dict = {k:v for k,v in zip(new_keylist,loc_avg_measurements)}
    
    return pd.DataFrame(loc_avg_dict)

# clustering and clustering associated functions-----------------------------------------------
# function for reforming the prediction list as regionprops does not start at 0
def reform_cluster_prediction_list(labelimage, predictionlist):
    import numpy as np
    predictionlist_new = np.array(predictionlist) + 1
    for i in range(int(np.min(labelimage[np.nonzero(labelimage)]))):
        predictionlist_new = np.insert(predictionlist_new,i,0)
    return predictionlist_new

# function for generating image labelled by clusters given the labelimage and the clusterpredictionlist
def generate_parametric_cluster_image(labelimage,gpu_labelimage ,predictionlist):
    import numpy as np
    import pyclesperanto_prototype as cle
    # reforming the prediction list this is done to account for cluster labels that start at 0
    # conviniently hdbscan labelling starts at -1 for noise, removing these from the labels
    predictionlist_new = np.array(predictionlist) + 1
    for i in range(int(np.min(labelimage[np.nonzero(labelimage)]))):
        predictionlist_new = np.insert(predictionlist_new,i,0)    

    # testing the cle functions for generation of outline image and cluster label image
    # first pushing of variables to GPU
    clelist = cle.push(predictionlist_new)

    #generation of cluster label image
    parametric_image = cle.replace_intensities(gpu_labelimage, clelist)
    gpu_labelimage = None
    clelist = None
    
    output = cle.pull(parametric_image).astype('uint32')
    parametric_image = None
    
    return output

# perform Kmeans clustering and return predictionlist
def kmeansclustering(measurements, clusternumber, iterations = 1000):
    from sklearn.cluster import KMeans
    import pandas as pd
    
    # scikit learn works with pandas dataframes so we will convert the dictionary into a dataframe
    data_frame = pd.DataFrame(measurements)
    
    # initialise clustering
    km = KMeans(n_clusters=clusternumber, max_iter=iterations, random_state =1000)

    # performing the clustering
    Y_pred = km.fit_predict(data_frame)

    # saving prediction as list for generating clustering image
    return Y_pred


def HDBSCAN_predictionlist(regionpropsdict, n_min_samples = 10, n_min_cluster = 50,UMAP = True, n_dimension_umap = 2, n_neighbors=30):
    import hdbscan
    import umap
    import pandas as pd
    
    # conversion to dataframe for handling by umap and hdbscan libraries
    dataframe = pd.DataFrame(regionpropsdict)
    
    if UMAP:
        # using UMAP to generate a dimension reduced non linear version of regionprops
        clusterable_embedding = umap.UMAP(
            n_neighbors=n_neighbors,
            min_dist=0.0,
            n_components=n_dimension_umap,
            random_state=42,
        ).fit_transform(dataframe)
        hdbscan_labels = hdbscan.HDBSCAN(min_samples=n_min_samples, min_cluster_size=n_min_cluster).fit_predict(clusterable_embedding)
    
    else:
        hdbscan_labels = hdbscan.HDBSCAN(min_samples=n_min_samples, min_cluster_size=n_min_cluster).fit_predict(dataframe)
    
    return hdbscan_labels

def GMM_with_testing_variables(dataframe,minclusters = 2,maxclusters=9):
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn import mixture
    import itertools


    lowest_bic = np.infty
    bic = []
    n_components_range = range(minclusters, maxclusters)
    cv_types = ['spherical', 'tied', 'diag', 'full']
    for cv_type in cv_types:
        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            gmm = mixture.GaussianMixture(n_components=n_components,
                                          covariance_type=cv_type)
            gmm.fit(dataframe)
            bic.append(gmm.bic(dataframe))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm

    bic = np.array(bic)
    color_iter = itertools.cycle(['navy', 'turquoise', 'cornflowerblue',
                              'darkorange'])
    clf = best_gmm
    bars = []

    # Plot the BIC scores
    plt.figure(figsize=(8, 6))
    spl = plt.subplot(2, 1, 1)
    for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
        xpos = np.array(n_components_range) + .2 * (i - 2)
        bars.append(plt.bar(xpos, bic[i * len(n_components_range):
                                      (i + 1) * len(n_components_range)],
                            width=.2, color=color))
    plt.xticks(n_components_range)
    plt.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
    plt.title('BIC score per model')
    xpos = np.mod(bic.argmin(), len(n_components_range)) + .65 +\
        .2 * np.floor(bic.argmin() / len(n_components_range))
    plt.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
    spl.set_xlabel('Number of components')
    spl.legend([b[0] for b in bars], cv_types)
    
    return clf

def plot_predictions_onto_UMAP(embedding, prediction, title = ' ', HDBSCAN = True):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    np.random.rand
    np.random.seed(42)
    rand_colours = np.random.rand((max(prediction)+3))
    plt.figure(figsize = (10,10))
    
    
    if HDBSCAN:
        clustered = (prediction >= 0)
        
        plt.scatter(embedding[~clustered, 0],
                    embedding[~clustered, 1],
                    c=(0.6, 0.6, 0.6), s=10, alpha=0.3)
        try:
            plt.scatter(embedding[clustered, 0],
                        embedding[clustered, 1],
                        c=[sns.color_palette()[int(x)] for x in prediction[clustered]],
                        s=10);
        except IndexError:
            plt.scatter(embedding[clustered, 0],
                        embedding[clustered, 1],
                        c=[rand_colours[x] for x in prediction[clustered]],
                        s=10);
    else:
        try:
            plt.scatter(embedding[:, 0],
                        embedding[:, 1],
                        c=[sns.color_palette()[int(x)] for x in prediction],
                        s=10);
        except IndexError:
            plt.scatter(embedding[:, 0],
                        embedding[:, 1],
                        c=[rand_colours[x] for x in prediction],
                        s=10);
    
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(title, fontsize=18)

# 2D image processing functions------------------------------------------------
def subtract_background(image, radius=50, light_bg=False):
    from skimage.morphology import white_tophat, black_tophat, disk #scikit image tophat function -> no subtraction of images needed
    str_el = disk(radius) #you can also use 'ball' here to get a slightly smoother result at the cost of increased computing time
    if light_bg:
        return black_tophat(image, str_el)
    else:
        return white_tophat(image, str_el)

# given an image from which blobs were detected and blobs list in format [[x,y,r]] returns boolean image
# with spots as True pixels 
def spot2image(image,spotlist):
    import numpy as np
    spot_image = np.zeros((image.shape), dtype=bool) # returns boolean image (only true = white and false = black) with original dimension
    for spot in spotlist:
        x, y, r = spot    # since scikit image returns x,y and radius coordinates we need 3 variables, even if one isn't used
        spot_image[int(x),int(y)] = True
    return spot_image

# marks spots as small green circles when given a list of spots with format [[x,y,r]] and axis to plot on
def marking_spots_plt(spotlist, axis_name):
    import matplotlib.pyplot as plt
    for blob in spotlist:
        y, x, r = blob
        c = plt.Circle((x, y), 1, color="lime", linewidth=1, fill=False)
        axis_name.add_patch(c)

def random_cmap(seed = 1):
    import numpy as np
    np.random.seed(seed)
    black = np.zeros((1,3), dtype=float)
    randcmap = np.append(black,(np.random.rand(255,3)),axis=0)
    return randcmap

# 2D visualisation functions---------------------------------------------------
def my_imshow(image):
    from matplotlib.pyplot import figure
    from skimage.io import imshow
    figure(figsize=(10,10)) # configure imshow dpi to make image larger
    imshow(image, cmap = 'gray')

def plot_horizontal(image_list, title_list = None, size = (20,20)):
    import matplotlib.pyplot as plt
    fig,axs = plt.subplots(1,len(image_list),figsize = size)
    for i,j in zip(image_list, range(len(image_list))):
        axs[j].imshow(i, cmap = 'gray')
        if title_list != None:
            axs[j].set_title(title_list[j])
    plt.show()

def nice_screenshot_lund(viewer_obj):
    import napari
    from skimage.transform import rotate
    from skimage.util import crop
    from skimage.color import rgba2rgb
    
    state = viewer_obj.window.qt_viewer.view.camera.get_state()
    state['center'] = (-500, -244.56994029525458, -3.7123967014400705)
    state['scale_factor'] = 650

    viewer_obj.window.qt_viewer.view.camera.set_state(state)

    screenshot = viewer_obj.screenshot()

    screenshot = rotate(screenshot, 355)
    screenshot = crop(screenshot, ((170, 70), (50, 40), (0,0)), copy=False)
    
    return rgba2rgb(screenshot)

# Testingspace
'''
#testing the generation of a colourmap for segmentation
import numpy as np
import pyclesperanto_prototype as cle
import time
from skimage.measure import regionprops_table
np.random.seed(1)
colours = np.zeros((1,3), dtype=float)
randocmap = np.append(colours,(np.random.rand(255,3)),axis=0) #lookup random seeds to have uniform colouring

voxel_size = np.array([2.5,0.6934,0.6934])


tribolium = io.imread("D://Uni\MSTER TUD//Master Thesis//First Coding Tries//tribolium_label_classification//Lund_18.0_22.0_Hours.tif")
tribolium_t0 = tribolium[7]
tribolium_t0_z25 = tribolium_t0[25]
isotropic_trib = resample_isotropic_nodownsample(tribolium_t0, voxel_size)
output, gpu_output = workflow(isotropic_trib)

start = time.process_time()
oldregprops = regionprops_with_neighborhood_data(output, gpu_output, isotropic_trib)
end = time.process_time()
print('old time = {}s'.format(end-start))

cleregionprops = cle.statistics_of_background_and_labelled_pixels(output, gpu_output)
neededkeys =['area','centroid_x','centroid_y','centroid_z','max_intensity','mean_intensity',
             'min_intensity','standard_deviation_intensity', 'sum_intensity']
cleregionprops_filtered = {k: cleregionprops[k] for k in neededkeys}
scikit_regionprops = regionprops_table(output.astype(dtype = 'uint16'), intensity_image= isotropic_trib, 
                                        properties= ('feret_diameter_max',
                                        'major_axis_length','minor_axis_length', 'solidity'))
regionprops = scikit_regionprops.update(cleregionprops_filtered)
'''