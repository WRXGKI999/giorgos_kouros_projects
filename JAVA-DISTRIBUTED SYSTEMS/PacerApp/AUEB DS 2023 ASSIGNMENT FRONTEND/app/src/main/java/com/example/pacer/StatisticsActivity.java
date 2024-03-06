package com.example.pacer;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.text.SpannableStringBuilder;
import android.text.Spanned;
import android.text.style.AbsoluteSizeSpan;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.formatter.ValueFormatter;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class StatisticsActivity extends AppCompatActivity {

    ImageView ivBack;
    TextView userStats;
    TextView globalStats;
    TextView statsPercent;

    // STATISTICS SCREEN
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_statistics);
        getWindow().setStatusBarColor(ContextCompat.getColor(this, R.color.main));
        ivBack = findViewById(R.id.ivBack);
        BarChart chartDuration = findViewById(R.id.chartDuration);
        BarChart chartDistance = findViewById(R.id.chartDistance);
        BarChart chartElevationGain = findViewById(R.id.chartElevationGain);
        Intent intent = getIntent();
        ArrayList<String> Data = intent.getStringArrayListExtra("Data");
        String user = Data.get(0);
        userStats = findViewById(R.id.userStats);

        // BACK ARROW
        ivBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });

        // FOR USER STATS
        String[] pieces1 = user.split("-----");
        SpannableStringBuilder ssb1 = new SpannableStringBuilder();

        for (int i = 0; i < pieces1.length; i++) {

            String piece1 = pieces1[i];
            int start = ssb1.length();
            if (i == pieces1.length -1){
                ssb1.append(piece1);
            } else {
                ssb1.append(piece1).append("\n");
            }
            int end = ssb1.length();

            if (i % 2 == 0) {
                ssb1.setSpan(new AbsoluteSizeSpan(26, true), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            } else {
                ssb1.setSpan(new AbsoluteSizeSpan(12, true), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            }
        }
        userStats.setText(ssb1);

        // FOR TOTAL STATS
        String percentages = Data.get(2);
        globalStats = findViewById(R.id.globalStats);

        String[] pieces2 = percentages.split("-----");
        SpannableStringBuilder ssb2 = new SpannableStringBuilder();

        for (int i = 0; i < pieces2.length; i++) {

            String piece = pieces2[i];
            int start = ssb2.length();
            if (i == pieces2.length -1){
                ssb2.append(piece);
            } else {
                ssb2.append(piece).append("\n");
            }
            int end = ssb2.length();

            if (i % 2 == 0) {
                ssb2.setSpan(new AbsoluteSizeSpan(26, true), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            } else {
                ssb2.setSpan(new AbsoluteSizeSpan(12, true), start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            }
        }
        globalStats.setText(ssb2);


        // FOR STATS PERCENTAGES
        String global = Data.get(1);

        String regex = "[-+]?\\d*\\.\\d{2}";

        // Extracting chart data from the string "global"
        Pattern pattern = Pattern.compile(regex);

        Matcher matcher = pattern.matcher(global);

        double[] chartdata = new double[6];
        int count = 0;

        while (matcher.find() && count < 6) {
            String matchedDouble = matcher.group();
            chartdata[count] = Double.parseDouble(matchedDouble);
            global = global.replaceFirst(Pattern.quote(matchedDouble), "");
            count++;
        }

        double selectedUser_avgRouteDistance = chartdata[0];
        double selectedUser_avgElevationGain = chartdata[1];
        double selectedUser_avgDuration = chartdata[2];
        double usersAverage_avgRouteDistance = chartdata[3];
        double usersAverage_avgElevationGain = chartdata[4];
        double usersAverage_avgDuration = chartdata[5];
        statsPercent = findViewById(R.id.statsPercent);
        statsPercent.setText(global);

        // Setting up the charts
        setupChart(chartDistance, "Distance (km)");
        setupChart(chartDuration, "Duration (minutes)");
        setupChart(chartElevationGain, "Elevation Gain (m)");

        setupBarChartData(chartDistance, (float) selectedUser_avgRouteDistance, (float) usersAverage_avgRouteDistance);
        setupBarChartData(chartDuration, (float) selectedUser_avgDuration, (float) usersAverage_avgDuration);
        setupBarChartData(chartElevationGain, (float) selectedUser_avgElevationGain, (float) usersAverage_avgElevationGain);

        setupCommonSettings(chartDistance);
        setupCommonSettings(chartDuration);
        setupCommonSettings(chartElevationGain);
    }

    private void setupChart(BarChart chart, String xAxisLabel) {
        // Customize X axis
        XAxis xAxis = chart.getXAxis();
        xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
        xAxis.setGranularity(1f);
        xAxis.setTextColor(Color.WHITE);
        xAxis.setLabelCount(2);
        xAxis.setValueFormatter(new ValueFormatter() {
            @Override
            public String getAxisLabel(float value, AxisBase axis) {
                if (value == 0f) {
                    return "You";
                } else {
                    return "Global";
                }
            }
        });

        // Customize Y axis
        YAxis leftAxis = chart.getAxisLeft();
        leftAxis.setAxisMinimum(0f);
        leftAxis.setTextColor(Color.WHITE);
        leftAxis.setDrawGridLines(false);
        chart.getAxisRight().setEnabled(false);
    }

    private void setupBarChartData(BarChart chart, float selectedUserValue, float usersAverageValue) {
        List<BarEntry> entries = new ArrayList<>();
        entries.add(new BarEntry(0f, new float[]{selectedUserValue}));
        entries.add(new BarEntry(1f, new float[]{usersAverageValue}));

        BarDataSet dataSet = new BarDataSet(entries, "");
        dataSet.setColors(ColorTemplate.COLORFUL_COLORS);
        dataSet.setValueTextSize(12f);
        dataSet.setValueTextColor(Color.WHITE);
        dataSet.setDrawValues(true);

        BarData barData = new BarData(dataSet);
        chart.setData(barData);
    }

    private void setupCommonSettings(BarChart chart) {
        chart.getDescription().setEnabled(false);
        chart.getLegend().setEnabled(false);
        chart.invalidate();
    }
}