// Filename: recognition.js
'use strict'
const fs = require('fs');
const path = require('path');
const async = require('async');
const request = require('request');
const gm = require('gm');

// TODO: Replace TOKEN with your own Sighthound Cloud Token
const recoConfig = {
  TOKEN: 'YourSighthoundCloudToken', 
  BASE_URL: 'https://dev.sighthoundapi.com/v1'
};

// Define a generic callback to be used for outputting responses and errors
function genericCallback(error, response, body) {
  if (!error && (response.statusCode == 200 || response.statusCode == 204)) {
    console.log(body, '\n');
  } else if (error) {
    console.log(error, '\n');
  } else {
    console.log(response.statusCode, body, '\n');
  }
}

// Create an array of the people we want to recognize. For this tutorial, the 
// person's name will be their Object ID, and it's also the folder name 
// containing their training images in the downloadable tutorial code zip file.
const people = ['Christy', 'Tristan', 'Abby', 'Kate'];

function step1_UploadImages() {
  
  // Create a queue to manage calls made to the /image endpoint. This queue
  // sets a limit of 3 concurrent calls.
  const qImages = async.queue((item, callback) => {
    console.log('uploading objectId: ' + item.objectId + ' | imageId: ' +
                item.imageId + ' | path: ' + item.imageLocalPath + '\n');

    // Create a read stream for the image to be uploaded
    const imageFileStream = fs.createReadStream(item.imageLocalPath);

    // Define options used for the API request
    const requestOptions = {
      url: `${recoConfig.BASE_URL}/image/${item.imageId}`,
      headers: {
        'Content-Type': 'application/octet-stream',
        'X-Access-Token': recoConfig.TOKEN
      },
      method: 'PUT',
      qs: {
        objectId: item.objectId,
        objectType: 'person',
        train: 'manual'
      }
    };

    // Pipe the image stream into the request with the options and callback
    imageFileStream.pipe(request(requestOptions, callback));
  }, 3);

  // For each person, get list of images in their folder and add to upload queue.
  // The objectId will be the person's name and the imageId will be the filename.
  people.forEach((name) => {
    const trainingDir = path.join(__dirname,'..','..','images','training',name);
    console.log('Scanning for input files in ', trainingDir);

    fs.readdir(trainingDir, (err, files) => {
      console.log(`Uploading ${files.length} files from '${name}' folder.`);

      // For every image found in folder, add the item to the queue for uploading
      files.forEach((filename) => {
        if (filename.indexOf('.jpg') > -1){
          qImages.push({
            objectId: name, 
            imageId: filename, 
            imageLocalPath: path.join(trainingDir, filename)
          }, genericCallback);
        }
      });
    });
  });

  // Proceed to Step 2 after all items in queue have been processed
  qImages.drain = () => step2_AddObjectsToGroup(people);
}

function step2_AddObjectsToGroup(objects) {
  console.log('*** STEP 2 - Adding People to Group "family" ***');
  const groupId = 'family';

  // Define options used for the API request
  const requestOptions = {
    body: JSON.stringify({objectIds: objects}),
    url: `${recoConfig.BASE_URL}/group/${groupId}`,
    headers: {
      'Content-Type': 'application/json',
      'X-Access-Token': recoConfig.TOKEN
    },
    method: 'PUT'
  };

  // Perform the API request using requestOptions and an anonymous callback
  request(requestOptions, (error, response, body) => {
    genericCallback(error, response, body);
    step3_TrainGroup(groupId);
  });
}

function step3_TrainGroup(groupId) {
  console.log(`*** Step 3 - Training Group '${groupId}' ***`);

  // Define options used for the API request
  const requestOptions = {
    url: `${recoConfig.BASE_URL}/group/${groupId}/training`,
    headers: {
      'Content-Type': 'application/json',
      'X-Access-Token': recoConfig.TOKEN
    },
    method: 'POST'
  };

  // Perform the API request using requestOptions and an anonymous callback
  request(requestOptions, (error, response, body) => {
    genericCallback(error, response, body);
    step4_TestReco(groupId);
  });
}

function step4_TestReco(groupId) {
  console.log('*** Step 4 - Test the Face Recognition ***');

  // Define the recognition callback
  function recoCallback(error, response, body) {
    if (!error && (response.statusCode == 200)) {
      console.log('Recognition success:', body);
      if (gm) {
        const objects = JSON.parse(body).objects;
        annotateImage(this.data.imageLocalPath, objects);
      } else {
        console.warn('\n*** Install GraphicsMagick to draw face recognition ' + 
          'results on images.')
      }
    } else if (error) {
      console.error(error);
    } else {
      console.error('error: ', response.statusCode, response.statusMessage);
    }
  }

  // Create a queue to manage calls made to the /recognition endpoint. This 
  // queue sets a limit of 1 concurrent upload.
  const qReco = async.queue((item, callback) => {
    console.log('\nUsing "' + item.groupId + '" group to recognize faces in ' +
      item.imageLocalPath + '\n');

    // Create a read stream for the image to be uploaded
    const imageFileStream = fs.createReadStream(item.imageLocalPath);

    // Define options used for the API request
    const requestOptions = {
      url: `${recoConfig.BASE_URL}/recognition`,
      headers: {
        'Content-Type': 'application/octet-stream',
        'X-Access-Token': recoConfig.TOKEN
      },
      method: 'POST',
      qs: {
        groupId: item.groupId
      }
    };

    // Pipe the image stream into the request with requestOptions and callback
    imageFileStream.pipe(request(requestOptions, callback));
  }, 1);

  
  // Get paths to the images to test recognition against
  const recoDir = path.join(__dirname, '..','..','images', 'reco-test');

  fs.readdir(recoDir, (err, files) => {
    console.log(`Recognizing faces in ${files.length} images`);

    // Add each image to the queue to be sent for face recognition
    files.forEach((filename) => {
      if (filename.indexOf('.jpg') > -1){
        qReco.push({
          groupId: groupId, 
          imageLocalPath: path.join(recoDir,filename)
        }, recoCallback);
      }
    });
  });

  // OPTIONAL - Using GraphicsMagick, markup the image with bounding boxes, 
  // names, and confidence scores.
  function annotateImage(imageFilePath, objects) {
    const inPath = path.parse(imageFilePath);
    const outPath = path.join(__dirname, 'out', inPath.name + '.png');

    // Set minimum confidence threshold needed to have a positive recognition.
    // Any values below this number will be marked as 'Unknown' in the tutorial.
    const recognitionConfidenceThreshold = 0.5

    // Load the source image and prepare to draw annotations on it.
    const outputImage = gm(imageFilePath)
      .autoOrient()
      .strokeWidth('2px')
      .fill('transparent')
      .font('Courier', 20);

    // Loop over each detected person and draw annotations
    objects.forEach((face) => {
      const confidence = face.faceAnnotation.recognitionConfidence;
      let name = face.objectId;

      // Set the bounding box color for positive recognitions
      outputImage.stroke('#73c7f1');

      // For low confidence scores, name the face 'Unknown' and use the color 
      // yellow for the bounding box
      if (confidence < recognitionConfidenceThreshold) {
        name = 'Unknown';
        outputImage.stroke('yellow');
        console.log('\nAn "Unknown" person was found since recognition ' +
          'confidence ' + confidence + ' is below the minimum threshold of ' +
          recognitionConfidenceThreshold);
      } else {
        console.log(`\nRecognized '${name}' with confidence ${confidence}`);
      }
      
      const verticesXY = face.faceAnnotation.bounding.vertices.map(
        vertice => [vertice.x, vertice.y]
      );
      console.log('Bounding vertices:', verticesXY);

      // Draw bounding box onto face
      outputImage.drawPolygon(verticesXY);

      // Get the x,y coordinate of the bottom left vertex
      const bottomLeft = verticesXY[3];
      const x = bottomLeft[0];
      const y = bottomLeft[1];

      // Draw objectId (name) and confidence score onto image
      outputImage.drawText(x, y + 16, name + '\n' + confidence);
    });

    // Save annotated image to local filesystem
    outputImage.write(outPath, (err) => {
      if (err){
        console.log('*** Face Recognition results not drawn on image. ' +
          'Install GraphicsMagick to do so.\n');
      }
    });
  }
}

// Start the recognition tutorial
step1_UploadImages();