package com.example.activitylifecycle

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    private fun logCallback(name: String) {
        Log.d("ActivityLifecycle", "$name instance=${System.identityHashCode(this)} changingConfigurations=$isChangingConfigurations")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        logCallback("onCreate")
        setContent {
            MaterialTheme {
                Surface {
                    Column(
                        modifier = Modifier.fillMaxSize().padding(24.dp),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text("ActivityLifecycle", style = MaterialTheme.typography.headlineMedium)
                        Text("Сверните приложение, вернитесь и поверните экран.\nLogcat: tag:ActivityLifecycle")
                    }
                }
            }
        }
    }

    override fun onStart() { super.onStart(); logCallback("onStart") }
    override fun onResume() { super.onResume(); logCallback("onResume") }
    override fun onPause() { super.onPause(); logCallback("onPause") }
    override fun onStop() { super.onStop(); logCallback("onStop") }
    override fun onRestart() { super.onRestart(); logCallback("onRestart") }
    override fun onDestroy() { super.onDestroy(); logCallback("onDestroy") }
}
