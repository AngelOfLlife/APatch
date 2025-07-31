package me.bmax.apatch.ui.theme

import android.content.SharedPreferences
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.ColorMatrix
import androidx.compose.ui.platform.LocalContext
import me.bmax.apatch.APApplication

data class UICustomizationState(
    val backgroundImageUri: String = "",
    val interfaceTransparency: Float = 1.0f,
    val backgroundBrightness: Float = 1.0f,
    val isEnabled: Boolean = true
)

object UICustomizationManager {
    private var _state = mutableStateOf(UICustomizationState())
    val state: androidx.compose.runtime.State<UICustomizationState> = _state

    fun loadSettings(prefs: SharedPreferences) {
        _state.value = UICustomizationState(
            backgroundImageUri = prefs.getString("background_image_uri", "") ?: "",
            interfaceTransparency = prefs.getFloat("interface_transparency", 1.0f),
            backgroundBrightness = prefs.getFloat("background_brightness", 1.0f),
            isEnabled = prefs.getBoolean("ui_customization_enabled", true)
        )
    }

    fun updateBackgroundImage(uri: String, prefs: SharedPreferences) {
        prefs.edit().putString("background_image_uri", uri).apply()
        _state.value = _state.value.copy(backgroundImageUri = uri)
    }

    fun updateTransparency(transparency: Float, prefs: SharedPreferences) {
        prefs.edit().putFloat("interface_transparency", transparency).apply()
        _state.value = _state.value.copy(interfaceTransparency = transparency)
    }

    fun updateBrightness(brightness: Float, prefs: SharedPreferences) {
        prefs.edit().putFloat("background_brightness", brightness).apply()
        _state.value = _state.value.copy(backgroundBrightness = brightness)
    }

    fun toggleEnabled(enabled: Boolean, prefs: SharedPreferences) {
        prefs.edit().putBoolean("ui_customization_enabled", enabled).apply()
        _state.value = _state.value.copy(isEnabled = enabled)
    }

    fun createBrightnessColorFilter(brightness: Float): ColorFilter? {
        if (brightness >= 0.99f) return null
        
        val matrix = ColorMatrix().apply {
            setScale(brightness, brightness, brightness, 1f)
        }
        return ColorFilter.colorMatrix(matrix)
    }

    fun getInterfaceAlpha(baseAlpha: Float = 1f): Float {
        return if (_state.value.isEnabled) {
            baseAlpha * _state.value.interfaceTransparency
        } else baseAlpha
    }
}

@Composable
fun InitializeUICustomization() {
    val context = LocalContext.current
    val prefs = remember { APApplication.sharedPreferences }
    
    LaunchedEffect(Unit) {
        UICustomizationManager.loadSettings(prefs)
    }
}

@Composable
fun rememberUICustomizationState(): UICustomizationState {
    val context = LocalContext.current
    val prefs = remember { APApplication.sharedPreferences }
    var state by remember { mutableStateOf(UICustomizationState()) }
    
    LaunchedEffect(Unit) {
        state = UICustomizationState(
            backgroundImageUri = prefs.getString("background_image_uri", "") ?: "",
            interfaceTransparency = prefs.getFloat("interface_transparency", 1.0f),
            backgroundBrightness = prefs.getFloat("background_brightness", 1.0f),
            isEnabled = prefs.getBoolean("ui_customization_enabled", true)
        )
    }
    
    return state
}