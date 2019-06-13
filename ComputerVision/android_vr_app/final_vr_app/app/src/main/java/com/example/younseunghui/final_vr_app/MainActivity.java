package com.example.younseunghui.final_vr_app;

import com.google.android.gms.maps.OnStreetViewPanoramaReadyCallback;
import com.google.android.gms.maps.StreetViewPanorama;
import com.google.android.gms.maps.StreetViewPanorama.OnStreetViewPanoramaCameraChangeListener;
import com.google.android.gms.maps.StreetViewPanorama.OnStreetViewPanoramaChangeListener;
import com.google.android.gms.maps.StreetViewPanorama.OnStreetViewPanoramaClickListener;
import com.google.android.gms.maps.StreetViewPanorama.OnStreetViewPanoramaLongClickListener;
import com.google.android.gms.maps.StreetViewPanoramaView;
import com.google.android.gms.maps.SupportStreetViewPanoramaFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.StreetViewPanoramaCamera;
import com.google.android.gms.maps.model.StreetViewPanoramaLocation;
import com.google.android.gms.maps.model.StreetViewPanoramaOrientation;

import android.content.Context;
import android.graphics.Point;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;
import android.view.View;

import javax.xml.datatype.Duration;

public class MainActivity extends AppCompatActivity {
    private static final LatLng PNU = new LatLng(35.231592, 129.084232);
    private static final LatLng ICELAND = new LatLng(64.1687981,-21.675231);
    private static final LatLng ENGLAND = new LatLng(51.5009722,-0.1249155);
    private static final LatLng COMBODIA = new LatLng(11.5643469,104.9319782 );

    private StreetViewPanorama mStreetViewPanorama;

    private SensorManager mySensorManager;
    private SensorEventListener gyroListener;
    private Sensor myGyroscope;

    private double roll; //up down  up이면 양수 , down이면 음수
    private double pitch; //right, left, right이면 양수 left이면 음수

    private double timestamp_past = 0.0f;
    private double dt;

    private double rad_to_dgr = 180/Math.PI;
    private static final float nano_to_sec = 1.0f/1000000000.0f;
    private long duration = 100;

    double roll_dgr = 0;
    double pitch_dgr = 0;
    double roll_dgr_old = 0;
    double pitch_dgr_old = 0;

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        SupportStreetViewPanoramaFragment streetViewPanoramaFragment =
                (SupportStreetViewPanoramaFragment)
                        getSupportFragmentManager().findFragmentById(R.id.streetviewpanorama);
        streetViewPanoramaFragment.getStreetViewPanoramaAsync(
                new OnStreetViewPanoramaReadyCallback() {
                    @Override
                    public void onStreetViewPanoramaReady(StreetViewPanorama panorama) {
                        mStreetViewPanorama = panorama;
                        // Only set the panorama to SYDNEY on startup (when no panoramas have been
                        // loaded which is when the savedInstanceState is null).
                        if (savedInstanceState == null) {
                            mStreetViewPanorama.setPosition(PNU);
                        }
                    }
                });


        //using the gyroscope and accelometer
        mySensorManager = (SensorManager)getSystemService(Context.SENSOR_SERVICE);
        myGyroscope = mySensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        gyroListener = new SensorEventListener(){
            @Override
            public void onSensorChanged(SensorEvent sensorEvent) {
                /* 각 축의 각속도 성분을 받는다. */
                double gyroX = sensorEvent.values[0];
                double gyroY = sensorEvent.values[1];

                /*각속도를 적분하여 회전각을 추출하기 위해 적분 간격을 구한다. (dt)
                 *dt : 센서가 현재 상태를 감지하는 시간 간격
                 * NS2S : nano sec -> sec
                 */
                dt = (sensorEvent.timestamp - timestamp_past)*nano_to_sec;
                timestamp_past = sensorEvent.timestamp;

                //젤 처음엔 timestamp_past==0일때는 pass한다.
                if((dt - timestamp_past*nano_to_sec) != 0){
                    /*
                    * 각속도의 성분을 적분한다. 즉,  회전각으로 변환
                    * 그 결과는 radian값으로 저장됨.
                    * */
                    pitch = pitch + gyroY*dt;
                    roll = roll + gyroX*dt;

                    //그래서 그 radian값을 degree값으로 변환해준다.
                    roll_dgr = roll*rad_to_dgr;
                    pitch_dgr  = pitch*rad_to_dgr;
                }
                Log.e("LOG", "GYSCOPE "
                        + " [roll_dgr_old] : " + String.format("%.4f", roll_dgr_old)
                        + "\t [roll_dgr]     : " + String.format("%.4f", roll_dgr)
                        + "\t [abs(roll)]    : " + String.format("%.4f", Math.abs(roll_dgr_old - roll_dgr))
                );

                //api reference : https://developers.google.com/android/reference/com/google/android/gms/maps/model/StreetViewPanoramaCamera
                if(Math.abs(roll_dgr_old - roll_dgr) > 0.5){
                    if(!checkReady()) return;
                    float newTilt = mStreetViewPanorama.getPanoramaCamera().tilt - (float)(roll_dgr_old - roll_dgr)*3;
                    if(newTilt > 90)
                        newTilt = 90;
                    else if(newTilt < -90)
                        newTilt = -90;
                    mStreetViewPanorama.animateTo(
                            new StreetViewPanoramaCamera.Builder()
                                    .zoom(mStreetViewPanorama.getPanoramaCamera().zoom)
                                    .tilt(newTilt)
                                    .bearing(mStreetViewPanorama.getPanoramaCamera().bearing)
                                    .build(), duration
                    );
                    roll_dgr_old = roll_dgr;
                }

                if(Math.abs(pitch_dgr_old - pitch_dgr) > 0.5){
                    if(!checkReady()) return;
                    float newBearing = mStreetViewPanorama.getPanoramaCamera().bearing + (float)(pitch_dgr_old - pitch_dgr)*2;
                    mStreetViewPanorama.animateTo(
                            new StreetViewPanoramaCamera.Builder()
                                    .zoom(mStreetViewPanorama.getPanoramaCamera().zoom)
                                    .tilt(mStreetViewPanorama.getPanoramaCamera().tilt)
                                    .bearing(newBearing)
                                    .build(), duration
                    );
                    pitch_dgr_old = pitch_dgr;
                }

            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int i) {
            }
        };
    }

    private boolean checkReady(){
        if(mStreetViewPanorama== null){
            Toast.makeText(this, R.string.panorama_not_ready, Toast.LENGTH_SHORT);
            return false;
        }
        return true;
    }

    protected void onResume(){
        super.onResume();
        mySensorManager.registerListener(gyroListener, myGyroscope, SensorManager.SENSOR_DELAY_UI);
    }

    protected void onPause(){
        super.onPause();
        mySensorManager.unregisterListener(gyroListener);
    }

    protected void onStop(){
        super.onStop();
    }

    public void gotoICELAND(View view){
        if(!checkReady()) return;
        mStreetViewPanorama.setPosition(ICELAND);
    }

    public void gotoENGLAND(View view){
        if(!checkReady()) return;
        mStreetViewPanorama.setPosition(ENGLAND);
    }

    public void gotoCOMBODIA(View view){
        if(!checkReady()) return;
        mStreetViewPanorama.setPosition(COMBODIA);
    }

    public void gotoPNU(View view){
        if(!checkReady()) return;
        mStreetViewPanorama.setPosition(PNU);
    }
}
