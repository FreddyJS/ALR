package com.lpro.guiame;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

public class MainActivity extends AppCompatActivity {
    public static String CHANNEL_ID = "guiaMeNotificationsChannel";
    public static int BLUETOOTH_NOTIFICATION_ID = 1;
    private BluetoothAdvertiser advertiser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // WebView Setup
        WebView webView = findViewById(R.id.webview);
        WebSettings wvSettings = webView.getSettings();
        wvSettings.setJavaScriptEnabled(true);
        wvSettings.setDomStorageEnabled(true);
        webView.loadUrl("https://freddyjs.github.io/guiaMe/#/room");

        // Start Bluetooth Advertiser
        if (advertiser != null) {
            // Stop the avertiser if it's already running
            advertiser.stopAdvertising();
        }

        advertiser = BluetoothAdvertiser.getInstance(this);
        if (advertiser.startAdvertising()) {
            this.pushBluetoothNotification();
        } else {
            Toast.makeText(this, "The bluetooth advertiser failed to start", Toast.LENGTH_LONG).show();
        }
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

        PendingIntent closePendingIntent = PendingIntent.getBroadcast(this, 0, closeIntent, PendingIntent.FLAG_MUTABLE);
        PendingIntent advertiserPendingIntent = PendingIntent.getBroadcast(this, 0, advertiserIntent, PendingIntent.FLAG_MUTABLE);
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