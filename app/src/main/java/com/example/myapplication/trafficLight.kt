import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun TrafficLightTab(isRedLightDetected: Boolean) {
    Column {
        if (isRedLightDetected) {
            Text(text = "Warning: Red light ahead!")
        } else {
            Text(text = "No red light detected ahead")
        }
    }
}
