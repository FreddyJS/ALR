package com.lpro.guiame;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.bluetooth.BluetoothAdapter;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

public class NotificationReceiver extends BroadcastReceiver {
    private final String TAG = this.getClass().getSimpleName();

    @Override
    public void onReceive(Context context, Intent intent) {
        NotificationManager manager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        BluetoothAdvertiser advertiser = BluetoothAdvertiser.getInstance(null);
        if (advertiser == null) {
            // The APP was closed from the task manager
            manager.cancel(MainActivity.BLUETOOTH_NOTIFICATION_ID);
            return;
        }

        String action = intent.getAction();

        // Prepare the updated notification
        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
        Notification updatedNotification = this.createNotification(context, action);

        switch (action) {
            case "close":
                Log.d(TAG, "Closed app notification");
                manager.cancel(MainActivity.BLUETOOTH_NOTIFICATION_ID);

                advertiser.stopAdvertising();
                break;
            case "stop":
                Log.d(TAG, "Stopping ble advertising");
                advertiser.stopAdvertising();

                notificationManager.notify(MainActivity.BLUETOOTH_NOTIFICATION_ID, updatedNotification);
                break;
            case "start":
                Log.d(TAG, "Starting ble advertising");
                advertiser.startAdvertising();

                notificationManager.notify(MainActivity.BLUETOOTH_NOTIFICATION_ID, updatedNotification);
                break;
            case BluetoothAdapter.ACTION_STATE_CHANGED:
                int bluetoothState = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR);

                if (bluetoothState == BluetoothAdapter.STATE_ON) {
                    advertiser.updateAdvertiser();
                    advertiser.startAdvertising();
                    notificationManager.notify(MainActivity.BLUETOOTH_NOTIFICATION_ID, updatedNotification);
                }
        }
    }

    private Notification createNotification(Context context, String action) {
        Intent closeIntent = new Intent(context, NotificationReceiver.class);
        closeIntent.setAction("close");
        Intent advertiserIntent = new Intent(context, NotificationReceiver.class);
        advertiserIntent.setAction(action.equals("stop") ? "start" : "stop");

        PendingIntent closePendingIntent = PendingIntent.getBroadcast(context, 0, closeIntent, 0);
        PendingIntent advertiserPendingIntent = PendingIntent.getBroadcast(context, 0, advertiserIntent, 0);
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
