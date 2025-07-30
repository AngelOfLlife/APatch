package me.bmax.apatch.util.ui

import android.content.ContentResolver
import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Matrix
import android.net.Uri
import android.util.Log
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import androidx.core.graphics.createBitmap
import androidx.core.content.edit
import androidx.core.net.toUri
import me.bmax.apatch.ui.theme.CardConfig
import me.bmax.apatch.ui.theme.ThemeConfig
import androidx.compose.ui.unit.dp

data class BackgroundTransformation(
    val scale: Float = 1f,
    val offsetX: Float = 0f,
    val offsetY: Float = 0f
)

fun Context.getImageBitmap(uri: Uri): Bitmap? {
    return try {
        val contentResolver: ContentResolver = contentResolver
        val inputStream: InputStream = contentResolver.openInputStream(uri) ?: return null
        val bitmap = BitmapFactory.decodeStream(inputStream)
        inputStream.close()
        bitmap
    } catch (e: Exception) {
        Log.e("BackgroundUtils", "Failed to get image bitmap: ${e.message}")
        null
    }
}

fun Context.applyTransformationToBitmap(bitmap: Bitmap, transformation: BackgroundTransformation): Bitmap {
    val width = bitmap.width
    val height = bitmap.height

    // 创建与屏幕比例相同的目标位图
    val displayMetrics = resources.displayMetrics
    val screenWidth = displayMetrics.widthPixels
    val screenHeight = displayMetrics.heightPixels
    val screenRatio = screenHeight.toFloat() / screenWidth.toFloat()

    // 计算目标宽高
    val targetWidth: Int
    val targetHeight: Int
    if (width.toFloat() / height.toFloat() > screenRatio) {
        targetHeight = height
        targetWidth = (height / screenRatio).toInt()
    } else {
        targetWidth = width
        targetHeight = (width * screenRatio).toInt()
    }

    // 创建与目标相同大小的位图
    val scaledBitmap = createBitmap(targetWidth, targetHeight)
    val canvas = Canvas(scaledBitmap)

    val matrix = Matrix()

    // 确保缩放值有效
    val safeScale = maxOf(0.1f, transformation.scale)
    matrix.postScale(safeScale, safeScale)

    // 计算偏移量，确保不会出现负最大值的问题
    val widthDiff = (bitmap.width * safeScale - targetWidth)
    val heightDiff = (bitmap.height * safeScale - targetHeight)

    // 安全计算偏移量边界
    val maxOffsetX = maxOf(0f, widthDiff / 2)
    val maxOffsetY = maxOf(0f, heightDiff / 2)

    // 限制偏移范围
    val safeOffsetX = if (maxOffsetX > 0)
        transformation.offsetX.coerceIn(-maxOffsetX, maxOffsetX) else 0f
    val safeOffsetY = if (maxOffsetY > 0)
        transformation.offsetY.coerceIn(-maxOffsetY, maxOffsetY) else 0f

    // 应用偏移量到矩阵
    val translationX = -widthDiff / 2 + safeOffsetX
    val translationY = -heightDiff / 2 + safeOffsetY

    matrix.postTranslate(translationX, translationY)

    // 将原始位图绘制到新位图上
    canvas.drawBitmap(bitmap, matrix, null)

    return scaledBitmap
}

fun Context.saveTransformedBackground(uri: Uri, transformation: BackgroundTransformation): Uri? {
    try {
        val bitmap = getImageBitmap(uri) ?: return null
        val transformedBitmap = applyTransformationToBitmap(bitmap, transformation)

        val fileName = "custom_background_transformed.jpg"
        val file = File(filesDir, fileName)
        val outputStream = FileOutputStream(file)

        transformedBitmap.compress(Bitmap.CompressFormat.JPEG, 90, outputStream)
        outputStream.flush()
        outputStream.close()

        return Uri.fromFile(file)
    } catch (e: Exception) {
        Log.e("BackgroundUtils", "Failed to save transformed image: ${e.message}", e)
        return null
    }
}

/**
 * 复制图片到内部存储
 */
fun Context.copyImageToInternalStorage(uri: Uri): Uri? {
    return try {
        val inputStream = contentResolver.openInputStream(uri) ?: return null
        val fileName = "custom_background.jpg"
        val file = File(filesDir, fileName)
        val outputStream = FileOutputStream(file)

        inputStream.copyTo(outputStream)
        inputStream.close()
        outputStream.close()

        Uri.fromFile(file)
    } catch (e: Exception) {
        Log.e("BackgroundUtils", "Failed to copy image: ${e.message}", e)
        null
    }
}

/**
 * 保存自定义背景
 */
fun Context.saveCustomBackground(uri: Uri?) {
    val newUri = uri?.let { copyImageToInternalStorage(it) }

    // 保存到配置文件
    getSharedPreferences("theme_prefs", Context.MODE_PRIVATE)
        .edit {
            putString("custom_background", newUri?.toString())
            if (uri == null) {
                // 如果清除背景，也重置阻止刷新标志
                putBoolean("prevent_background_refresh", false)
            } else {
                // 设置阻止刷新标志为false，允许新设置的背景加载一次
                putBoolean("prevent_background_refresh", false)
            }
        }

    ThemeConfig.customBackgroundUri = newUri
    ThemeConfig.backgroundImageLoaded = false
    ThemeConfig.preventBackgroundRefresh = false

    if (uri != null) {
        CardConfig.cardElevation = 0.dp
        CardConfig.isCustomBackgroundEnabled = true
    }
}

/**
 * 加载自定义背景
 */
fun Context.loadCustomBackground() {
    val uriString = getSharedPreferences("theme_prefs", Context.MODE_PRIVATE)
        .getString("custom_background", null)

    val newUri = uriString?.toUri()
    val preventRefresh = getSharedPreferences("theme_prefs", Context.MODE_PRIVATE)
        .getBoolean("prevent_background_refresh", false)

    ThemeConfig.preventBackgroundRefresh = preventRefresh

    if (!preventRefresh || ThemeConfig.customBackgroundUri?.toString() != newUri?.toString()) {
        Log.d("ThemeSystem", "Loading custom background: $uriString, prevent refresh: $preventRefresh")
        ThemeConfig.customBackgroundUri = newUri
        ThemeConfig.backgroundImageLoaded = false
    }
}