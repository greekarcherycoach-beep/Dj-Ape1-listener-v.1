package gr.djape1.listener;

import android.os.Bundle;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(RadioPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
