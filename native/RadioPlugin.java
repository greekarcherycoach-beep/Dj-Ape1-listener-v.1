package gr.djape1.listener;

import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;

import androidx.core.content.ContextCompat;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "Radio")
public class RadioPlugin extends Plugin {

    @Override
    public void load() {
        RadioService.onStop = () -> notifyListeners("stop", new JSObject());
    }

    @PluginMethod
    public void start(PluginCall call) {
        try {
            Context ctx = getContext();
            Intent i = new Intent(ctx, RadioService.class);
            i.putExtra("title", call.getString("title", "Dj Ape1"));
            i.putExtra("text", call.getString("text", ""));
            ContextCompat.startForegroundService(ctx, i);
            call.resolve();
        } catch (Exception e) {
            call.reject(String.valueOf(e.getMessage()));
        }
    }

    @PluginMethod
    public void update(PluginCall call) {
        try {
            Context ctx = getContext();
            NotificationManager nm = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
            nm.notify(RadioService.NOTIF_ID, RadioService.build(ctx,
                    call.getString("title", "Dj Ape1"), call.getString("text", "")));
            call.resolve();
        } catch (Exception e) {
            call.reject(String.valueOf(e.getMessage()));
        }
    }

    @PluginMethod
    public void stop(PluginCall call) {
        try {
            Context ctx = getContext();
            ctx.stopService(new Intent(ctx, RadioService.class));
            call.resolve();
        } catch (Exception e) {
            call.reject(String.valueOf(e.getMessage()));
        }
    }
}
