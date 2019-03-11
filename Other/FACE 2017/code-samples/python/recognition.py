#!/usr/bin/python

import base64
import httplib
import json
import os
import sys

# To annotate test images a recent version of Pillow is required. Under OS X
# or Windows install via `pip install Pillow`. Under linux install the
# `python-imaging` package.
from PIL import Image, ImageDraw, ImageFont

# Set this variable to True to print all server responses.
_print_responses = False

# Your Sighthound Cloud token. More information at
# https://www.sighthound.com/support/creating-api-token
_cloud_token = "YourSighthoundCloudToken"

# The cloud server to use, here we set the development server.
_cloud_host = "dev.sighthoundapi.com"

# A set in which to gather object names during step 1.
_object_ids = set()

# The name of the group to which we will add objects (step 2), train (step 3),
# and test with (step 4).
_group_name = "family"

# The directory where annotated test images will be written.
_output_folder = "out"


###############################################################################
def send_request(request_method, request_path, params):
    """A utility function to send API requests to the Sighthound Cloud server.

    This function will abort the script with sys.exit(1) on API errors.
    
    @param  request_method  The request method, "PUT" or "POST".
    @param  request_path    The URL path for the API request.
    @param  params          The parameters of the API request, if any.
    @return response_body   The body of the response.
    """
    # Send the request.
    headers = {"Content-type": "application/json",
               "X-Access-Token": _cloud_token}
    conn = httplib.HTTPSConnection(_cloud_host)
    conn.request(request_method, request_path, params, headers)

    # Process the response.
    response = conn.getresponse()
    body = response.read()
    error = response.status not in [200, 204]

    if _print_responses or error:
        print response.status, body

    if error:
        sys.exit(1)

    return body


###############################################################################
def is_image(filename):
    """A naive utility function to determine images via filename extension.

    @param  filename  The filename to examine.
    @return is_image  True if the file appears to be an image.
    """
    return filename.endswith('.png') or filename.endswith('.jpeg') or \
            filename.endswith('.jpg') or filename.endswith('.bmp')


###############################################################################
# Step 1: Upload Images & Link to Persons
# 
# The first thing to do is create a unique "objectId" for each Person you upload
# to the API. This ID can be anything you want, but we'll use their names for
# this tutorial. You must include this ID in the query string when uploading
# images so that the API knows who is in the photo. In the code example below,
# we will upload several photos of our subjects. This will accomplish two
# things: it will create four new Person Objects  and associate the uploaded
# images with each Person to teach the system to recognize them again in the
# future.
###############################################################################

###############################################################################
def step1_upload_images(train_path):
    """Upload all training images.

    @param  train_path  The path to the training image directory. This expects
                        images to be organized in directories by object name as
                        in "sighthound-cloud-tutorial/images/training".
    """
    print "Step 1: Uploading training images"
    # Look for directories in our training folder. The names of each directory
    # will be used as the object id for the images within.
    for name in os.listdir(train_path):
        base_path = os.path.join(train_path, name)
        if os.path.isdir(base_path):
            # Upload all image files within the directory.
            print "  Adding images for object id " + name
            for training_file in os.listdir(base_path):
                file_path = os.path.join(base_path, training_file)
                if is_image(file_path):
                    print "    Uploading file " + training_file
                    add_training_image(file_path, name)

                    # Track all object ids for group creation in step 2.
                    _object_ids.add(name)

    print "Step 1 complete\n"


###############################################################################
def add_training_image(image_path, object_id):
    """Submit an image to Sighthound Cloud for training.

    @param  image_path  File path to the image to analyze. The filename will be
                        used as the image id
    @param  object_id   The id of the object (person) captured by this image.
    """
    base64_image = base64.b64encode(open(image_path).read())
    params = json.dumps({"image": base64_image})

    url_path = "/v1/image/%s?train=manual&objectType=person&objectId=%s" % \
            (os.path.basename(image_path), object_id)
    send_request("PUT", url_path, params)


###############################################################################
# Step 2: Add Persons to a Group
# 
# Now that we have several Person Objects in the system with several photos
# each, let's add them to a new Group with the name specified in _group_name.
# Objects (People, in this tutorial) can be placed in one or more Groups.
###############################################################################

###############################################################################
def step2_create_group():
    """Create a group named via _group_name with the members from step 1."""
    print "Step 2: Creating group"
    print "  Adding objects %s to group %s" % (str(_object_ids), _group_name)

    params = json.dumps({"objectIds": list(_object_ids)})
    send_request("PUT", "/v1/group/" + _group_name, params)
    
    print "Step 2 complete\n"


###############################################################################
# Step 3: Train the Group
# 
# After the Group has been created, it is time to train the system to recognize
# these people in future requests. "Training" is a computer vision term that
# relates to the process of converting image data into mathematical models that
# a computer system can use to detect and identify objects. The Sighthound Cloud
# API requires that Groups be trained after new Objects are added to a Group, or
# when additional images are uploaded and linked to existing Objects as in Step
# 1 of the tutorial. 
###############################################################################

###############################################################################
def step3_train_group():
    """Train the group we created in step 2 to prepare it for recognition."""
    print "Step 3: Training group"
    print "  Sending train request for group %s" % _group_name

    send_request("POST", "/v1/group/%s/training" % _group_name, None)
    
    print "Step 3 complete\n"


###############################################################################
# Step 4: Test the Recognition
# 
# At this point, the API is now trained to recognize the Objects. The final step
# of this tutorial will upload several images to the recognition endpoint for
# testing: the default set provided with this sample includes one image for each
# person, and a group shot that includes all four people plus a new person that
# wasn't trained. The _group_name Group will be specified in the recognition
# request so that the API knows which people to look for. A folder named "out"
# will be created in the same directory as your source code file after the
# photos are processed. This folder will contain images that were generated
# based on the recognition response. The images will have bounding vertices,
# person names, and recognition confidence scores drawn over the people
# detected in the images uploaded for testing.
###############################################################################

###############################################################################
def step4_test(test_path):
    """Send images to our newly trained group to test its recognition."""
    print "Step 4: Beginning tests"
    # Create the output directory.
    if not os.path.exists(_output_folder):
        os.mkdir(_output_folder)


    # Submit all images in the test directory for recognition.
    for test_file in os.listdir(test_path):
        file_path = os.path.join(test_path, test_file)
        if not is_image(file_path):
            continue

        print "  Submitting test image " + test_file
        base64_image = base64.b64encode(open(file_path).read())
        params = json.dumps({"image": base64_image})
        url_path = "/v1/recognition?groupId=" + _group_name
        response = json.loads(send_request("POST", url_path, params))

        # Annotate the image
        image = Image.open(file_path)
        font = ImageFont.load_default
        draw = ImageDraw.Draw(image)

        for face in response['objects']:
            # Retrieve and draw a bounding box for the detected face.
            json_vertices = face['faceAnnotation']['bounding']['vertices']
            vert_list = [(point['x'], point['y']) for point in json_vertices]
            draw.polygon(vert_list)

            # Retrieve and draw the id and confidence of the recongition.
            name = face['objectId']
            confidence = face['faceAnnotation']['recognitionConfidence']
            draw.text(vert_list[0], "%s - %s" % (name, confidence))

        image.save(os.path.join(_output_folder, test_file))

    print "Step 4 complete\n"


###############################################################################
if __name__ == '__main__':
    # The entry point for the recogntion sample. This expects to be called
    # with the "images" directory provided with this sample, or a directory
    # of identical structure.
    if len(sys.argv) != 2:
        print "Usage: python recognition.py <path to images directory>"
        sys.exit(2)

    root_dir = sys.argv[1]

    step1_upload_images(os.path.join(root_dir, "training"))
    step2_create_group()
    step3_train_group()
    step4_test(os.path.join(root_dir, "reco-test"))

