import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun BlindSpotTab(isObjectDetectedOnRightBlindSpot: Boolean, isObjectDetectedOnLeftBlindSpot: Boolean) {
    Column {
        if (isObjectDetectedOnRightBlindSpot) {
            Text(text = "Warning: Object detected on the right blind spot!")
        } else if (isObjectDetectedOnLeftBlindSpot) {
            Text(text = "Warning: Object detected on the left blind spot!")
        } else {
            Text(text = "No objects detected in the blind spots")
        }
    }
}
