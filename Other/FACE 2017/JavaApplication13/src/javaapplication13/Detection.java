
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.Set;
import java.util.logging.Logger;
import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonObject;
import javax.json.JsonReader;

public class Detection {

    // TODO: Replace TOKEN with your own Sighthound Cloud Token
    public static final String TOKEN = "taxiwbbtopjO82jEVvkCDh0mlpZBE2B2wy1x";
    public static final String BASE_URL = "https://dev.sighthoundapi.com/v1/";

    // Set minimum confidence threshold needed to have a positive recognition.
    // Any values below this number will be marked as 'Unknown' in the tutorial.
    public static final double recognitionConfidenceThreshold = 0.5;
    // contentType
    private static final String contentTypeStream = "application/octet-stream";
    private static final String contentTypeJson = "application/json";

    // image folder if different from default folder
    private static String imageFolder = null;
    // working folder if different from default folder
    private static String workingFolder = null;
    // java logging
    private static Logger logger = Logger.getLogger(Detection.class.getName());

    // Create an array of the people we want to recognize. For this tutorial,
    // the person's name will be their Object ID, and it's also the folder name
    // containing their training images.
    private static final Set<File> peoples = new HashSet<File>();
    final byte[] data = null;

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

    private static JsonObject httpCall(String api, String method,
            String contentType, byte[] body) throws IOException {
        URL apiURL = new URL(api);
        HttpURLConnection connection = (HttpURLConnection) apiURL
                .openConnection();
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

    public static void step2_GetResult(byte[] data, File image) throws IOException {
        logger.info("*** Step 2 - Retrieve the Face Detection ***");
        final String api = BASE_URL + "detections?";
        JsonObject result = httpCall(api, "POST", contentTypeStream, data);
        if (result != null) {
            JsonArray objects = result.getJsonArray("objects");
            int faceFound = 0;
            for (int i = 0; i < objects.size(); i++) {
                if ("face".equals(objects.getJsonObject(i).getJsonString("type").getString())) {
                    faceFound++;
                    JsonObject attributes = objects.getJsonObject(i).getJsonObject("attributes");
                    String gender = attributes.getJsonString("gender").getString();
                    double genderConfidence = attributes.getJsonNumber("genderConfidence").doubleValue();
                    int age = attributes.getJsonNumber("age").intValue();
                    double ageConfidence = attributes.getJsonNumber("ageConfidence").doubleValue();
                    String emotion = attributes.getJsonString("emotion").getString();
                    double emotionConfidence = attributes.getJsonNumber("emotionConfidence").doubleValue();
                    System.out.println("Person "+ faceFound + ": "+ "Gender: "+gender + "Gender Confidence: "+genderConfidence + "Age: "+age+ "age Confidence: "+ageConfidence + "Emotion: "+emotion + "EmotionConfidence: "+emotionConfidence);
                }if("person".equals(objects.getJsonObject(i).getJsonString("type").getString()))
                {
                    JsonObject boundingBox = objects.getJsonObject(i).getJsonObject("boundingBox");
                    int x = boundingBox.getJsonNumber("x").intValue();
                    int y = boundingBox.getJsonNumber("y").intValue();
                    int height = boundingBox.getJsonNumber("height").intValue();
                    int width = boundingBox.getJsonNumber("width").intValue();
                    System.out.println("x: "+x+"y: "+y+"height: "+height+"width: "+width);
                }
            }
        }
    }

    public static void main(String[] args) throws IOException,
            InterruptedException {
        if (workingFolder == null) {
            workingFolder = new File(".").getCanonicalPath();
        }
        if (imageFolder == null) {
            imageFolder = workingFolder + File.separator + ".."
                    + File.separator + ".." + File.separator + "images";
        }
        logger.info(imageFolder);
        File images1 = new File(imageFolder + File.separator + "detection");
        if (images1.exists()) {
            File[] listOfFiles = images1.listFiles();
            logger.info("First file: " + listOfFiles[0].getName());
            byte[] data1 = null;
            if (listOfFiles[0].isFile()) {
                data1 = Files.readAllBytes(Paths.get(listOfFiles[0].getCanonicalPath()));
            }
            step2_GetResult(data1, listOfFiles[0]);
            //step2_AddObjectsToGroup();
            //step3_TrainGroup("family");
            //step4_TestReco("family");
        } else {
            logger.info("Failed to find images at " + images1.getCanonicalPath());
        }
    }
}
