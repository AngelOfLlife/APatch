package me.bmax.apatch.ui.component

import android.net.Uri
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import coil.compose.AsyncImage
import coil.request.ImageRequest
import me.bmax.apatch.R
import me.bmax.apatch.util.ui.BackgroundTransformation
import me.bmax.apatch.util.ui.saveTransformedBackground
import kotlinx.coroutines.launch
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.layout.onSizeChanged
import kotlin.math.max

@Composable
fun ImageEditorDialog(
    imageUri: Uri,
    onDismiss: () -> Unit,
    onConfirm: (Uri) -> Unit
) {
    var scale by remember { mutableFloatStateOf(1f) }
    var offsetX by remember { mutableFloatStateOf(0f) }
    var offsetY by remember { mutableFloatStateOf(0f) }
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var lastScale by remember { mutableFloatStateOf(1f) }
    var lastOffsetX by remember { mutableFloatStateOf(0f) }
    var lastOffsetY by remember { mutableFloatStateOf(0f) }
    var imageSize by remember { mutableStateOf(Size.Zero) }
    var screenSize by remember { mutableStateOf(Size.Zero) }
    val animatedScale by animateFloatAsState(
        targetValue = scale,
        label = "ScaleAnimation"
    )
    val animatedOffsetX by animateFloatAsState(
        targetValue = offsetX,
        label = "OffsetXAnimation"
    )
    val animatedOffsetY by animateFloatAsState(
        targetValue = offsetY,
        label = "OffsetYAnimation"
    )
    val updateTransformation = remember {
        { newScale: Float, newOffsetX: Float, newOffsetY: Float ->
            val scaleDiff = kotlin.math.abs(newScale - lastScale)
            val offsetXDiff = kotlin.math.abs(newOffsetX - lastOffsetX)
            val offsetYDiff = kotlin.math.abs(newOffsetY - lastOffsetY)
            if (scaleDiff > 0.01f || offsetXDiff > 1f || offsetYDiff > 1f) {
                scale = newScale
                offsetX = newOffsetX
                offsetY = newOffsetY
                lastScale = newScale
                lastOffsetX = newOffsetX
                lastOffsetY = newOffsetY
            }
        }
    }
    val scaleToFullScreen = remember {
        {
            if (imageSize.height > 0 && screenSize.height > 0) {
                val newScale = screenSize.height / imageSize.height
                updateTransformation(newScale, 0f, 0f)
            }
        }
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(
            dismissOnBackPress = true,
            dismissOnClickOutside = false,
            usePlatformDefaultWidth = false
        )
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.9f))
        ) {
            // 顶部工具栏
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.Black.copy(alpha = 0.6f))
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(
                    onClick = onDismiss,
                    modifier = Modifier
                        .size(40.dp)
                        .background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(8.dp))
                ) {
                    Icon(
                        Icons.Default.Close,
                        contentDescription = stringResource(R.string.settings_custom_background),
                        tint = Color.White
                    )
                }

                IconButton(
                    onClick = scaleToFullScreen,
                    modifier = Modifier
                        .size(40.dp)
                        .background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(8.dp))
                ) {
                    Icon(
                        Icons.Default.Fullscreen,
                        contentDescription = null,
                        tint = Color.White
                    )
                }

                IconButton(
                    onClick = {
                        scope.launch {
                            val transformation = BackgroundTransformation(scale, offsetX, offsetY)
                            val transformedUri = context.saveTransformedBackground(imageUri, transformation)
                            transformedUri?.let { onConfirm(it) }
                        }
                    },
                    modifier = Modifier
                        .size(40.dp)
                        .background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(8.dp))
                ) {
                    Icon(
                        Icons.Default.Check,
                        contentDescription = null,
                        tint = Color.White
                    )
                }
            }

            // 图像区域
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(top = 80.dp, bottom = 80.dp)
                    .onSizeChanged { screenSize = it }
            ) {
                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current)
                        .data(imageUri)
                        .crossfade(true)
                        .build(),
                    contentDescription = null,
                    modifier = Modifier
                        .fillMaxSize()
                        .graphicsLayer(
                            scaleX = animatedScale,
                            scaleY = animatedScale,
                            translationX = animatedOffsetX,
                            translationY = animatedOffsetY
                        )
                        .pointerInput(Unit) {
                            detectTransformGestures { _, pan, zoom, _ ->
                                val newScale = (scale * zoom).coerceIn(0.1f, 5f)
                                val newOffsetX = offsetX + pan.x
                                val newOffsetY = offsetY + pan.y
                                updateTransformation(newScale, newOffsetX, newOffsetY)
                            }
                        }
                        .onSizeChanged { imageSize = it },
                    contentScale = ContentScale.Fit
                )
            }

            // 底部 инструкции
            Box(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
                    .background(Color.Black.copy(alpha = 0.6f))
                    .padding(16.dp)
            ) {
                Text(
                    text = stringResource(R.string.image_editor_instructions),
                    color = Color.White,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}