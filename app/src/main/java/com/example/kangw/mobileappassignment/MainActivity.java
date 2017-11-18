package com.example.kangw.mobileappassignment;

import android.app.Activity;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.drawable.BitmapDrawable;
import android.media.Image;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.CountDownTimer;
import android.os.Environment;
import android.provider.MediaStore;
import android.speech.tts.TextToSpeech;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.Timer;
import java.util.TimerTask;

import javax.json.JsonObject;

public class MainActivity extends AppCompatActivity {
    //variable for android
    private ImageView imageView1;
    private ImageView imageView2;
    private TextView textView;
    private TextView textView2;
    //variable for image data
    public static byte[] data1;
    //variable for toSpeech
    public TextToSpeech toSpeech;
    int result;
    //variable for detection result
    public float[][] path;
    public String string;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button buttonLoadImage = (Button) findViewById(R.id.button1);
        textView = (TextView) findViewById(R.id.textView);
        textView2 = (TextView) findViewById(R.id.textView2);
        imageView1 = (ImageView) findViewById(R.id.imageView1);
        imageView2 = (ImageView) findViewById(R.id.imageView2);
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
        String text = textView.getText().toString();
        toSpeech.speak(text,TextToSpeech.QUEUE_FLUSH,null);
        buttonLoadImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                dispatchTakePictureIntent();
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
            Bundle extras = data.getExtras();
            final Bitmap imageBitmap = (Bitmap) extras.get("data");
            imageView1.setImageBitmap(imageBitmap);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, baos);
            data1 = baos.toByteArray();
            NetworkAsyncTask asyncTask = new NetworkAsyncTask();
            asyncTask.execute();
            textView.setText("Please wait...");
            new CountDownTimer(4000, 1000) {
                public void onFinish() {
                    textView2.setText(Detection.personString);
                    textView.setText(string);
                    annotateImage(imageBitmap);
                }
                public void onTick(long millisUntilFinished) {
                    // millisUntilFinished    The amount of time until finished.
                }
            }.start();
        }
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
                string = Detection.detection_GetResult(MainActivity.data1);
                path = Detection.detection_GetLine();
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}