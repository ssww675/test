
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import load_model


model = load_model("model_new.h5")
#os.chdir('\\C:\Users\USER\Desktop\hesaru_code\\')
labels = os.listdir('./train_2')

def seperateBoxesAndSaveIt (image):
    box_list = []

    # Load the image
    image = cv2.imread(image) #IMG-20230212-WA0076.jpeg

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of blue color in HSV space
    lower_blue = np.array([100,50,50])
    upper_blue = np.array([140,255,255])

    # Create a binary image with only blue pixels
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply thresholding to the binary image to create a binary image
    thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Perform morphological operations to remove noise and fill the boxes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours in the binary image
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Iterate through each contour
    img_num = 0
    for i, c in enumerate(contours):
        # Approximate the contour as a polygon
        polygon = cv2.approxPolyDP(c, 0.05 * cv2.arcLength(c, True), True)
        
        # Check if the polygon has 4 sides (indicating a rectangle)
        if len(polygon) == 4:
            x, y, w, h = cv2.boundingRect(polygon)
            # Check if the contour has a minimum width and height to be considered a box
            if w > 100 and h > 100:
                text_region = image[y:y+h, x:x+w]
                # Neglect the blue border of the box by cropping the text region
                text_region = text_region[170:-170, 170:-170]

                img_num +=1
                #Check for the image name and delete if a file is already exist
                file_name = "text_{}.png".format(img_num)
                file_path = os.path.join(os.getcwd(), file_name)
               
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    
                # Save the boxed text as a separate image
                cv2.imwrite("text_{}.png".format(img_num), text_region)
                box_list.append("text_{}.png".format(img_num))
                # print(box_list)
    return box_list

def delete_files_in_root_folder(strings_list):
    for file_name in os.listdir():
        for string_value in strings_list:
            if string_value in file_name:
                os.remove(file_name)

def takeBoxOneByOneAndSaveCharactersSeperatelyAndSaveItInATextFile(box_list):
    all_letters = []
    letter_file_names = []

    

    ## check the length of box_list, throw an error
    if (box_list is None): 
        return []

    img_name_one = 0
    for item in box_list:
        img_name_one +=1
        # Load the image
        img = cv2.imread(item)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to binarize the image
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Find contours of the characters
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours from left to right
        contours = sorted(contours, key=lambda cnt: cv2.boundingRect(cnt)[0])

        # Set a counter for naming the saved images
        i = 0
        img_name_two = 0
        character_list = []        
        # Loop through the contours and save each character as a separate image
        for cnt in contours:
            img_name_two += 1
            x, y, w, h = cv2.boundingRect(cnt)
            roi = img[y:y+h, x:x+w]
            filename = str(img_name_one) + "_" + str(img_name_two) + '.png'
            # Check file size before saving
            if cv2.imencode('.png', roi)[1].size >= 600:
                cv2.imwrite(filename, roi)
                letter_file_names.append(filename)
                # character_list.append(filename)
                character_list.append(filename)
            i += 1

            #character recognizing part should come here inside the second for loop
        letters = []
        for val in character_list:
            imge = cv2.imread(val, cv2.IMREAD_GRAYSCALE)
            #print(imge)

            imge = cv2.resize(imge, (28, 28))
            imge = imge.reshape(1,28, 28, 1)
            #print(imge)
            pred = model.predict(imge)
            letter_idx = np.argmax(pred)
            letter = labels[letter_idx]
            letters.append(letter)
            ##print(letter)        
        all_letters.append(letters)
        
    delete_files_in_root_folder(box_list) 
    delete_files_in_root_folder(letter_file_names + ["MainImage.png"])
    print(all_letters)    
    return all_letters


# print(takeBoxOneByOneAndSaveCharactersSeperatelyAndSaveItInATextFile(seperateBoxesAndSaveIt("IMG_20230317_121624.jpg")))

# def getImg (req, res) :
#         img = req.data
#         # save the img
#         #....        
#         takeBoxOneByOneAndSaveCharactersSeperatelyAndSaveItInATextFile(seperateBoxesAndSaveIt())




# imge = cv2.imread(f'10.png', cv2.IMREAD_GRAYSCALE)
# #print(imge)

# imge = cv2.resize(imge, (28, 28))
# imge = imge.reshape(1,28, 28, 1)
# #print(imge)
# pred = model.predict(imge)
# letter_idx = np.argmax(pred)
# letter = labels[letter_idx]
# print(letter)