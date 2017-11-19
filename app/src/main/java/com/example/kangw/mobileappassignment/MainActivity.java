package com.example.kangw.mobileappassignment;

import android.Manifest;
import android.app.Dialog;
import android.app.job.JobParameters;
import android.app.job.JobService;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.drawable.BitmapDrawable;
import android.os.Build;
import android.os.Environment;
import android.os.Handler;
import android.os.AsyncTask;
import android.os.CountDownTimer;
import android.os.HandlerThread;
import android.provider.MediaStore;
import android.speech.tts.TextToSpeech;
import android.support.annotation.NonNull;
import android.support.annotation.StringRes;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.DialogFragment;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.cameraview.CameraView;

import org.w3c.dom.Text;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Locale;
import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends AppCompatActivity {
    //variable for android
    private ImageView imageView1;
    private ImageView imageView2;
    private TextView textView;
    private TextView textView2;
    private TextView textView3;
    private TextView textView4;
    //variable for image data
    public static byte[] data1;
    //variable for toSpeech
    public TextToSpeech toSpeech;
    public int result;
    public String text;
    //variable for detection result
    public float[][] path;
    public String string;
    public String name;
    public String carPlate;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button buttonLoadImage = (Button) findViewById(R.id.button1);
        Button buttonRepeat = (Button)findViewById(R.id.button2);
        Button buttonCar = (Button)findViewById(R.id.button3);
        textView = (TextView) findViewById(R.id.textView);
        textView2 = (TextView) findViewById(R.id.textView2);
        textView3 = (TextView) findViewById(R.id.textView3);
        textView4 = (TextView) findViewById(R.id.textView4);
        imageView1 = (ImageView) findViewById(R.id.imageView1);
        imageView2 = (ImageView) findViewById(R.id.imageView2);
        buttonLoadImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                textView.setText("");
                textView2.setText("");
                textView3.setText("");
                textView4.setText("");
                dispatchTakePictureIntent();
            }
        });
        buttonRepeat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                toSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null);
            }
        });
        buttonCar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                toSpeech.speak(carPlate, TextToSpeech.QUEUE_FLUSH, null);
            }
        });
        toSpeech = new TextToSpeech(MainActivity.this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status==TextToSpeech.SUCCESS){
                    result=toSpeech.setLanguage(Locale.UK);
                }else{
                    Toast.makeText(getApplicationContext(),"Features not supported in your device.",Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    static final int REQUEST_IMAGE_CAPTURE = 1;

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            textView.setText("Please wait...");
            Bundle extras = data.getExtras();
            final Bitmap imageBitmap = (Bitmap) extras.get("data");
            imageView1.setImageBitmap(imageBitmap);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, baos);
            data1 = baos.toByteArray();
            NetworkAsyncTask asyncTask = new NetworkAsyncTask();
            asyncTask.execute();
            new CountDownTimer(9000, 1000) {
                public void onFinish() {
                    textView4.setText(carPlate);
                    //Person recognition
                    textView3.setText(name);
                    //face detection
                    textView.setText(string);
                    //Person detection
                    textView2.setText(Detection.personString);
                    //Add rectangle into image
                    annotateImage(imageBitmap);

                }
                public void onTick(long millisUntilFinished) {
                    // millisUntilFinished    The amount of time until finished.
                }
            }.start();
        }
            final Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Toast.makeText(getApplicationContext(), "Feature not supported in your device.", Toast.LENGTH_SHORT).show();
                    } else {
                        /*for(int i =0;i<Detection.person.length;i++){
                            if(Detection.person[i][0]!=null){
                                text += Detection.person[i][0]+" is feeling "+Detection.person[i][1];
                            }
                        }*/
                        text = Detection.objectName+" is feeling "+Detection.emotion;
                        toSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null);
                    }
                }
            }, 9000);
        }


    private void annotateImage(Bitmap bmp){
        Bitmap tempBitmap = Bitmap.createBitmap(bmp.getWidth(), bmp.getHeight(), Bitmap.Config.RGB_565);
        Canvas tempCanvas = new Canvas(tempBitmap);
        Paint paint = new Paint();
        paint.setColor(Color.RED);
        tempCanvas.drawBitmap(bmp, 0, 0, null);
        for(int i=0;i<path.length;i++){
            tempCanvas.drawLines(path[i],paint);
        }
        imageView2.setImageDrawable(new BitmapDrawable(getResources(), tempBitmap));
    }

    class NetworkAsyncTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            try {
                name = Detection.recognition_GetResult(MainActivity.data1);
                string = Detection.detection_GetResult(MainActivity.data1);
                path = Detection.detection_GetLine();
                carPlate = Detection.detect_CarPlate(MainActivity.data1);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}