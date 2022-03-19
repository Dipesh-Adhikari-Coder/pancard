# importing libraries

from flask import Flask, render_template, request
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image


app = Flask(__name__)  # app starter


@app.route('/', methods=["GET", "POST"])  # app route or URL only "/" means it will open in home page
@app.route('/home')
def homepage():
    # execute if request is "GET"
    if request.method == "GET":
        return render_template('index.html')

    # execute if request is "POST"
    if request.method == "POST":
        # GET uploaded image
        file_upload = request.files['file_upload']
        filename = file_upload.filename

        # resize and save the uploaded image
        uploaded_image = Image.open(file_upload).resize(250, 160)
        uploaded_image.save('images/resized-image1.jpg')

        # Resize and save the original image to ensure both uploaded and original matches in size
        original_image = Image.open(file_upload).resize((250, 160))
        original_image.save('image/resized-image1.jpg')

        # Read uploaded and original image as array
        original_image = cv2.imread('image/resized-image1.jpg')
        uploaded_image = cv2.imread('image/resized-image1.jpg')

        # convert image into grayscale
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

        # Calculate structural similarity
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")

        # Calculate threshold and contours
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Draw contours on image
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_image, (x, y), (c + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(uploaded_image, (x, y), (c + w, y + h), (0, 0, 255), 2)

        # to save all the outputs
        cv2.imwrite('image_original.jpg', original_image)
        cv2.imwrite('image_uploaded.jpg', uploaded_image)
        cv2.imwrite('image_diff.jpg', diff)
        cv2.imwrite('image_thresh.jpg', thresh)

        return render_template('index.html', pred=str(round(score * 100, 2)) + '%' + 'correct')


# main function
if __name__ == '__main__':
    app.run(debug=True)
