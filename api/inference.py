import numpy as np
import os
from PIL import Image

# return_raw = True returns predictions with no threshold
def get_predictions(model,img,return_raw = False):

    width,height = img.size    
    # running the model
    results = model(img,size=320)
    # getting cumulative xmin ymin xmax ymax conf_score class_label
    output = results.xyxy[0]
    # made changes to models/common.py line 770 to return the image with bbox when 
    # retults.show() is done
    bbox_img = results.show()
    # converting to numpy
    output_arr = output.numpy()
    # array of dictionaries to return
    final_arr = []
    # when there are no detections return nothing
    if(not np.any(output_arr)):
        return final_arr

    # every_monument = ['bg', 'badrinath temple', 'basantapur tower', 'bhagavati temple', 'bhairavnath temple', 'bhaktapur tower', 
    #                   'bhimeleshvara', 'bhimsen temple', 'bhupatindra malla column', 'bhuvana lakshmeshvara', 'chasin dega',
    #                     'chayasilin mandap', 'dattatreya temple', 'degu tale temple_KDS', 'fasidega temple', 'gaddi durbar',
    #                     'garud', 'golden gate', 'gopinath krishna temple', 'hanuman idol', 'indrapura', 'jagannatha temple', 
    #                     'kala-bhairava', 'kasthamandap', 'kavindrapura sattal', 'kedamatha tirtha', 'kirtipur tower', 'kumari ghar',
    #                     'lalitpur tower', 'mahadev temple', 'narayan temple', 'national gallery', 'nyatapola temple', 'palace of the 55 windows',
    #                     'panchamukhi hanuman', 'pratap malla column', 'shiva temple', 'shveta bhairava', 'siddhi lakshmi temple', 'simha sattal',
    #                     'taleju bell_BDS', 'taleju bell_KDS', 'taleju temple', 'trailokya mohan', 'vastala temple', 'vishnu temple',
    #                     'bhimsen temple_PDS', 'char narayan temple', 'chyasim deval', 'garud statue', 'harishankar temple',
    #                     'krishna mandir', 'mani ganesh temple', 'mani mandap','royal palace_PDS', 'taleju bell_PDS', 'taleju temple north',
    #                       'taleju temple south', 'vishwanath temple', 'yognarendra malla statue']

    every_monument = ['badrinath temple', 'basantapur tower', 'bhagavati temple', 'bhairavnath temple', 'bhaktapur tower',
                     'bhimeleshvara', 'bhimsen temple', 'bhupatindra malla column', 'bhuvana lakshmeshvara', 'chasin dega',
                    'chayasilin mandap', 'dattatreya temple', 'degu tale temple_KDS', 'fasidega temple', 'gaddi durbar', 
                    'garud', 'golden gate', 'gopinath krishna temple', 'hanuman idol', 'indrapura', 'jagannatha temple', 
                    'kala-bhairava', 'kasthamandap', 'kavindrapura sattal', 'kedamatha tirtha', 'kirtipur tower', 'kumari ghar',
                    'lalitpur tower', 'mahadev temple', 'narayan temple', 'national gallery', 'nyatapola temple', 
                    'palace of the 55 windows', 'panchamukhi hanuman', 'pratap malla column', 'shiva temple',
                    'shveta bhairava', 'siddhi lakshmi temple', 'simha sattal', 'taleju bell_BDS', 'taleju bell_KDS', 
                    'taleju temple', 'trailokya mohan', 'vastala temple', 'vishnu temple', 'bhimsen temple_PDS', 
                    'char narayan temple', 'chyasim deval', 'garud statue', 'harishankar temple', 'krishna mandir',
                    'mani ganesh temple', 'mani mandap', 'royal palace_PDS', 'taleju bell_PDS', 'taleju temple north', 
                    'taleju temple south', 'vishwanath temple', 'yognarendra malla statue']

    # output_arr variable format for an images
    #  xmin ymin xmax ymax conf_score class_label
    #  [[          0      245.61      201.34      463.53     0.87713          33]
    #  [     394.69      138.53      530.92      472.24     0.84944          44]
    #  [     292.25      293.58      356.51      428.44     0.80411          40]
    #  [     189.05      268.21      253.16      438.15     0.73511          38]
    #  [          0      337.43      53.189      477.89     0.55997          17]
    #  [     251.73      259.03      303.86      477.59     0.40175           8]]
    
    # print(output_arr)
    # print(output_arr.shape) (rows,column)

    
    # removing the probability scores less than 50
    # keeping the number of detections per class 1
    THRESHOLD = 0.45
    if(return_raw) : THRESHOLD = 0.0
    
    output_arr1 = []    # array that contains bboxes with distinct classes

    i_count = 0
    for i in output_arr:
        # removing the classes having confidence score less than the threshold
        if ( i[4] < THRESHOLD): continue
        # initializing the first instance as the one with highest probability
        high = i
        # looping the list and finding if there's same class having higher probability
        # and calculating the position in which the hit occured
        hit_pos = -1
        j_count = 0
        for j in output_arr:
            # if they are of same class 
            if j[5] == high[5] and j[4] > high[4]:
                high = j
                hit_pos = j_count
            j_count += 1
        i_count += 1

        # if no element with same class was found then append
        if(hit_pos == -1):
            output_arr1.append(high)
        # if two elements of same classes were found then append ony if the hit was in latter index
        if(hit_pos > i_count): 
            output_arr1.append(high)


    # creating corresponding dictionary for every detection and appending into an array
    for i in output_arr1:
        dict = {"rect" : { "w" : (i[2]-i[0]) / width ,      #width 
                            "x" : i[0] / width ,            #xmin
                            "h" : (i[3]-i[1]) / height ,    #height
                            "y" : i[1] / height,            #ymin
                            },
                "confidenceInClass" : i[4],
                "DetectedClass" : every_monument[int(i[5])]
                }
        final_arr.append(dict)
    
    # changing the final arrays of dictionaries before returning
    # maximum detections per class 1 ( choose the one with maximum probability value)

    # this is returned when inferencing with form
    if(return_raw):
        print(bbox_img)
        return bbox_img,final_arr 
    # this is returned in case of API request
    return final_arr


if __name__ == '__main__':
    test_img_directory = r"C:\Users\upoud\Desktop\Trying to infer from Tflit\Images"
    img_file = "hello.jpg"
    img = Image.open(os.path.join(test_img_directory,img_file))
    print(get_predictions(img))
    