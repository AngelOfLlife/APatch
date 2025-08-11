package me.bmax.apatch.ui.theme

import android.content.Context
import android.net.Uri
import android.os.Build
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.livedata.observeAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.paint
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.MutableLiveData
import coil.compose.AsyncImagePainter
import coil.compose.rememberAsyncImagePainter
import me.bmax.apatch.APApplication
import java.io.File

@Composable
private fun SystemBarStyle(
    darkMode: Boolean,
    statusBarScrim: Color = Color.Transparent,
    navigationBarScrim: Color = Color.Transparent
) {
    val context = LocalContext.current
    val activity = context as ComponentActivity

    SideEffect {
        activity.enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.auto(
                statusBarScrim.toArgb(),
                statusBarScrim.toArgb(),
            ) { darkMode }, navigationBarStyle = when {
                darkMode -> SystemBarStyle.dark(
                    navigationBarScrim.toArgb()
                )

                else -> SystemBarStyle.light(
                    navigationBarScrim.toArgb(),
                    navigationBarScrim.toArgb(),
                )
            }
        )
    }
}

val refreshTheme = MutableLiveData(false)

object ThemeConfig {
    var customBackgroundUri by mutableStateOf<Uri?>(null)
    var backgroundImageLoaded by mutableStateOf(false)
}

@Composable
fun APatchTheme(
    content: @Composable () -> Unit
) {
    val context = LocalContext.current
    val prefs = APApplication.sharedPreferences

    var darkThemeFollowSys by remember { mutableStateOf(prefs.getBoolean("night_mode_follow_sys", true)) }
    var nightModeEnabled by remember { mutableStateOf(prefs.getBoolean("night_mode_enabled", false)) }
    var dynamicColor by remember {
        mutableStateOf(
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) prefs.getBoolean("use_system_color_theme", true) else false
        )
    }
    var customColorScheme by remember { mutableStateOf(prefs.getString("custom_color", "blue")) }

    val refreshThemeObserver by refreshTheme.observeAsState(false)
    if (refreshThemeObserver == true) {
        darkThemeFollowSys = prefs.getBoolean("night_mode_follow_sys", true)
        nightModeEnabled = prefs.getBoolean("night_mode_enabled", false)
        dynamicColor = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) prefs.getBoolean("use_system_color_theme", true) else false
        customColorScheme = prefs.getString("custom_color", "blue")
        refreshTheme.postValue(false)
    }

    val darkTheme = if (darkThemeFollowSys) isSystemInDarkTheme() else nightModeEnabled

    val baseScheme = if (!dynamicColor) {
        if (darkTheme) DarkColorScheme(customColorScheme) else LightColorScheme(customColorScheme)
    } else {
        when {
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
                if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
            }
            darkTheme -> DarkColorScheme("blue")
            else -> LightColorScheme("blue")
        }
    }

    LaunchedEffect(Unit) {
        CardConfig.load(context)
        loadCustomBackground(context)
    }

    val backgroundUri = rememberSaveable { mutableStateOf(ThemeConfig.customBackgroundUri) }
    LaunchedEffect(ThemeConfig.customBackgroundUri) { backgroundUri.value = ThemeConfig.customBackgroundUri }

    val painter = backgroundUri.value?.let {
        rememberAsyncImagePainter(model = it, onSuccess = { ThemeConfig.backgroundImageLoaded = true })
    }

    // Interpret slider as transparency percent (0..1); convert to actual alpha that surfaces should use
    val effectiveAlpha = remember(CardConfig.cardAlpha) { 1f - CardConfig.cardAlpha }
    val scheme = remember(baseScheme, effectiveAlpha, CardConfig.isCustomBackgroundEnabled) {
        applyAlphaToSurfaces(baseScheme, effectiveAlpha, CardConfig.isCustomBackgroundEnabled)
    }

    SystemBarStyle(darkMode = darkTheme, statusBarScrim = Color.Transparent, navigationBarScrim = Color.Transparent)

    MaterialTheme(colorScheme = scheme, typography = Typography) {
        Box(modifier = Modifier.fillMaxSize()) {
            if (ThemeConfig.customBackgroundUri != null) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .paint(painter = painter ?: rememberAsyncImagePainter(model = ThemeConfig.customBackgroundUri), contentScale = ContentScale.Crop)
                        .graphicsLayer { alpha = if (ThemeConfig.backgroundImageLoaded) 1f else 0f }
                )

                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = CardConfig.cardDim))
                )

                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                            Brush.radialGradient(
                                colors = listOf(Color.Transparent, if (darkTheme) Color.Black.copy(alpha = 0.5f + CardConfig.cardDim * 0.2f) else Color.Black.copy(alpha = 0.2f + CardConfig.cardDim * 0.1f)),
                                radius = 1200f
                            )
                        )
                )
            }

            Box(modifier = Modifier.fillMaxSize().alpha(1f)) { content() }
        }
    }
}

private fun DarkColorScheme(name: String?): ColorScheme = when (name) {
    "amber" -> DarkAmberTheme
    "blue_grey" -> DarkBlueGreyTheme
    "blue" -> DarkBlueTheme
    "brown" -> DarkBrownTheme
    "cyan" -> DarkCyanTheme
    "deep_orange" -> DarkDeepOrangeTheme
    "deep_purple" -> DarkDeepPurpleTheme
    "green" -> DarkGreenTheme
    "indigo" -> DarkIndigoTheme
    "light_blue" -> DarkLightBlueTheme
    "light_green" -> DarkLightGreenTheme
    "lime" -> DarkLimeTheme
    "orange" -> DarkOrangeTheme
    "pink" -> DarkPinkTheme
    "purple" -> DarkPurpleTheme
    "red" -> DarkRedTheme
    "sakura" -> DarkSakuraTheme
    "teal" -> DarkTealTheme
    "yellow" -> DarkYellowTheme
    else -> DarkBlueTheme
}

private fun LightColorScheme(name: String?): ColorScheme = when (name) {
    "amber" -> LightAmberTheme
    "blue_grey" -> LightBlueGreyTheme
    "blue" -> LightBlueTheme
    "brown" -> LightBrownTheme
    "cyan" -> LightCyanTheme
    "deep_orange" -> LightDeepOrangeTheme
    "deep_purple" -> LightDeepPurpleTheme
    "green" -> LightGreenTheme
    "indigo" -> LightIndigoTheme
    "light_blue" -> LightLightBlueTheme
    "light_green" -> LightLightGreenTheme
    "lime" -> LightLimeTheme
    "orange" -> LightOrangeTheme
    "pink" -> LightPinkTheme
    "purple" -> LightPurpleTheme
    "red" -> LightRedTheme
    "sakura" -> LightSakuraTheme
    "teal" -> LightTealTheme
    "yellow" -> LightYellowTheme
    else -> LightBlueTheme
}

private fun applyAlphaToSurfaces(base: ColorScheme, alpha: Float, transparentBg: Boolean): ColorScheme {
    fun Color.maybeTransparent(): Color = if (transparentBg) this.copy(alpha = alpha) else this
    return base.copy(
        background = base.background.maybeTransparent(),
        surface = base.surface.maybeTransparent(),
        surfaceVariant = base.surfaceVariant.maybeTransparent(),
        surfaceContainer = base.surfaceContainer.maybeTransparent(),
        surfaceContainerHigh = base.surfaceContainerHigh.maybeTransparent(),
        surfaceContainerHighest = base.surfaceContainerHighest.maybeTransparent(),
        surfaceContainerLow = base.surfaceContainerLow.maybeTransparent(),
        surfaceContainerLowest = base.surfaceContainerLowest.maybeTransparent(),
        outline = base.outline.copy(alpha = if (transparentBg) alpha else base.outline.alpha),
        outlineVariant = base.outlineVariant.copy(alpha = if (transparentBg) alpha else base.outlineVariant.alpha),
        primaryContainer = base.primaryContainer.maybeTransparent(),
        secondaryContainer = base.secondaryContainer.maybeTransparent(),
        tertiaryContainer = base.tertiaryContainer.maybeTransparent()
    )
}

private fun loadCustomBackground(context: Context) {
    val uri = context.getSharedPreferences("theme_prefs", Context.MODE_PRIVATE)
        .getString("custom_background", null)
        ?.let { Uri.parse(it) }
    ThemeConfig.customBackgroundUri = uri
    CardConfig.isCustomBackgroundEnabled = uri != null
}

fun Context.saveCustomBackground(uri: Uri?) {
    val newUri = uri?.let { copyImageToInternalStorage(it) }
    getSharedPreferences("theme_prefs", Context.MODE_PRIVATE).edit().putString("custom_background", newUri?.toString()).apply()
    ThemeConfig.customBackgroundUri = newUri
    CardConfig.isCustomBackgroundEnabled = newUri != null
}

private fun Context.copyImageToInternalStorage(uri: Uri): Uri? {
    return try {
        val input = contentResolver.openInputStream(uri) ?: return null
        val file = File(filesDir, "custom_background.jpg")
        file.outputStream().use { out -> input.copyTo(out) }
        Uri.fromFile(file)
    } catch (_: Exception) { null }
}
