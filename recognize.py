'''
gesture recognizer
by: tracy :3
'''

import math

# constants
MIN_WIDTH = 30 #if gesture width is <30 then it is not stretched horizontally (ex. i, l)
MIN_HEIGHT = 30 #if gesture height is <30 then it is not stretched vertically (ex. _)
NORM_SIZE = 200 #all gestures are normalized to 200x200 before comparison with existing
ACCURACY_PTS = 10 #how many points the gesture is generalized to before comparison

# helper functions ##############################################################
gest = [[0, 0], [50, 0], [50, 50], [0, 50], [0, 0]]

def get_x(point):
    ''' consume Point and produce x coordinate '''
    return point[0]

def get_y(point):
    ''' consume Point and produce y coordinate '''
    return point[1]

def get_max_ind(gesture, index):
    ''' return max index value in gesture '''
    lst = []
    for i in range(len(gesture)):
        lst.append(gesture[i][index])
    return max(lst)

def get_min_ind(gesture, index):
    ''' return min index value in gesture '''
    lst = []
    for i in range(len(gesture)):
        lst.append(gesture[i][index])
    return min(lst)

def translate_gesture(gesture, x_offset, y_offset):
    ''' consume gesture and offset it by x-offset and y-offset '''
    for i in range(len(gesture)):
        gesture[i][0] += x_offset
        gesture[i][1] += y_offset
    return gesture

def scale_gesture(gesture, x_scale, y_scale):
    ''' consume gesture and scale it by x_scale and y_scale '''
    for i in range(len(gesture)):
        gesture[i][0] *= x_scale
        gesture[i][1] *= y_scale
    return gesture

def get_b_box(gesture):
    ''' consume gesture and produce top left and bottom right points of bbox '''
    return [[get_min_ind(gesture, 0), get_min_ind(gesture, 1)],
            [get_max_ind(gesture, 0), get_max_ind(gesture, 1)]]

def dist_between_pts(point1, point2):
    ''' consume 2 points and produce distance between them '''
    return math.sqrt((get_x(point2) - get_x(point1)) ** 2 + (get_y(point2) - get_y(point1)) ** 2)

def gesture_length(gesture):
    ''' consume gesture and calculates total distance between all points '''
    length = 0
    for i in range(len(gesture)-1):
        length += dist_between_pts(gesture[i], gesture[i+1])
    return length

def get_points(gesture, loi):
    ''' consumes gesture and list of index, and produce list of all points at index '''
    lst = []
    for i in loi:
        lst.append(gesture[i])
    return lst

def get_n_sample(gesture):
    ''' produces n points from gesture '''
    sample = []
    index_at = 1/ACCURACY_PTS
    
    for i in range(ACCURACY_PTS):
        sample.append(gesture[math.floor((len(gesture) - 1) * index_at * i)])
        
    return sample

def move_and_scale(gesture, x_scale, y_scale):
    ''' moves top left corner to [0, 0] and scales it  accordingly '''
    x_shift = get_b_box(gesture)[0][0]
    y_shift = get_b_box(gesture)[0][1]
    gesture = translate_gesture(gesture, -x_shift, -y_shift)
    
    return scale_gesture(gesture, x_scale, y_scale)

def x_scale(bbox):
    ''' bbox width / norm-size '''
    return (NORM_SIZE / (bbox[1][0] - bbox[0][0]))

def y_scale(bbox):
    ''' bbox height / norm-size '''
    return (NORM_SIZE / (bbox[1][1] - bbox[0][1]))

def normalize(gesture):
    ''' normalize gesture to origin and size NORM_SIZE '''
    bbox = get_b_box(gesture) #[[x, y], [x, y]]
    
    if ((bbox[1][0] - bbox[0][0]) < MIN_WIDTH):
        return move_and_scale(gesture, 1, y_scale(bbox))
    elif ((bbox[1][1] - bbox[0][1]) < MIN_HEIGHT):
        return move_and_scale(gesture, x_scale(bbox), 1)
    else:
        return move_and_scale(gesture, x_scale(bbox), y_scale(bbox))

def diff_between_points(gesture1, gesture2):
    ''' find distance between corresponding points in 2 gestures '''
    # both gestures have same length
    diff = 0
    for i in range(len(gesture1)):
        diff += dist_between_pts(gesture1[i], gesture2[i])
    return diff

def calculate_spatial_point(point1, point2, unit, dist):
    ''' calculates point that is unit away from point1 between pt1 and pt2 '''
    x = get_x(point1) + (get_x(point2) - get_x(point1)) * (unit / dist)
    y = get_y(point1) + (get_y(point2) - get_y(point1)) * (unit / dist)
    return [x, y]

def spatial_sample(gesture):
    ''' produces ACCURACY_PTS spatially spaced out points in gesture '''
    length = gesture_length(gesture)
    u = length / ACCURACY_PTS
    unit = u
    num_points = math.floor(length/unit)
    sample = []
    counter = 0

    while (counter < num_points):
        dist = dist_between_pts(gesture[0], gesture[1])
        if (dist >= unit):
            sample.append(calculate_spatial_point(gesture[0], gesture[1], unit, dist))
            unit += u
            counter += 1
        else:
            unit = unit - dist
            gesture = gesture[1:]
        
    return sample

def find_closest_match(gesture, templates):
    ''' finds closest match for gesture in templates '''
    gesture_sample = spatial_sample(gesture)
    closest_match = diff_between_points(gesture_sample, spatial_sample(templates[0][1]))
    sym = templates[0][0]

    for i in range(len(templates)):
        t_sample = spatial_sample(templates[i][1])
        diff = diff_between_points(gesture_sample, t_sample)

        if (closest_match > diff):
            closest_match = diff
            sym = templates[i][0]

    return sym


# main function reads templates from csv





