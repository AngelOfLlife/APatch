package me.bmax.apatch.ui.util

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

    // Create target bitmap with same aspect ratio as screen
    val displayMetrics = resources.displayMetrics
    val screenWidth = displayMetrics.widthPixels
    val screenHeight = displayMetrics.heightPixels
    val screenRatio = screenHeight.toFloat() / screenWidth.toFloat()

    // Calculate target dimensions
    val targetWidth: Int
    val targetHeight: Int
    if (width.toFloat() / height.toFloat() > screenRatio) {
        targetHeight = height
        targetWidth = (height / screenRatio).toInt()
    } else {
        targetWidth = width
        targetHeight = (width * screenRatio).toInt()
    }

    // Create bitmap with target dimensions
    val scaledBitmap = createBitmap(targetWidth, targetHeight)
    val canvas = Canvas(scaledBitmap)

    val matrix = Matrix()

    // Ensure scale value is valid
    val safeScale = maxOf(0.1f, transformation.scale)
    matrix.postScale(safeScale, safeScale)

    // Calculate offsets
    val widthDiff = (bitmap.width * safeScale - targetWidth)
    val heightDiff = (bitmap.height * safeScale - targetHeight)

    // Safe offset calculation
    val maxOffsetX = maxOf(0f, widthDiff / 2)
    val maxOffsetY = maxOf(0f, heightDiff / 2)

    // Limit offset range
    val safeOffsetX = if (maxOffsetX > 0)
        transformation.offsetX.coerceIn(-maxOffsetX, maxOffsetX) else 0f
    val safeOffsetY = if (maxOffsetY > 0)
        transformation.offsetY.coerceIn(-maxOffsetY, maxOffsetY) else 0f

    // Apply offset to matrix
    val translationX = -widthDiff / 2 + safeOffsetX
    val translationY = -heightDiff / 2 + safeOffsetY

    matrix.postTranslate(translationX, translationY)

    // Draw original bitmap to new bitmap
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

fun Context.saveCustomBackground(uri: Uri?) {
    val prefs = getSharedPreferences("settings", Context.MODE_PRIVATE)
    if (uri != null) {
        prefs.edit().putString("custom_background_uri", uri.toString()).apply()
    } else {
        prefs.edit().remove("custom_background_uri").apply()
    }
}

fun Context.getCustomBackgroundUri(): Uri? {
    val prefs = getSharedPreferences("settings", Context.MODE_PRIVATE)
    val uriString = prefs.getString("custom_background_uri", null)
    return uriString?.let { Uri.parse(it) }
}
