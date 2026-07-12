package com.example.kindred.feed

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeContentPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.kindred.core.model.Post

private val samplePosts =
    listOf(
        Post(author = "@albert", caption = "A quiet afternoon."),
        Post(author = "@robbie", caption = "Lunch in the park."),
        Post(author = "@hailey", caption = "Golden hour."),
        Post(author = "@neil", caption = "Rain on the windows."),
        Post(author = "@tyler", caption = "First coffee of the day."),
    )

@Composable
internal fun FeedScreen() {
    // The screen owns like state; cards receive only their value and an event callback.
    var likedPostAuthors by remember { mutableStateOf(setOf("@albert")) }

    LazyColumn(
        modifier =
            Modifier.fillMaxSize()
                .background(MaterialTheme.colorScheme.primaryContainer)
                .safeContentPadding()
    ) {
        item {
            Text(
                text = "Kindred",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.padding(16.dp),
            )
        }

        items(samplePosts, key = { it.author }) { post ->
            val isLiked = post.author in likedPostAuthors
            PostCard(
                post = post,
                isLiked = isLiked,
                onLikeClick = {
                    likedPostAuthors =
                        if (isLiked) {
                            likedPostAuthors - post.author
                        } else {
                            likedPostAuthors + post.author
                        }
                },
            )
        }
    }
}
