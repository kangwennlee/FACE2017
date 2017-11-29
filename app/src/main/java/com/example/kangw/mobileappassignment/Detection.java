package com.example.kangw.mobileappassignment;

/**
 * Created by Kangwenn on 18/11/2017.
 */

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.logging.Logger;

import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonReader;

public class Detection {

    // TODO: Replace TOKEN with your own Sighthound Cloud Token
    public static final String TOKEN = "";
    public static final String BASE_URL = "https://dev.sighthoundapi.com/v1/";

    // contentType
    private static final String contentTypeStream = "application/octet-stream";
    private static final String contentTypeJson = "application/json";

    // java logging
    private static Logger logger = Logger.getLogger(Detection.class.getName());
    public final static String apiD = BASE_URL + "detections?";
    private final static String apiR = String.format("%srecognition?groupId=%s", BASE_URL, "family", "UTF-8");
    public final static String apiC = BASE_URL + "recognition?objectType=vehicle,licenseplate";
    public static JsonObject result;
    public static String personString = "";
    public static String emotion = "";
    public static String gender = "";
    public static String objectName = "";
    public static String carName = "";
    //public static String[][] person = new String[5][2];

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
        result = httpCall(apiD, "POST", contentTypeStream, data);
        double genderConfidence = 0;
        int age = 0;
        double ageConfidence = 0;
        double emotionConfidence = 0;
        int faceFound = 0;
        String detectionString = "Face Detection: ";
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
                    detectionString += "\nFace " + faceFound + ": " + " Gender: " + gender + " | Gender Confidence: " + genderConfidence + " | Age: " + age + " | age Confidence: " + ageConfidence + " | Emotion: " + emotion + " | EmotionConfidence: " + emotionConfidence;
                    //person[faceFound][1]=emotion;
                }
            }
        }
        return detectionString;
    }

    public static float[][] detection_GetLine(){
        JsonArray objects = result.getJsonArray("objects");
        float[][] pth=new float[objects.size()][16];
        int x = 0;
        int y = 0;
        int height = 0;
        int width = 0;
        int personFound = 0;
        personString="Person Found: ";
        for (int i = 0; i < objects.size(); i++) {
            if ("person".equals(objects.getJsonObject(i).getJsonString("type").getString())) {
                personFound++;
                JsonObject boundingBox = objects.getJsonObject(i).getJsonObject("boundingBox");
                x = boundingBox.getJsonNumber("x").intValue();
                y = boundingBox.getJsonNumber("y").intValue()+70;
                height = boundingBox.getJsonNumber("height").intValue();
                width = boundingBox.getJsonNumber("width").intValue();
                personString +="\nPerson "+ personFound+" : "+" x: "+x + " | y: " + y + " | height: " + height + " | width: " + width;
            }
            //line1
            pth[i][0] = x;
            pth[i][1] = y;
            pth[i][2] = x + width;
            pth[i][3] = y;
            //line2
            pth[i][4] = x;
            pth[i][5] = y;
            pth[i][6] = x;
            pth[i][7] = y-height;
            //line3
            pth[i][8] = x+width;
            pth[i][9] = y;
            pth[i][10] = x + width;
            pth[i][11] = y - height;
            //line4
            pth[i][12] = x;
            pth[i][13] = y - height;
            pth[i][14] = x + width;
            pth[i][15] = y - height;
        }

        return pth;
    }

    public static String recognition_GetResult(byte[] data)throws IOException{
        logger.info("*** Step 2 - Retrieve the Face Recognition ***");
        result = httpCall(apiR, "POST", contentTypeStream, data);
        JsonArray objects = result.getJsonArray("objects");
        double recognitionConfidence;
        String detectedPerson = "Person Detected: ";
        objectName="";
        if(result!=null){
            for(int i=0;i<objects.size();i++){
                objectName = objects.getJsonObject(i).getString("objectId");
                recognitionConfidence = objects.getJsonObject(i).getJsonObject("faceAnnotation").getJsonNumber("recognitionConfidence").doubleValue();
                detectedPerson += "\nName: " + objectName + " Confidence: " + recognitionConfidence;
            }
        }
        return detectedPerson;
    }

    public static String detect_CarPlate(byte[] data)throws IOException{
        logger.info("*** Step 2 - Retrieve the Car Plate ***");
        result = httpCall(apiC, "POST", contentTypeStream, data);
        String carPlateNumber="Car Plate: ";
        carName="";
        if(result!=null){
            JsonArray objects = result.getJsonArray("objects");
            for(int i=0;i<objects.size();i++){
                JsonObject vehicleAnnotation = objects.getJsonObject(i).getJsonObject("vehicleAnnotation");
                JsonObject licenseplate = vehicleAnnotation.getJsonObject("licenseplate");
                JsonObject licenseBounding = licenseplate.getJsonObject("bounding");
                JsonObject licenseAttributes = licenseplate.getJsonObject("attributes");
                JsonObject licenseSystem = licenseAttributes.getJsonObject("system");
                JsonObject licenseSystemString = licenseSystem.getJsonObject("string");
                String licenseSystemStringName = licenseSystemString.getString("name");
                carPlateNumber+=licenseSystemStringName;
            }
        }
        return carPlateNumber;
    }
}
