package me.bmax.apatch.ui.theme

import android.content.Context
import androidx.compose.material3.CardDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

object CardConfig {
    var cardAlpha by mutableFloatStateOf(1f)
    var cardDim by mutableFloatStateOf(0f)
    var isCustomBackgroundEnabled by mutableStateOf(false)
    var isCustomAlphaSet by mutableStateOf(false)
    var isCustomDimSet by mutableStateOf(false)

    fun save(context: Context) {
        val prefs = context.getSharedPreferences("settings", Context.MODE_PRIVATE)
        with(prefs.edit()) {
            putFloat("card_alpha", cardAlpha)
            putFloat("card_dim", cardDim)
            putBoolean("custom_background_enabled", isCustomBackgroundEnabled)
            putBoolean("is_custom_alpha_set", isCustomAlphaSet)
            putBoolean("is_custom_dim_set", isCustomDimSet)
            apply()
        }
    }

    fun load(context: Context) {
        val prefs = context.getSharedPreferences("settings", Context.MODE_PRIVATE)
        cardAlpha = prefs.getFloat("card_alpha", 1f)
        cardDim = prefs.getFloat("card_dim", 0f)
        isCustomBackgroundEnabled = prefs.getBoolean("custom_background_enabled", false)
        isCustomAlphaSet = prefs.getBoolean("is_custom_alpha_set", false)
        isCustomDimSet = prefs.getBoolean("is_custom_dim_set", false)
    }
}

@Composable
fun getCardColors(originalColor: Color) = CardDefaults.cardColors(
    containerColor = originalColor.copy(alpha = CardConfig.cardAlpha),
    contentColor = Color.Unspecified
)