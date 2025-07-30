package me.bmax.apatch.ui.theme

import android.net.Uri
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

/**
 * 主题配置对象，管理应用的主题相关状态
 */
object ThemeConfig {
    var customBackgroundUri by mutableStateOf<Uri?>(null)
    var forceDarkMode by mutableStateOf<Boolean?>(null)
    var currentTheme by mutableStateOf<ThemeColors>(ThemeColors.Default)
    var useDynamicColor by mutableStateOf(false)
    var backgroundImageLoaded by mutableStateOf(false)
    var needsResetOnThemeChange by mutableStateOf(false)
    var isThemeChanging by mutableStateOf(false)
    var preventBackgroundRefresh by mutableStateOf(false)

    private var lastDarkModeState: Boolean? = null
    fun detectThemeChange(currentDarkMode: Boolean): Boolean {
        val isChanged = lastDarkModeState != null && lastDarkModeState != currentDarkMode
        lastDarkModeState = currentDarkMode
        return isChanged
    }

    fun resetBackgroundState() {
        if (!preventBackgroundRefresh) {
            backgroundImageLoaded = false
        }
        isThemeChanging = true
    }
}

/**
 * 主题颜色枚举
 */
enum class ThemeColors(val displayName: String) {
    Default("Default"),
    Blue("Blue"),
    Green("Green"),
    Orange("Orange"),
    Purple("Purple"),
    Red("Red"),
    Teal("Teal"),
    Pink("Pink"),
    Indigo("Indigo"),
    Cyan("Cyan"),
    Lime("Lime"),
    Brown("Brown");

    companion object {
        fun fromName(name: String): ThemeColors {
            return values().find { it.name == name } ?: Default
        }
    }
}