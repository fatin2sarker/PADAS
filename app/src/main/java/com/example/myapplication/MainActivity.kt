package com.example.myapplication

import androidx.compose.runtime.Composable
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.example.myapplication.ui.theme.Purple80
import com.example.myapplication.ui.theme.MyApplicationTheme

import androidx.compose.ui.tooling.preview.Preview

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplicationTheme {
                var isWelcomePageVisible by remember { mutableStateOf(true) }

                if (isWelcomePageVisible) {
                    WelcomePage(onContinueClick = { isWelcomePageVisible = false })
                } else {
                    MainScreen()
                }
            }
        }
    }
}

@Composable
fun LaneDetectionTab(isCarTouchingRightLane: Boolean, isCarTouchingLeftLane: Boolean) {
    val alertColor = if (isCarTouchingRightLane || isCarTouchingLeftLane) Color.Red else Color.Green
    val alertText = if (isCarTouchingRightLane || isCarTouchingLeftLane) "Warning: Car is touching the lane!" else "Car is centered"
    Column {
        Text(text = alertText, color = alertColor)
    }
}

@Composable
fun BlindSpotTab(isObjectDetectedOnRightBlindSpot: Boolean, isObjectDetectedOnLeftBlindSpot: Boolean) {
    val alertColor = if (isObjectDetectedOnRightBlindSpot || isObjectDetectedOnLeftBlindSpot) Color.Red else Color.Green
    val alertText = if (isObjectDetectedOnRightBlindSpot) "Warning: Object detected on the right blind spot!" else if (isObjectDetectedOnLeftBlindSpot) "Warning: Object detected on the left blind spot!" else "No objects detected in the blind spots"
    Column {
        Text(text = alertText, color = alertColor)
    }
}

@Composable
fun TrafficLightTab(isRedLightDetected: Boolean) {
    val alertColor = if (isRedLightDetected) Color.Red else Color.Green
    val alertText = if (isRedLightDetected) "Warning: Red light ahead!" else "No red light detected ahead"
    Column {
        Text(text = alertText, color = alertColor)
    }
}

@Composable
fun WelcomePage(onContinueClick: () -> Unit) {
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Welcome to PADAS",
                color = Color.Black
            )
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = onContinueClick,
                modifier = Modifier.padding(16.dp),
            ) {
                Text(text = "Continue", color = Color.White)
            }
        }
    }
}

@Composable
fun MainScreen() {
    // Mock data, replace with actual data from sensors
    val isCarTouchingRightLane = true
    val isCarTouchingLeftLane = false
    val isObjectDetectedOnRightBlindSpot = false
    val isObjectDetectedOnLeftBlindSpot = true
    val isRedLightDetected = true

    // State variable for selected tab index
    var selectedTabIndex by remember { mutableStateOf(0) }

    Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
        Column {
            // Tabs
            TabRow(
                selectedTabIndex = selectedTabIndex,
                modifier = Modifier.fillMaxWidth(),
            ) {
                Tab(
                    text = { Text("Lane Detection") },
                    selected = selectedTabIndex == 0,
                    onClick = { selectedTabIndex = 0 }
                )
                Tab(
                    text = { Text("Blind Spot") },
                    selected = selectedTabIndex == 1,
                    onClick = { selectedTabIndex = 1 }
                )
                Tab(
                    text = { Text("Traffic Light") },
                    selected = selectedTabIndex == 2,
                    onClick = { selectedTabIndex = 2 }
                )
            }

            // Tab content based on the selected tab
            when (selectedTabIndex) {
                0 -> LaneDetectionTab(isCarTouchingRightLane, isCarTouchingLeftLane)
                1 -> BlindSpotTab(isObjectDetectedOnRightBlindSpot, isObjectDetectedOnLeftBlindSpot)
                2 -> TrafficLightTab(isRedLightDetected)
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenPreview() {
    MyApplicationTheme {
        MainScreen()
    }
}

@Preview(showBackground = true)
@Composable
fun WelcomePagePreview() {
    MyApplicationTheme {
        WelcomePage(onContinueClick = {})
    }
}