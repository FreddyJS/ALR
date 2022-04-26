package com.lpro.guiame;

import android.annotation.SuppressLint;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

@SuppressLint("SetJavaScriptEnabled")
public class MainActivity extends AppCompatActivity {
    public static String CHANNEL_ID = "guiaMeNotificationsChannel";
    public static int BLUETOOTH_NOTIFICATION_ID = 1;
    private BluetoothAdvertiser advertiser;

    private void hideSystemUI() {
        View decorView = getWindow().getDecorView();
        decorView.setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE
                        // Set the content to appear under the system bars so that the
                        // content doesn't resize when the system bars hide and show.
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        // Hide the nav bar and status bar
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_FULLSCREEN);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.hideSystemUI();

        // WebView Setup
        WebView webView = findViewById(R.id.webview);
        WebSettings wvSettings = webView.getSettings();
        wvSettings.setJavaScriptEnabled(true);
        wvSettings.setDomStorageEnabled(true);
        webView.loadUrl("http://guiame.ddns.net/#/room");

        // Start Bluetooth Advertiser
        advertiser = BluetoothAdvertiser.getInstance(this);
        if (!advertiser.isAdvertising()) {
            if (advertiser.startAdvertising()) {
                pushBluetoothNotification();
            }
        } else {
            pushBluetoothNotification();
        }
    }

    @Override
    protected void onDestroy() {
        Log.d("MainActivity", "onDestroy(): Cleaning resources");
        super.onDestroy();
    }

    private void createNotificationChannel() {
        // Create the NotificationChannel, but only on API 26+ because
        // the NotificationChannel class is new and not in the support library
        CharSequence name = getString(R.string.channel_name);
        String description = getString(R.string.channel_description);

        NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, NotificationManager.IMPORTANCE_HIGH);
        channel.setDescription(description);

        // Register the channel with the system; you can't change the importance
        // or other notification behaviors after this
        NotificationManager notificationManager = getSystemService(NotificationManager.class);
        notificationManager.createNotificationChannel(channel);
    }

    private void pushBluetoothNotification()
    {
        // Create notification channel to display the bluetooth status
        this.createNotificationChannel();

        // Prepare and push the notification
        Intent closeIntent = new Intent(this, NotificationReceiver.class);
        closeIntent.setAction("close");

        Intent advertiserIntent = new Intent(this, NotificationReceiver.class);
        advertiserIntent.setAction("stop");

        PendingIntent closePendingIntent = PendingIntent.getBroadcast(this, 0, closeIntent, 0);
        PendingIntent advertiserPendingIntent = PendingIntent.getBroadcast(this, 0, advertiserIntent, 0);
        NotificationCompat.Action closeAction = new NotificationCompat.Action.Builder(R.mipmap.ic_launcher, "Close", closePendingIntent).build();
        NotificationCompat.Action advertiserAction = new NotificationCompat.Action.Builder(R.mipmap.ic_launcher, "Stop", advertiserPendingIntent).build();

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("guiaMe")
                .setContentText("Bluetooth LE Advertising")
                .setStyle(new NotificationCompat.BigTextStyle()
                        .bigText("Bluetooth Advertising Enabled")
                )
                .setContentIntent(closePendingIntent)
                .addAction(closeAction)
                .addAction(advertiserAction)
                .setOngoing(true);

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);
        notificationManager.notify(BLUETOOTH_NOTIFICATION_ID, builder.build());
    }
}