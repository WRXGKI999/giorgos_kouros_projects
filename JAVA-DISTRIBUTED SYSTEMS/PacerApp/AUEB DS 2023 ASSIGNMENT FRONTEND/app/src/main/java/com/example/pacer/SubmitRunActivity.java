package com.example.pacer;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.content.Intent;
import android.os.Bundle;
import android.text.SpannableStringBuilder;
import android.text.Spanned;
import android.text.style.AbsoluteSizeSpan;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

public class SubmitRunActivity extends AppCompatActivity {
    ImageView ivBack;
    TextView stats;

    // SUBMIT RUN SCREEN
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_submit_run);
        getWindow().setStatusBarColor(ContextCompat.getColor(this, R.color.main));
        ivBack = findViewById(R.id.ivBack);
        Intent intent = getIntent();
        String RunData = intent.getStringExtra("RunData");
        stats = findViewById(R.id.stats);

        // FOR CURRENT ROUTE DATA
        String[] pieces = RunData.split("-----");
        SpannableStringBuilder ssb = new SpannableStringBuilder();

        for (int i = 0; i < pieces.length; i++) {
            String piece = pieces[i];
            int start = ssb.length();
            if (i == pieces.length -1){
                ssb.append(piece);
            } else {
                ssb.append(piece).append("\n");
            }
            int end = ssb.length();
            if (i % 2 == 0) {
                ssb.setSpan(new AbsoluteSizeSpan(35, true), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            } else {
                ssb.setSpan(new AbsoluteSizeSpan(16, true), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            }
        }
        stats.setText(ssb);

        // BACK ARROW
        ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });
    }

    @Override
    public void onBackPressed() {
        Intent intent = new Intent(SubmitRunActivity.this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        startActivity(intent);
    }
}