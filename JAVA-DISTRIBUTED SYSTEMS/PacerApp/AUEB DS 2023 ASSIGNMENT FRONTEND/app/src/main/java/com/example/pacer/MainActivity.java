package com.example.pacer;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.core.content.ContextCompat;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.content.ContentResolver;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.os.AsyncTask;


import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    CardView cvRun, cvStatistics;
    TextView cvStatus;
    ImageView cvExit;
    Socket clientsocket;
    ObjectInputStream in;
    ObjectOutputStream out;
    private static final int FILE_CHOOSER_REQUEST_CODE = 1;
    final String ServerIP = "192.168.68.115"; // CHANGE THE IP MANUALLY!!!
    static final int ServerPort =  6000;
    Handler handler;
    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().setStatusBarColor(ContextCompat.getColor(this, R.color.main));
        cvExit = findViewById(R.id.cvExit);
        cvRun = findViewById(R.id.cvRun);
        cvStatistics = findViewById(R.id.cvStatistics);
        cvStatus = findViewById(R.id.cvStatus);
        handler = new Handler(Looper.getMainLooper());

        new Thread(() -> {
            try {
                handler.post(() -> cvStatus.setText("Connecting to the server..."));
                clientsocket = new Socket();
                clientsocket.connect(new InetSocketAddress(ServerIP, ServerPort), 4000);
                out = new ObjectOutputStream(clientsocket.getOutputStream());
                in = new ObjectInputStream(clientsocket.getInputStream());
                handler.post(() -> cvStatus.setText("Connected\nServer IP Address: " + ServerIP));

            } catch (IOException e) {
                e.printStackTrace();
                handler.post(this::OfflineDialog);
            }

        }).start();

        // EXIT BUTTON
        cvExit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                    CloseApp terminate = new CloseApp();
                    terminate.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
            }
        });

        // SUBMIT RUN BUTTON
        cvRun.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                    showDialog();
            }
        });

        // SHOW STATS BUTTON
        cvStatistics.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                    showStatsDialog();
            }
        });
    }

    // UNABLE TO CONNECT POP UP
    private void OfflineDialog(){
        final Dialog dialog = new Dialog(MainActivity.this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.layout_exitpopup);
        dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        dialog.setCancelable(false);
        Button btnExit = dialog.findViewById(R.id.btnexit);
        btnExit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        dialog.show();
    }

    // SHOW STATS -> POP UP
    private void showStatsDialog(){
        final Dialog dialog = new Dialog(MainActivity.this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.layout_statspopup);
        dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        dialog.setCancelable(false);
        ImageView PopupBack = dialog.findViewById(R.id.statback);
        EditText ID = dialog.findViewById(R.id.statuserID);
        Button btnEnter = dialog.findViewById(R.id.statbtnEnter);
        PopupBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dialog.dismiss();
            }
        });
        btnEnter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (ID.getText().toString().isEmpty()) {
                    Toast.makeText(MainActivity.this, "Please ENTER user ID (eg 5) ", Toast.LENGTH_SHORT).show();
                } else {
                    String userID = ID.getText().toString();
                    ReceiveStatistics stats = new ReceiveStatistics(userID,dialog);
                    stats.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                }
            }
        });
        dialog.show();
    }

    // SUBMIT RUN BUTTON -> POP UP
    private void showDialog() {
        final Dialog dialog = new Dialog(MainActivity.this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.layout_popup);
        dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        dialog.setCancelable(false);

        ImageView PopupBack = dialog.findViewById(R.id.back);
        Button btnFileChooser = dialog.findViewById(R.id.btnChooser);
        EditText ID = dialog.findViewById(R.id.userID);
        Button btnEnter = dialog.findViewById(R.id.btnEnter);

        // BUTTON TO OPEN FILE EXPLORER
        btnFileChooser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openFileChooser();

            }
        });

        // BACK BUTTON TO RETURN TO MAIN SCREEN
        PopupBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dialog.dismiss();
            }
        });

        // OPEN FIELD TO TYPE USER ID
        btnEnter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Uri path = getPath();
                if (path == null) {
                    Toast.makeText(MainActivity.this, "Please SELECT .GPX FILE NAME ", Toast.LENGTH_SHORT).show();
                } else {
                    String userID = ID.getText().toString();
                    if (!userID.isEmpty()){
                        Toast.makeText(MainActivity.this, String.valueOf(path), Toast.LENGTH_SHORT).show();
                        if (isGPXFile(path)) {
                            SentGpxToServer send = new SentGpxToServer(path,userID);
                            send.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                            dialog.dismiss();
                        } else {
                            Toast.makeText(MainActivity.this, "Please SELECT A .GPX FILE ", Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        Toast.makeText(MainActivity.this, "Please provide a User ID ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });
        dialog.show();
    }

    // METHOD TO INVOKE FILE EXPLORER
    @SuppressWarnings("deprecation")
    private void openFileChooser() {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("*/*");
        startActivityForResult(intent, FILE_CHOOSER_REQUEST_CODE);

    }

    //FOLLOWING METHODS ARE USED TO RETRIEVE THE .GPX FILE AND SEND IT TO THE MASTER
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == FILE_CHOOSER_REQUEST_CODE && resultCode == RESULT_OK) {
            if (data != null && data.getData() != null) {
                Uri uri = data.getData();
                String selectedFilePath = uri.getPath();// Store the selected file path for later use
                if (selectedFilePath != null) {
                    setPath(uri);
                } else {
                    Toast.makeText(MainActivity.this, "Failed to retrieve file path", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    private boolean isGPXFile(Uri uri) {
        String extension = getFileExtension(uri);
        return extension != null && extension.equalsIgnoreCase(".gpx");
    }
    private String getFileExtension(Uri uri) {
        String filePath = uri.getPath();
        int dotIndex = filePath.lastIndexOf(".");
        if (dotIndex != -1 && dotIndex < filePath.length() - 1) {
            return filePath.substring(dotIndex);
        }
        return null;
    }
    private Uri filepath;
    private void setPath(Uri path) {
        filepath = path;
    }
    private Uri getPath() {
        return filepath;
    }


    // INVOKE WHEN SUBMIT RUN BUTTON IS PRESSED
    public  class SentGpxToServer extends AsyncTask<String, Void, String> {

        private final Uri gpxfile;
        private final String userID;
        @SuppressWarnings("deprecation")
        public SentGpxToServer(Uri gpxfile, String userID){

            this.gpxfile = gpxfile;
            this.userID = userID;
        }

        @Override
        @SuppressWarnings("deprecation")
        protected String doInBackground(String... voids) {
            String serverResponse = null;
            try {
                OutputStream outputStream = clientsocket.getOutputStream();
                out.writeUTF("submit"); // useroption
                out.flush();
                out.writeInt(Integer.parseInt(userID));
                out.flush();
                ContentResolver content = getContentResolver();
                InputStream gpx = content.openInputStream(gpxfile);
                long filesize = content.openAssetFileDescriptor(gpxfile, "r").getLength();
                DataOutputStream dataOutputStream = new DataOutputStream(outputStream);
                dataOutputStream.writeLong(filesize);
                dataOutputStream.flush();

                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = gpx.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                }
                outputStream.flush();
                serverResponse = in.readUTF();

            } catch (IOException e) {
                e.printStackTrace();
            }
            return serverResponse;
        }

        @SuppressWarnings("deprecation")
        protected void onPostExecute(String serverResponse){
            Toast.makeText(MainActivity.this, "Upload Successful", Toast.LENGTH_SHORT).show();
            Intent intent = new Intent(MainActivity.this, SubmitRunActivity.class);
            intent.putExtra("RunData", serverResponse);
            startActivity(intent);
        }
    }

    // INVOKE WHEN THE EXIT BUTTON IS PRESSED
    public  class CloseApp extends AsyncTask<Void, Void, Void> {
        @SuppressWarnings("deprecation")
        protected void onPreExecute(){
            Toast.makeText(MainActivity.this, "Closing", Toast.LENGTH_SHORT).show();
        }

        @Override
        @SuppressWarnings("deprecation")
        protected Void doInBackground(Void... voids) {
            try {
                out.writeUTF("exit");
                out.flush();
                in.close();
                out.close();
                clientsocket.close();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            return null;
        }
        @Override
        @SuppressWarnings("deprecation")
        protected void onPostExecute(Void aVoid) {
            finish();
        }
    }

    // INVOKE WHEN THE STATISTICS BUTTON IS PRESSED
    public  class ReceiveStatistics extends AsyncTask<String, Void, ArrayList<String>> {
        private final String userID;
        private final Dialog dialog;
        @SuppressWarnings("deprecation")
        public ReceiveStatistics(String userID, Dialog dialog){
            this.userID = userID;
            this.dialog = dialog;
        }

        @Override
        @SuppressWarnings("deprecation")
        protected ArrayList<String> doInBackground(String... voids) {
            ArrayList<String> data = new ArrayList<>();
            try {
                out.writeUTF("stats"); // useroption
                out.flush();
                out.writeInt(Integer.parseInt(userID));
                out.flush();
                if (in.readBoolean()) {
                    String userStats = in.readUTF();
                    String statsPercent = in.readUTF();
                    String globalStats = in.readUTF();
                    data.add(userStats);
                    data.add(statsPercent);
                    data.add(globalStats);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            return data;
        }

        @SuppressWarnings("deprecation")
        protected void onPostExecute(ArrayList<String> data){
            if (data.isEmpty()){
                dialog.dismiss();
                Toast.makeText(MainActivity.this, "No user found with this ID", Toast.LENGTH_SHORT).show();
            } else {
                dialog.dismiss();
                Toast.makeText(MainActivity.this, "Download Successful", Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(MainActivity.this, StatisticsActivity.class);
                intent.putStringArrayListExtra("Data", data);
                startActivity(intent);
            }
        }
    }
}