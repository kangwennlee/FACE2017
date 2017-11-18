package com.example.kangw.mobileappassignment;

/**
 * Created by Kangwenn on 18/11/2017.
 */

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.logging.Logger;

import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonReader;

public class Detection {

    // TODO: Replace TOKEN with your own Sighthound Cloud Token
    public static final String TOKEN = "xd4FUSLqx9ZFdKWv2BfPhW9Wq2534NnNAYqG";
    public static final String BASE_URL = "https://dev.sighthoundapi.com/v1/";

    // contentType
    private static final String contentTypeStream = "application/octet-stream";
    private static final String contentTypeJson = "application/json";

    // java logging
    private static Logger logger = Logger.getLogger(Detection.class.getName());

    // Define a generic callback to be used for outputting responses and errors
    private static void genericCallback(boolean error, int statusCode,
                                        String body) {
        if (!error && (statusCode == 200 || statusCode == 204)) {
            logger.info(body);
        } else if (error) {
            logger.warning(statusCode + "\n" + body);
        } else {
            logger.info(statusCode + "\n" + body);
        }
    }

    private static JsonObject httpCall(String api, String method, String contentType, byte[] body) throws IOException {
        URL apiURL = new URL(api);
        HttpURLConnection connection = (HttpURLConnection) apiURL.openConnection();
        connection.setRequestProperty("Content-Type", contentType);
        connection.setRequestProperty("X-Access-Token", TOKEN);
        connection.setRequestMethod(method);
        connection.setDoInput(true);
        if (body != null) {
            connection.setDoOutput(true);
            connection.setFixedLengthStreamingMode(body.length);
            OutputStream os = connection.getOutputStream();
            os.write(body);
            os.flush();
        }
        int statusCode = connection.getResponseCode();
        if (statusCode < 400) {
            JsonReader jReader = Json.createReader(connection.getInputStream());
            JsonObject jsonBody = jReader.readObject();
            genericCallback(false, statusCode, jsonBody.toString());
            return jsonBody;
        } else if (statusCode == 401) {
            genericCallback(true, statusCode, "Invalidated TOKEN");
            return null;
        } else {
            JsonReader jReader = Json.createReader(connection.getErrorStream());
            JsonObject jsonError = jReader.readObject();
            genericCallback(true, statusCode, jsonError.toString());
            return jsonError;
        }
    }

    public static String detection_GetResult(byte[] data) throws IOException {
        logger.info("*** Step 2 - Retrieve the Face Detection ***");
        final String api = BASE_URL + "detections?";
        JsonObject result = httpCall(api, "POST", contentTypeStream, data);
        String gender = null;
        double genderConfidence = 0;
        int age = 0;
        double ageConfidence = 0;
        String emotion = null;
        double emotionConfidence = 0;
        int faceFound = 0;
        String detectionString=null;
        if (result != null) {
            JsonArray objects = result.getJsonArray("objects");
            for (int i = 0; i < objects.size(); i++) {
                if ("face".equals(objects.getJsonObject(i).getJsonString("type").getString())) {
                    faceFound++;
                    JsonObject attributes = objects.getJsonObject(i).getJsonObject("attributes");
                    gender = attributes.getJsonString("gender").getString();
                    genderConfidence = attributes.getJsonNumber("genderConfidence").doubleValue();
                    age = attributes.getJsonNumber("age").intValue();
                    ageConfidence = attributes.getJsonNumber("ageConfidence").doubleValue();
                    emotion = attributes.getJsonString("emotion").getString();
                    emotionConfidence = attributes.getJsonNumber("emotionConfidence").doubleValue();
                    detectionString+="\nPerson " + faceFound + ": " + "Gender: " + gender + "Gender Confidence: " + genderConfidence + "Age: " + age + "age Confidence: " + ageConfidence + "Emotion: " + emotion + "EmotionConfidence: " + emotionConfidence;
                }
            }
        }
        return (detectionString);
    }
}