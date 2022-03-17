package com.lpro.guiame;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertisingSet;
import android.bluetooth.le.AdvertisingSetCallback;
import android.bluetooth.le.AdvertisingSetParameters;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.ParcelUuid;
import android.util.Log;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import androidx.core.content.ContextCompat;

import java.util.UUID;

public class MainActivity extends AppCompatActivity {
    private final String CHANNEL_ID = "guiaMeNotificationsChannel";
    public static int BLUETOOTH_NOTIFICATION_ID = 1;

    private AdvertisingSet currentAdvertisingSet = null;

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
        this.startBtAdvertiser();
    }

    private void startBtAdvertiser() {
        // Permissions check, needed for bluetooth advertiser
        int permissionCheck = ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_ADVERTISE);
        if (permissionCheck != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.BLUETOOTH_ADVERTISE)) {
                showExplanation("Rationale", Manifest.permission.BLUETOOTH_ADVERTISE, 0);
            } else {
                requestPermission(Manifest.permission.BLUETOOTH_ADVERTISE, 0);
            }
        } else {
            Log.i("guiaMe/BT", "Bluetooth permissions already granted");
        }

        // Bluetooth Advertiser
        BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();

        if (!adapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            ActivityResultLauncher<Intent> registerForResult = registerForActivityResult(
                    new ActivityResultContracts.StartActivityForResult(),
                    result -> {
                        if (result.getResultCode() == Activity.RESULT_OK) {
                            // There are no request codes
                            // Intent data = result.getData();
                            Toast.makeText(this, "Bluetooth permissions granted", Toast.LENGTH_LONG).show();
                        } else {
                            // TODO: Show message to user saying we need the bluetooth and close the app
                            Toast.makeText(this, "This app needs Bluetooth to properly work!", Toast.LENGTH_LONG).show();
                        }
                    });

            registerForResult.launch(enableBtIntent);
            if (!adapter.isEnabled()) return;
        }

        BluetoothLeAdvertiser advertiser = adapter.getBluetoothLeAdvertiser();
        ParcelUuid pUuid = new ParcelUuid(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"));

        AdvertisingSetParameters parameters = (new AdvertisingSetParameters.Builder())
                .setLegacyMode(true) // True by default
                .setConnectable(false)
                .setInterval(AdvertisingSetParameters.INTERVAL_MIN)
                .setTxPowerLevel(AdvertisingSetParameters.TX_POWER_HIGH)
                .build();

        AdvertiseData data = (new AdvertiseData.Builder())
                .setIncludeDeviceName(true)
                .setIncludeTxPowerLevel(true)
                .addServiceData(pUuid, "SSSSamu".getBytes())
                .build();

        AdvertisingSetCallback callback = new AdvertisingSetCallback() {
            @Override
            public void onAdvertisingSetStarted(AdvertisingSet advertisingSet, int txPower, int status) {
                Log.i("ADV/CALLBACK", "onAdvertisingSetStarted(): txPower:" + txPower + " , status: "  + status);
                currentAdvertisingSet = advertisingSet;

                pushBluetoothNotification();
            }

            @Override
            public void onAdvertisingDataSet(AdvertisingSet advertisingSet, int status) {
                Log.i("ADV/CALLBACK", "onAdvertisingDataSet() :status:" + status);
            }

            @Override
            public void onScanResponseDataSet(AdvertisingSet advertisingSet, int status) {
                Log.i("ADV/CALLBACK", "onScanResponseDataSet(): status:" + status);
            }

            @Override
            public void onAdvertisingSetStopped(AdvertisingSet advertisingSet) {
                Log.i("ADV/CALLBACK", "onAdvertisingSetStopped():");
            }
        };

        advertiser.startAdvertisingSet(parameters, data, null, null, null, callback);
        // We should be sending advertisements every 160ms until we call advertiser.stopAdvertisingSet(callback);
    }

    private void showExplanation(String message, final String permission, final int permissionRequestCode) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Permission Needed")
                .setMessage(message)
                .setPositiveButton(android.R.string.ok, (dialog, id) -> requestPermission(permission, permissionRequestCode));
        builder.create().show();
    }

    private void requestPermission(String permissionName, int permissionRequestCode) {
        ActivityCompat.requestPermissions(this, new String[]{permissionName}, permissionRequestCode);
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

        PendingIntent closePendingIntent = PendingIntent.getBroadcast(this, 0, closeIntent, PendingIntent.FLAG_MUTABLE);
        NotificationCompat.Action closeAction = new NotificationCompat.Action.Builder(R.mipmap.ic_launcher, "Close", closePendingIntent).build();

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("guiaMe")
                .setContentText("Bluetooth LE Advertising")
                .setStyle(new NotificationCompat.BigTextStyle()
                        .bigText("Bluetooth Advertising Enabled")
                )
                .setContentIntent(closePendingIntent)
                .addAction(closeAction)
                .setOngoing(true);

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);
        notificationManager.notify(BLUETOOTH_NOTIFICATION_ID, builder.build());
    }
}