#!/usr/bin/python3

import numpy as np
import os
from scipy import stats
import sys

def main():

    project_name = sys.argv[1]
    image_width = sys.argv[2]
    scale_factor = sys.argv[3]

    points = np.loadtxt('unclassified_cloud.txt', usecols=range(4))
    offset = np.loadtxt('offset.txt', usecols=range(3))
    p_matrices = np.loadtxt('pmatrix.txt', usecols=range(1,13))
    filenames = np.genfromtxt('pmatrix.txt', usecols=range(1), dtype=str)

    x_offset = offset[0] 
    y_offset = offset[1]
    z_offset = offset[2]

    for point in points:
        print('Now processing point:')
        print(point)
        pixel_classes = np.array([])

        x = point[0]
        y = point[1]
        z = point[2]

        x_prime = x - x_offset
        y_prime = y - y_offset
        z_prime = z - z_offset

        prime_matrix = np.matrix([[x_prime], [y_prime], [z_prime], [1]])

        for i in range(p_matrices.shape[0]):
            filename = filenames[i]
            print('Now processing filename:')
            print(filename)
            p_matrix = np.matrix(p_matrices[i])
            print('Now processing pmatrix:')
            print(p_matrix)
            p_matrix = np.reshape(p_matrix, (-1, 4))
            dot_matrix = np.matmul(p_matrix, prime_matrix)
            dot_matrix = np.reshape(dot_matrix, (-1, 3))

            u = dot_matrix.A[0][0] / dot_matrix.A[0][2]
            v = dot_matrix.A[0][1] / dot_matrix.A[0][2]

            if u < 0 or v < 0:
                print ('Point is not found on this image')
                continue

            try:
                segmented_image = np.loadtxt(filename + '.txt.', usecols=range(np.floor(image_width / scale_factor)))
            except:
                print ('Segmented image not found.')
                continue

            pixel_class = segmented_image.astype(int)[np.floor(u / scale_factor)][np.floor(v / scale_factor)]
            pixel_classes = np.append(pixel_classes, pixel_class)
            print('Pixel classes now look like:')
            print(pixel_classes)

        try:
            point[3] = stats.mode(pixel_classes)[0][0]
        except:
            print('No classifications for this point.')
            continue

    classified_cloud = open('classified_cloud.txt', 'w')
    print(np.array2string(points).replace('\n','').replace(']','\n').replace('[',' ').replace('    ',' ').replace('   ',' ').replace('  ',' '), file = classified_cloud)
    classified_cloud.close()

if __name__ == "__main__":
    main()