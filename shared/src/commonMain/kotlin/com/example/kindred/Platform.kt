package com.example.kindred

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform