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
                var currentPage by remember { mutableStateOf<Page>(Page.Welcome) }
                var selectedFeature by remember { mutableStateOf<Feature?>(null) }

                when (currentPage) {
                    Page.Welcome -> WelcomePage { currentPage = Page.FeatureSelection }
                    Page.FeatureSelection -> FeatureSelectionPage {
                        selectedFeature = it
                        currentPage = Page.MainScreen
                    }
                    Page.MainScreen -> MainScreen(selectedFeature!!)
                }
            }
        }
    }
}

data class LaneDetectionData(
    val isCarTouchingRightLane: Boolean,
    val isCarTouchingLeftLane: Boolean
)

data class BlindSpotData(
    val isObjectDetectedOnRightBlindSpot: Boolean,
    val isObjectDetectedOnLeftBlindSpot: Boolean
)

data class TrafficLightData(
    val isRedLightDetected: Boolean
)

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


sealed class Page {
    object Welcome : Page()
    object FeatureSelection : Page()
    object MainScreen : Page()
}

sealed class Feature {
    object LaneDetection : Feature()
    object BlindSpot : Feature()
    object TrafficLight : Feature()
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
fun FeatureSelectionPage(onFeatureSelected: (Feature) -> Unit) {
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
                text = "Select a feature:",
                color = Color.Black
            )
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = { onFeatureSelected(Feature.LaneDetection) },
                modifier = Modifier.padding(16.dp),
            ) {
                Text(text = "Lane Detection", color = Color.White)
            }
            Button(
                onClick = { onFeatureSelected(Feature.BlindSpot) },
                modifier = Modifier.padding(16.dp),
            ) {
                Text(text = "Blind Spot Detection", color = Color.White)
            }
            Button(
                onClick = { onFeatureSelected(Feature.TrafficLight) },
                modifier = Modifier.padding(16.dp),
            ) {
                Text(text = "Traffic Light Recognition", color = Color.White)
            }
        }
    }
}

@Composable
fun MainScreen(selectedFeature: Feature) {
    // Mock data for each feature
    val isCarTouchingRightLane = true
    val isCarTouchingLeftLane = false
    val isObjectDetectedOnRightBlindSpot = false
    val isObjectDetectedOnLeftBlindSpot = true
    val isRedLightDetected = true


    Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
        Column {
            when (selectedFeature) {
                is Feature.LaneDetection -> LaneDetectionTab(isCarTouchingRightLane, isCarTouchingLeftLane)
                is Feature.BlindSpot -> BlindSpotTab(isObjectDetectedOnRightBlindSpot, isObjectDetectedOnLeftBlindSpot)
                is Feature.TrafficLight -> TrafficLightTab(isRedLightDetected)
            }
        }
    }
}
@Preview(showBackground = true)
@Composable
fun WelcomePagePreview() {
    MyApplicationTheme {
        WelcomePage(onContinueClick = {})
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenPreview() {
    MyApplicationTheme {
        MainScreen(selectedFeature = Feature.LaneDetection)
    }
}

@Preview(showBackground = true)
@Composable
fun LaneDetectionTabPreview() {
    MyApplicationTheme {
        LaneDetectionTab(isCarTouchingRightLane = true, isCarTouchingLeftLane = false)
    }
}

@Preview(showBackground = true)
@Composable
fun BlindSpotTabPreview() {
    MyApplicationTheme {
        BlindSpotTab(isObjectDetectedOnRightBlindSpot = false, isObjectDetectedOnLeftBlindSpot = true)
    }
}

@Preview(showBackground = true)
@Composable
fun TrafficLightTabPreview() {
    MyApplicationTheme {
        TrafficLightTab(isRedLightDetected = true)
    }
}
