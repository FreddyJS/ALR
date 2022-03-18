package com.lpro.guiame;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

public class NotificationReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        NotificationManager manager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        BluetoothAdvertiser advertiser = BluetoothAdvertiser.getInstance(context);
        String action = intent.getAction();

        // Prepare the updated notification
        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
        Notification updatedNotification = this.createNotification(context, action);

        switch (action) {
            case "close":
                Log.d("NotificationReceiver", "Closed app notification");
                manager.cancel(MainActivity.BLUETOOTH_NOTIFICATION_ID);

                advertiser.stopAdvertising();
                break;
            case "stop":
                Log.d("NotificationReceiver", "Stopping ble advertising");
                advertiser.stopAdvertising();

                notificationManager.notify(MainActivity.BLUETOOTH_NOTIFICATION_ID, updatedNotification);
                break;
            case "start":
                Log.d("NotificationReceiver", "Starting ble advertising");
                advertiser.startAdvertising();

                notificationManager.notify(MainActivity.BLUETOOTH_NOTIFICATION_ID, updatedNotification);
                break;
        }
    }

    private Notification createNotification(Context context, String action) {
        Intent closeIntent = new Intent(context, NotificationReceiver.class);
        closeIntent.setAction("close");
        Intent advertiserIntent = new Intent(context, NotificationReceiver.class);
        advertiserIntent.setAction(action.equals("stop") ? "start" : "stop");

        PendingIntent closePendingIntent = PendingIntent.getBroadcast(context, 0, closeIntent, PendingIntent.FLAG_MUTABLE);
        PendingIntent advertiserPendingIntent = PendingIntent.getBroadcast(context, 0, advertiserIntent, PendingIntent.FLAG_MUTABLE);
        NotificationCompat.Action closeAction = new NotificationCompat.Action.Builder(R.mipmap.ic_launcher, "Close", closePendingIntent).build();
        NotificationCompat.Action advertiserAction = new NotificationCompat.Action.Builder(R.mipmap.ic_launcher, action.equals("stop") ? "Start" : "Stop", advertiserPendingIntent).build();

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, MainActivity.CHANNEL_ID)
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

        return builder.build();
    }
}
