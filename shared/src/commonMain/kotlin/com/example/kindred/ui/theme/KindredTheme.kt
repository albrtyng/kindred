package com.example.kindred.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color

internal data class KindredColors(
    val likeLiked: Color,
    val likeUnliked: Color,
)

private val lightKindredColors =
    KindredColors(
        likeLiked = Color(0xFFE53935),
        likeUnliked = Color.White,
    )

internal val LocalKindredColors = staticCompositionLocalOf {
    lightKindredColors
}

@Composable
internal fun KindredTheme(content: @Composable () -> Unit) {
    CompositionLocalProvider(LocalKindredColors provides lightKindredColors) {
        MaterialTheme(content = content)
    }
}
