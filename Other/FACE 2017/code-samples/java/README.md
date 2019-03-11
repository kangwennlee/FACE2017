# Sighthound Cloud Face Recognition API Tutorial - Java

## Prerequisites

- Create a Sighthound Cloud Token: https://www.sighthound.com/support/creating-api-token
- Java 6 SDK or newer must be installed: http://www.oracle.com/technetwork/java/javase/downloads/index.html

## Getting Started

- In recognition.java, replace 'YourSighthoundCloudToken' with your actual Token:

        public class Recognition {
            // TODO: Replace TOKEN with your own Sighthound Cloud Token
            public static final String TOKEN = "YourSighthoundCloudToken";
            ...

- From within the `code-samples/java` folder, run the following command to compile the code when ready:
    
        javac -cp ".:javax.json-1.0.4.jar" Recognition.java 

- Run the tutorial code by executing the following command:

        java -cp ".:javax.json-1.0.4.jar" Recognition

- View the full tutorial at https://www.sighthound.com/products/cloud/recognition/tutorial

## Open Source Licenses

This Java tutorial includes a library from the JSON Processing project (https://jsonp.java.net/index.html).
JSON Processing is dual licensed under 2 OSI approved licenses:
- COMMON DEVELOPMENT AND DISTRIBUTION LICENSE (CDDL - Version 1.1)
- GNU General Public License (GPL - Version 2, June 1991) with the Classpath Exception

A copy of the licenses are included here in CDDL-GPL-1-1.html or online at https://jsonp.java.net/license.html