import numpy as np
import os
from PIL import Image


def get_predictions(model,img):

    width,height = img.size    
    # running the model
    results = model(img,size=320)
    # getting cumulative xmin ymin xmax ymax conf_score class_label
    output = results.xyxy[0]
    # converting to numpy
    output_arr = output.numpy()
    # array of dictionaries to return
    final_arr = []
    # when there are no detections return nothing
    if(not np.any(output_arr)):
        return final_arr

    every_monument = ['bg', 'badrinath temple', 'basantapur tower', 'bhagavati temple', 'bhairavnath temple', 
        'bhaktapur tower', 'bhimeleshvara', 'bhimsen temple', 'bhupatindra malla column', 'bhuvana lakshmeshvara',
        'chasin dega', 'chayasilin mandap', 'dattatreya temple', 'degu tale temple_KDS', 'fasidega temple',
        'gaddi durbar', 'garud', 'golden gate', 'gopinath krishna temple', 'hanuman idol', 'indrapura',
        'jagannatha temple', 'kala-bhairava', 'kasthamandap', 'kavindrapura sattal', 'kedamatha tirtha', 'kirtipur tower', 
        'kumari ghar', 'lalitpur tower', 'mahadev temple', 'narayan temple', 'national gallery', 'nyatapola temple',
        'palace of the 55 windows', 'panchamukhi hanuman', 'pratap malla column', 'shiva temple', 'shveta bhairava',
        'siddhi lakshmi temple', 'simha sattal', 'taleju bell_BDS', 'taleju bell_KDS', 'taleju temple', 'trailokya mohan',
        'vastala temple', 'vishnu temple']
    # output_arr variable format for an image
    #  xmin ymin xmax ymax conf_score class_label
    #  [[          0      245.61      201.34      463.53     0.87713          33]
    #  [     394.69      138.53      530.92      472.24     0.84944          44]
    #  [     292.25      293.58      356.51      428.44     0.80411          40]
    #  [     189.05      268.21      253.16      438.15     0.73511          38]
    #  [          0      337.43      53.189      477.89     0.55997          17]
    #  [     251.73      259.03      303.86      477.59     0.40175           8]]

    # creating corresponding dictionary for every detection and appending into an array
    for i in output_arr:
        dict = {"rect" : { "w" : (i[2]-i[0]) / width ,      #width 
                            "x" : i[0] / width ,            #xmin
                            "h" : (i[3]-i[1]) / height ,    #height
                            "y" : i[1] / height,            #ymin
                            },
                "confidenceInClass" : i[4],
                "detectedClass" : every_monument[int(i[5])]
                }
        final_arr.append(dict)
        
    return final_arr


if __name__ == '__main__':
    test_img_directory = r"C:\Users\upoud\Desktop\Trying to infer from Tflit\Images"
    img_file = "hello.jpg"
    img = Image.open(os.path.join(test_img_directory,img_file))
    print(get_predictions(img))
    