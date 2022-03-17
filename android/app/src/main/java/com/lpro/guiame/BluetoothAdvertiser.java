package com.lpro.guiame;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertisingSet;
import android.bluetooth.le.AdvertisingSetCallback;
import android.bluetooth.le.AdvertisingSetParameters;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.ParcelUuid;
import android.util.Log;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.UUID;

public class BluetoothAdvertiser {
    private final ParcelUuid dataUuid = new ParcelUuid(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"));
    private final AdvertisingSetParameters parameters;
    private final BluetoothLeAdvertiser advertiser;
    private final AdvertisingSetCallback callback;
    private final AdvertiseData data;
    private final Context context;

    BluetoothAdvertiser(Context context) {
        BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
        this.context = context;
        this.setupBluetooth(adapter);

        advertiser = adapter.getBluetoothLeAdvertiser();
        parameters = (new AdvertisingSetParameters.Builder())
                .setLegacyMode(true)
                .setConnectable(false)
                .setInterval(AdvertisingSetParameters.INTERVAL_MIN)
                .setTxPowerLevel(AdvertisingSetParameters.TX_POWER_HIGH)
                .build();

        data = (new AdvertiseData.Builder())
                .setIncludeDeviceName(true)
                .setIncludeTxPowerLevel(true)
                .addServiceData(dataUuid, "SSSSamu".getBytes())
                .build();

        callback = new AdvertisingSetCallback() {
            @Override
            public void onAdvertisingSetStarted(AdvertisingSet advertisingSet, int txPower, int status) {
                Log.i("ADV/CALLBACK", "onAdvertisingSetStarted(): txPower:" + txPower + " , status: " + status);
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
    }

    private void setupBluetooth(BluetoothAdapter adapter) {
        // Permissions check, needed for bluetooth advertiser in SDK >= 31
        int permissionCheck = ContextCompat.checkSelfPermission(context, Manifest.permission.BLUETOOTH_ADVERTISE);
        if (Build.VERSION.SDK_INT >= 31 && permissionCheck != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(context, "Requesting permissions", Toast.LENGTH_LONG).show();
            if (ActivityCompat.shouldShowRequestPermissionRationale(((MainActivity) context), Manifest.permission.BLUETOOTH_ADVERTISE)) {
                AlertDialog.Builder builder = new AlertDialog.Builder(context);
                builder.setTitle("Permission Needed")
                        .setMessage("Please grant bluetooth permissions")
                        .setPositiveButton(android.R.string.ok, (dialog, id) -> ActivityCompat.requestPermissions(((MainActivity) context), new String[]{Manifest.permission.BLUETOOTH_ADVERTISE}, 0));
                builder.create().show();
            } else {
                ActivityCompat.requestPermissions(((MainActivity) context), new String[]{Manifest.permission.BLUETOOTH_ADVERTISE}, 0);
            }
        } else {
            Toast.makeText(context, "Bluetooth permissions already granted", Toast.LENGTH_LONG).show();
        }

        // Turn on bluetooth adapter if it's not
        if (!adapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            ActivityResultLauncher<Intent> registerForResult = ((MainActivity) context).registerForActivityResult(
                    new ActivityResultContracts.StartActivityForResult(),
                    result -> {
                        if (result.getResultCode() == Activity.RESULT_OK) {
                            // There are no request codes
                            // Intent data = result.getData();
                            Toast.makeText(context, "Bluetooth permissions granted", Toast.LENGTH_LONG).show();
                        } else {
                            // TODO: Show message to user saying we need the bluetooth and close the app
                            Toast.makeText(context, "This app needs Bluetooth to properly work!", Toast.LENGTH_LONG).show();
                        }
                    });

            registerForResult.launch(enableBtIntent);
        }
    }

    public boolean startAdvertising() {
        if (Build.VERSION.SDK_INT >= 31 && ContextCompat.checkSelfPermission(context, Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED) {
            return false;
        }

        advertiser.startAdvertisingSet(parameters, data, null, null, null, callback);
        // We should be sending advertisements every 160ms until we call advertiser.stopAdvertisingSet(callback);
        return true;
    }

    public void stopAdvertising() {
        if (Build.VERSION.SDK_INT >= 31 && ContextCompat.checkSelfPermission(context, Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED) {
            return;
        }

        advertiser.stopAdvertisingSet(callback);
    }
}
