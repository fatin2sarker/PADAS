import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun LaneDetectionTab(isCarTouchingRightLane: Boolean, isCarTouchingLeftLane: Boolean) {
    Column {
        if (isCarTouchingRightLane || isCarTouchingLeftLane) {
            Text(text = "Warning: Car is touching the lane!")
        } else {
            Text(text = "Car is centered")
        }
    }
}
