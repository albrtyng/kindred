package com.example.kindred

import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import com.example.kindred.feed.FeedScreen
import com.example.kindred.ui.theme.KindredTheme

@Composable
@Preview
fun App() {
    KindredTheme {
        FeedScreen()
    }
}
