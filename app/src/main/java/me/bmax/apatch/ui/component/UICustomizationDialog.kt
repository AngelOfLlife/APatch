package me.bmax.apatch.ui.component

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Brightness6
import androidx.compose.material.icons.filled.CenterFocusStrong
import androidx.compose.material.icons.filled.Opacity
import androidx.compose.material.icons.filled.PhotoSizeSelectLarge
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.DialogProperties
import coil.compose.rememberAsyncImagePainter
import me.bmax.apatch.R
import me.bmax.apatch.ui.theme.UICustomizationManager

@Composable
fun UICustomizationDialog(
    showDialog: Boolean,
    onDismiss: () -> Unit,
    backgroundImageUri: String?,
    transparency: Float,
    brightness: Float,
    onTransparencyChange: (Float) -> Unit,
    onBrightnessChange: (Float) -> Unit,
    onScalePositionReset: () -> Unit
) {
    if (showDialog) {
        AlertDialog(
            onDismissRequest = onDismiss,
            properties = DialogProperties(usePlatformDefaultWidth = false),
            modifier = Modifier.padding(16.dp),
            title = {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Icon(
                        Icons.Filled.Tune,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Text(
                        text = stringResource(id = R.string.ui_customization),
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            text = {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState()),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // Background Preview
                    if (!backgroundImageUri.isNullOrEmpty()) {
                        Text(
                            text = "Preview",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Medium
                        )
                        
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(120.dp),
                            shape = RoundedCornerShape(12.dp),
                            colors = CardDefaults.cardColors(
                                containerColor = MaterialTheme.colorScheme.surfaceVariant
                            )
                        ) {
                            Box(modifier = Modifier.fillMaxWidth()) {
                                Image(
                                    painter = rememberAsyncImagePainter(backgroundImageUri),
                                    contentDescription = "Background Preview",
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(120.dp)
                                        .alpha(0.8f),
                                    contentScale = ContentScale.Crop,
                                    colorFilter = UICustomizationManager.createBrightnessColorFilter(brightness)
                                )
                                
                                // Interface preview overlay
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .background(
                                            MaterialTheme.colorScheme.surface.copy(
                                                alpha = UICustomizationManager.getInterfaceAlpha(0.9f)
                                            ),
                                            RoundedCornerShape(bottomStart = 12.dp, bottomEnd = 12.dp)
                                        )
                                        .padding(8.dp)
                                        .align(Alignment.BottomCenter)
                                ) {
                                    Text(
                                        text = "Interface Preview",
                                        style = MaterialTheme.typography.bodySmall,
                                        modifier = Modifier.align(Alignment.Center)
                                    )
                                }
                            }
                        }
                    }
                    
                    // Transparency Control
                    CustomSliderItem(
                        icon = Icons.Filled.Opacity,
                        title = stringResource(id = R.string.ui_interface_transparency),
                        summary = "Adjust transparency of all UI elements",
                        value = transparency,
                        onValueChange = onTransparencyChange,
                        valueRange = 0.1f..1.0f,
                        steps = 18,
                        modifier = Modifier.fillMaxWidth()
                    )
                    
                    // Brightness Control
                    if (!backgroundImageUri.isNullOrEmpty()) {
                        CustomSliderItem(
                            icon = Icons.Filled.Brightness6,
                            title = stringResource(id = R.string.ui_background_brightness),
                            summary = "Adjust brightness of background image",
                            value = brightness,
                            onValueChange = onBrightnessChange,
                            valueRange = 0.1f..1.0f,
                            steps = 18,
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                    
                    // Scale and Position Controls
                    if (!backgroundImageUri.isNullOrEmpty()) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                Icons.Filled.PhotoSizeSelectLarge,
                                contentDescription = null,
                                modifier = Modifier.size(24.dp),
                                tint = MaterialTheme.colorScheme.onSurface
                            )
                            
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = stringResource(id = R.string.ui_scale_and_position),
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.Medium
                                )
                                Text(
                                    text = "Advanced image positioning controls",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                            
                            OutlinedButton(
                                onClick = onScalePositionReset,
                                modifier = Modifier.size(height = 36.dp, width = 100.dp)
                            ) {
                                Icon(
                                    Icons.Filled.Refresh,
                                    contentDescription = stringResource(id = R.string.ui_reset_scale_position),
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.padding(2.dp))
                                Text(
                                    text = "Reset",
                                    style = MaterialTheme.typography.labelSmall
                                )
                            }
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = onDismiss) {
                    Text("Done")
                }
            },
            dismissButton = {
                TextButton(onClick = onDismiss) {
                    Text("Cancel")
                }
            }
        )
    }
}

@Composable
fun ScalePositionControlDialog(
    showDialog: Boolean,
    onDismiss: () -> Unit,
    imageScale: Float,
    positionX: Float,
    positionY: Float,
    onScaleChange: (Float) -> Unit,
    onPositionChange: (Float, Float) -> Unit,
    onReset: () -> Unit
) {
    var scale by remember { mutableFloatStateOf(imageScale) }
    var offsetX by remember { mutableFloatStateOf(positionX) }
    var offsetY by remember { mutableFloatStateOf(positionY) }

    if (showDialog) {
        AlertDialog(
            onDismissRequest = onDismiss,
            title = {
                Text(
                    text = stringResource(id = R.string.ui_scale_and_position),
                    style = MaterialTheme.typography.headlineSmall
                )
            },
            text = {
                Column(
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // Scale Control
                    CustomSliderItem(
                        icon = Icons.Filled.PhotoSizeSelectLarge,
                        title = "Scale",
                        summary = "Adjust image scale",
                        value = scale,
                        onValueChange = { 
                            scale = it
                            onScaleChange(it)
                        },
                        valueRange = 0.5f..2.0f,
                        steps = 30
                    )
                    
                    // Position X Control
                    CustomSliderItem(
                        icon = Icons.Filled.CenterFocusStrong,
                        title = "Horizontal Position",
                        summary = "Adjust horizontal position",
                        value = offsetX,
                        onValueChange = { 
                            offsetX = it
                            onPositionChange(it, offsetY)
                        },
                        valueRange = -1.0f..1.0f,
                        steps = 40
                    )
                    
                    // Position Y Control
                    CustomSliderItem(
                        icon = Icons.Filled.CenterFocusStrong,
                        title = "Vertical Position", 
                        summary = "Adjust vertical position",
                        value = offsetY,
                        onValueChange = { 
                            offsetY = it
                            onPositionChange(offsetX, it)
                        },
                        valueRange = -1.0f..1.0f,
                        steps = 40
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = onDismiss) {
                    Text("Apply")
                }
            },
            dismissButton = {
                Row {
                    TextButton(onClick = {
                        scale = 1.0f
                        offsetX = 0.0f
                        offsetY = 0.0f
                        onReset()
                    }) {
                        Text("Reset")
                    }
                    TextButton(onClick = onDismiss) {
                        Text("Cancel")
                    }
                }
            }
        )
    }
}