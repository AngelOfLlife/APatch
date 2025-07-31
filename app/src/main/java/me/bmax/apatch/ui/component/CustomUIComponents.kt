package me.bmax.apatch.ui.component

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.CenterFocusStrong
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.PhotoSizeSelectLarge
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import coil.compose.rememberAsyncImagePainter
import me.bmax.apatch.R
import kotlin.math.roundToInt

@Composable
fun CustomSliderItem(
    icon: ImageVector,
    title: String,
    summary: String,
    value: Float,
    onValueChange: (Float) -> Unit,
    valueRange: ClosedFloatingPointRange<Float> = 0f..1f,
    steps: Int = 0,
    modifier: Modifier = Modifier
) {
    val animatedValue by animateFloatAsState(
        targetValue = value,
        animationSpec = tween(300),
        label = "SliderAnimation"
    )
    
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                modifier = Modifier.size(24.dp),
                tint = MaterialTheme.colorScheme.onSurface
            )
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Medium
                )
                Text(
                    text = summary,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            Text(
                text = "${(animatedValue * 100).roundToInt()}%",
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.width(50.dp),
                textAlign = TextAlign.End
            )
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Slider(
            value = animatedValue,
            onValueChange = onValueChange,
            valueRange = valueRange,
            steps = steps,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp),
            colors = SliderDefaults.colors(
                thumbColor = MaterialTheme.colorScheme.primary,
                activeTrackColor = MaterialTheme.colorScheme.primary,
                inactiveTrackColor = MaterialTheme.colorScheme.surfaceVariant
            )
        )
    }
}

@Composable
fun CustomBackgroundImageItem(
    icon: ImageVector,
    title: String,
    summary: String,
    backgroundImageUri: String?,
    onImageSelected: (String) -> Unit,
    onImageRemoved: () -> Unit,
    modifier: Modifier = Modifier
) {
    var showImagePreview by remember { mutableStateOf(false) }
    
    val imagePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let { 
            onImageSelected(it.toString())
        }
    }

    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                modifier = Modifier.size(24.dp),
                tint = MaterialTheme.colorScheme.onSurface
            )
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Medium
                )
                Text(
                    text = summary,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        
        Spacer(modifier = Modifier.height(12.dp))
        
        // Image preview and controls
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(120.dp),
            shape = RoundedCornerShape(12.dp),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
            )
        ) {
            Box(
                modifier = Modifier.fillMaxWidth(),
                contentAlignment = Alignment.Center
            ) {
                if (!backgroundImageUri.isNullOrEmpty()) {
                    // Show background image
                    Image(
                        painter = rememberAsyncImagePainter(backgroundImageUri),
                        contentDescription = "Background Preview",
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(120.dp),
                        contentScale = ContentScale.Crop
                    )
                    
                    // Control overlay
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(
                                MaterialTheme.colorScheme.surface.copy(alpha = 0.9f),
                                RoundedCornerShape(bottomStart = 12.dp, bottomEnd = 12.dp)
                            )
                            .padding(8.dp)
                            .align(Alignment.BottomCenter),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        IconButton(
                            onClick = { imagePickerLauncher.launch("image/*") }
                        ) {
                            Icon(
                                Icons.Filled.PhotoSizeSelectLarge,
                                contentDescription = stringResource(id = R.string.ui_choose_background_image),
                                tint = MaterialTheme.colorScheme.primary
                            )
                        }
                        
                        IconButton(
                            onClick = { showImagePreview = true }
                        ) {
                            Icon(
                                Icons.Filled.CenterFocusStrong,
                                contentDescription = stringResource(id = R.string.ui_scale_and_position),
                                tint = MaterialTheme.colorScheme.secondary
                            )
                        }
                        
                        IconButton(
                            onClick = onImageRemoved
                        ) {
                            Icon(
                                Icons.Filled.Delete,
                                contentDescription = stringResource(id = R.string.ui_remove_background_image),
                                tint = MaterialTheme.colorScheme.error
                            )
                        }
                    }
                } else {
                    // Show add button
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { imagePickerLauncher.launch("image/*") }
                            .padding(16.dp)
                    ) {
                        Icon(
                            Icons.Filled.Add,
                            contentDescription = stringResource(id = R.string.ui_choose_background_image),
                            modifier = Modifier.size(32.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = stringResource(id = R.string.ui_choose_background_image),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.primary,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }
        }
        
        // Scale and Position Dialog
        if (showImagePreview && !backgroundImageUri.isNullOrEmpty()) {
            ScalePositionControlDialog(
                showDialog = showImagePreview,
                onDismiss = { showImagePreview = false },
                imageScale = 1.0f, // TODO: Load from preferences
                positionX = 0.0f,  // TODO: Load from preferences
                positionY = 0.0f,  // TODO: Load from preferences
                onScaleChange = { /* TODO: Save to preferences */ },
                onPositionChange = { _, _ -> /* TODO: Save to preferences */ },
                onReset = { /* TODO: Reset and save to preferences */ }
            )
        }
    }
}

@Composable
fun CustomSwitchItem(
    icon: ImageVector,
    title: String,
    summary: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    enabled: Boolean = true,
    modifier: Modifier = Modifier
) {
    ListItem(
        modifier = modifier
            .clickable(enabled = enabled) { onCheckedChange(!checked) }
            .alpha(if (enabled) 1f else 0.6f),
        headlineContent = { 
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium
            ) 
        },
        supportingContent = { 
            Text(
                text = summary,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            ) 
        },
        leadingContent = {
            Icon(
                imageVector = icon,
                contentDescription = title,
                tint = if (enabled) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
            )
        },
        trailingContent = {
            Switch(
                checked = checked,
                onCheckedChange = onCheckedChange,
                enabled = enabled
            )
        }
    )
}