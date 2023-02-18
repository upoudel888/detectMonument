import numpy as np
import os
from PIL import Image


def get_predictions(model,img):

    dim = img.size
    
    results = model(img,size=320)
    # getting cumulative xmin ymin xmax ymax conf_score class_label
    output = results.xyxy[0]
    # converting to numpy
    new_output = output.numpy()

    # when there are no detections return all zeros
    if(not np.any(new_output)):
        # Create output arrays of the desired sizes
        bbox_out = np.zeros((1, 10, 4))
        classes_out = np.zeros((1, 10))
        score_out = np.zeros((1, 10))
        num_boxes_out = np.zeros((1,))

        return [bbox_out, classes_out, score_out, num_boxes_out]




    # retrieving bbox classes score and class_no from cumulative output
    bbox = new_output[...,:4]
    classes = new_output[...,5:6]
    score = new_output[...,4:5]

    # converting above variables to desired dimensions
    # (1,10,4), (1,10) , (1,10) , (1)
    # bbox classes scores class_no

    # helper function to normalize the final results
    def normalize_xy(arr):
        width,height = dim
        arr[0] /= width
        arr[1] /= height
        arr[2] /= width
        arr[3] /= height
        return arr

    # Compute the desired sizes
    max_boxes = 10

    # Create output arrays of the desired sizes
    bbox_out = np.zeros((1, max_boxes, 4))
    classes_out = np.zeros((1, max_boxes))
    score_out = np.zeros((1, max_boxes))
    num_boxes_out = np.zeros((1,))

    # Copy the input arrays to output arrays
    num_boxes = min(max_boxes, bbox.shape[0])
    bbox_out[0, :num_boxes, :] = np.array(list(map(normalize_xy,bbox[:num_boxes, :])))
    classes_out[0, :num_boxes] = classes[:num_boxes,:].flatten()
    score_out[0, :num_boxes] = score[:num_boxes, :].flatten()
    num_boxes_out[0] = max_boxes

    return [bbox_out, classes_out, score_out, num_boxes_out]


if __name__ == '__main__':
    test_img_directory = r"C:\Users\upoud\Desktop\Trying to infer from Tflit\Images"
    img_file = "hello.jpg"
    img = Image.open(os.path.join(test_img_directory,img_file))
    print(get_predictions(img))
    