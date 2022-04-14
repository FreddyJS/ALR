package com.lpro.guiame;

import android.Manifest;
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
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

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.UUID;

public class BluetoothAdvertiser {
    private static BluetoothAdvertiser instance;

    private final ParcelUuid dataUuid = new ParcelUuid(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"));
    private final String TAG = this.getClass().getSimpleName();

    private final AdvertisingSetParameters parameters;
    private final AdvertisingSetCallback callback;
    private final AdvertiseData data;
    private final Context appContext;

    private BluetoothLeAdvertiser advertiser;
    private boolean advertising = false;

    /**
     *
     * @param activity: To turn on bluetooth if needed and to get the appContext
     */
    BluetoothAdvertiser(Activity activity) {
        BluetoothManager manager = (BluetoothManager) activity.getSystemService(Context.BLUETOOTH_SERVICE);
        BluetoothAdapter adapter = manager.getAdapter();
        this.appContext = activity.getApplicationContext();
        this.setupBluetooth(adapter, activity);

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
                Log.d(TAG, "onAdvertisingSetStarted(): txPower:" + txPower + " , status: " + status);
                advertising = true;
            }

            @Override
            public void onAdvertisingDataSet(AdvertisingSet advertisingSet, int status) {
                Log.d(TAG, "onAdvertisingDataSet() :status:" + status);
            }

            @Override
            public void onScanResponseDataSet(AdvertisingSet advertisingSet, int status) {
                Log.d(TAG, "onScanResponseDataSet(): status:" + status);
            }

            @Override
            public void onAdvertisingSetStopped(AdvertisingSet advertisingSet) {
                Log.d(TAG, "onAdvertisingSetStopped():");
                advertising = false;
            }
        };
    }

    private void setupBluetooth(BluetoothAdapter adapter, Activity activity) {
        // Permissions check, needed for bluetooth advertiser in SDK >= 31
        if (Build.VERSION.SDK_INT >= 31) {
            if (ContextCompat.checkSelfPermission(activity, Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(activity, new String[]{Manifest.permission.BLUETOOTH_ADVERTISE}, 0);
            }
        }

        // Turn on bluetooth adapter if it's not
        if (!adapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            ActivityResultLauncher<Intent> registerForResult = ((MainActivity) activity).registerForActivityResult(
                    new ActivityResultContracts.StartActivityForResult(),
                    result -> {
                        if (result.getResultCode() == Activity.RESULT_OK) {
                            Log.d(TAG, "Bluetooth enabled correctly");
                        } else {
                            Log.d(TAG, "Could not enable bluetooth adapter");
                        }
                    });

            registerForResult.launch(enableBtIntent);
        }
    }

    public boolean startAdvertising() {
        if (Build.VERSION.SDK_INT >= 31 && ContextCompat.checkSelfPermission(appContext, Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED) {
            return false;
        } else if (advertiser == null) {
            return false;
        }

        advertiser.startAdvertisingSet(parameters, data, null, null, null, callback);
        // We should be sending advertisements every 160ms until we call advertiser.stopAdvertisingSet(callback);
        return true;
    }

    public void stopAdvertising() {
        if (Build.VERSION.SDK_INT >= 31 && ContextCompat.checkSelfPermission(appContext, Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED) {
            return;
        } else if (advertiser == null) {
            return;
        }

        advertiser.stopAdvertisingSet(callback);
    }

    public void updateAdvertiser() {
        this.stopAdvertising();
        BluetoothManager manager = (BluetoothManager) appContext.getSystemService(Context.BLUETOOTH_SERVICE);
        BluetoothAdapter adapter = manager.getAdapter();
        advertiser = adapter.getBluetoothLeAdvertiser();
    }

    public boolean isAdvertising() {
        return advertising;
    }

    /**
     *
     * @param activity: To turn on bluetooth if needed and to get the appContext (first time only)
     * @return BluetoothAdvertiser instance
     */
    public static BluetoothAdvertiser getInstance(@Nullable Activity activity) {
        if (instance == null && activity != null) {
            instance = new BluetoothAdvertiser(activity);
        }

        return  instance;
    }
}
