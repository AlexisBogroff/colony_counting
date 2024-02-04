import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def set_output_name():
    current_time = time.strftime("%Y%m%d-%H%M%S")
    name = 'clusters_' + current_time + '.png'
    return name

def load_image(img_path):
    with Image.open(img_path) as img:
        img_array = np.array(img)
    return img_array

def extract_red_channel(img_array):
    red_channel = img_array[:,:,0]
    return red_channel

def filter_redish_pixels(red_channel, threshold=109):
    red_filter = red_channel < threshold
    X = np.where(red_filter)
    return X

def train_model(X, eps=5, min_samples=10):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(np.array(X).T)
    return dbscan

def plot_image_with_clusters(img_array, X, dbscan, show_plot=True, export_img=True, output_path=''):
    plt.imshow(img_array)
    for label in set(dbscan.labels_):
        if label != -1:
            cluster_center = np.mean(X[0][dbscan.labels_ == label]), np.mean(X[1][dbscan.labels_ == label])
            shift_text = 2
            plt.text(cluster_center[1] + shift_text, cluster_center[0] - shift_text, str(label),
                     fontsize=5, 
                     color='white')
    if export_img:
        name = set_output_name()
        output_path = 'output/' + name
        plt.savefig(output_path)
    if show_plot:
        plt.show()



def count_colonies(dbscan):
    n_colonies = len(set(dbscan.labels_))
    return n_colonies

def count_red_pixels(img_path, threshold=109, eps=5, min_samples=10, export_img=True, show_plot=True, output_path=''):
    """ Return the number of points counted and the image with the clusters' labels """
    img_array = load_image(img_path)
    red_channel = extract_red_channel(img_array)
    X = filter_redish_pixels(red_channel, threshold)
    dbscan = train_model(X, eps, min_samples)
    n_colonies = count_colonies(dbscan)
    plot_image_with_clusters(img_array, X, dbscan, show_plot, export_img, output_path)
    return n_colonies



if __name__ == '__main__':
    IMG_PATH    = 'data/sample_1.png'
    OUTPUT_PATH = 'output/'
    SHOW_PLOT   = True
    EXPORT_IMG  = True
    THRESHOLD   = 109       # Default 109; higher = more points considered red
    EPS         = 5
    MIN_SAMPLES = 8

    n_colonies = count_red_pixels(img_path      = IMG_PATH,
                                  threshold     = THRESHOLD,
                                  eps           = EPS,
                                  min_samples   = MIN_SAMPLES,
                                  show_plot     = SHOW_PLOT,
                                  export_img    = EXPORT_IMG,
                                  output_path   = OUTPUT_PATH)
    
    print(f'Number of colonies: {n_colonies}')
