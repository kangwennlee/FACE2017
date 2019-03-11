# Sighthound Cloud Face Recognition API Tutorial - Node.js


## Prerequisites

- Create a Sighthound Cloud Token: https://www.sighthound.com/support/creating-api-token
- Install Node.js: https://nodejs.org
- (optional) Install GraphicsMagick to draw detection boxes, person names, and confidence scores on the final recognition images.
    - Mac: `brew install graphicsmagick`
    - Windows: http://www.graphicsmagick.org/INSTALL-windows.html


## Getting Started

- In recognition.js, replace 'YourSighthoundCloudToken' with your actual Token:

        var recoConfig = {
          TOKEN: 'YourSighthoundCloudToken', 
          BASE_URL: 'https://dev.sighthoundapi.com/v1/'
        };

- Install Node.js packages: From within the `code-samples/node` folder, run the following command to install them before starting the tutorial:
    
        npm install

- Run the tutorial code by executing the following command:

        node recognition.js

- View the full tutorial at https://www.sighthound.com/products/cloud/recognition/tutorial

