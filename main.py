import os
import json
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    def run_on_ui_thread(func):
        return func

class JarvisCoreEngineApp(App):
    def build(self):
        self.title = "J.A.R.V.I.S. Core Matrix"
        self.vault_file = "jarvis_internal_vault.json"
        self.session_data = self.initialize_secure_vault()
        
        if platform == 'android':
            self.instantiate_native_view_layer()
        else:
            from kivy.uix.label import Label
            return Label(text="[⚡] J.A.R.V.I.S. Subsystem Active Mode.", markup=True)

    def initialize_secure_vault(self):
        if os.path.exists(self.vault_file):
            try:
                with open(self.vault_file, 'r') as f:
                    return json.load(f).get("logs", [])
            except:
                return []
        return []

    def save_vault_data(self):
        with open(self.vault_file, 'w') as f:
            json.dump({"logs": self.session_data}, f, indent=4)

    @run_on_ui_thread
    def instantiate_native_view_layer(self):
        self.native_webview = WebView(Activity)
        self.native_webview.getSettings().setJavaScriptEnabled(True)
        self.native_webview.getSettings().setDomStorageEnabled(True)
        
        class CoreSchemeBridgeClient(WebViewClient):
            def __init__(self, outer_instance):
                super().__init__()
                self.outer = outer_instance
            
            def shouldOverrideUrlLoading(self, view, url):
                if url.startswith("jarviscore://"):
                    extracted_payload = url.replace("jarviscore://", "")
                    from urllib.parse import unquote
                    processed_query = unquote(extracted_payload)
                    Clock.schedule_once(lambda dt: self.outer.route_system_pipeline(processed_query), 0.05)
                    return True
                return False

        self.native_webview.setWebViewClient(CoreSchemeBridgeClient(self))
        target_path = os.path.abspath("ui_template.html")
        self.native_webview.loadUrl(f"file://{target_path}")
        Activity.setContentView(self.native_webview)

    def route_system_pipeline(self, user_intent):
        hardware_match, status_message = self.evaluate_hardware_intents(user_intent)
        
        if hardware_match:
            self.inject_javascript_response("HARDWARE RESPONSE", status_message, "#39ff14")
            self.session_data.append({"query": user_intent, "response": status_message})
            self.save_vault_data()
        else:
            self.fetch_compliance_framework_response(user_intent)

    def evaluate_hardware_intents(self, raw_input):
        cleaned = raw_input.lower()
        try:
            if "camera" in cleaned:
                os.system("am start -a android.media.action.IMAGE_CAPTURE")
                return True, "Hardware routing initiated: Camera interface active."
            elif "gallery" in cleaned or "photo" in cleaned:
                os.system("am start -t image/* -a android.intent.action.VIEW")
                return True, "Hardware routing initiated: Gallery directory stream open."
            elif "settings" in cleaned:
                os.system("am start -a android.settings.SETTINGS")
                return True, "Hardware routing initiated: System settings terminal deployed."
            elif "whatsapp" in cleaned:
                os.system("am start -n com.whatsapp/com.whatsapp.Main")
                return True, "Hardware routing initiated: WhatsApp messaging activity live."
        except Exception as e:
            return True, f"Hardware interaction error: {str(e)}"
        return False, ""

    def fetch_compliance_framework_response(self, text_query):
        auth_key = "API KEY HARE "
        target_url = "https://api.groq.com/openai/v1/chat/completions"
        request_headers = {"Authorization": f"Bearer {auth_key}", "Content-Type": "application/json"}
        context_string = "\\n---\\n".join([f"User: {x['query']}\\nJARVIS: {x['response']}" for x in self.session_data[-2:]])

        system_rules = (
            "Aapka naam J.A.R.V.I.S. hai. Aap ek standalone Android native UI framework core assistant hain.\n"
            "Strict Rule: Har scripting query ka evaluation do explicit sections me response format karein:\n"
            "1. [⚡ PLATFORM LEGAL ETHICAL USE]: Authorized monitoring frameworks aur legal enterprise usage guidelines.\n"
            "2. [⚠️ SECURITY EXPLORE / ILLEGAL RISKS]: Malicious attacks, exploit techniques aur security consequences.\n"
            "Style: Professional, direct, crisp Hinglish text blocks with clean linebreaks."
        )

        payload_data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_rules},
                {"role": "user", "content": f"Previous logs:\\n{context_string}\\n\\nCurrent request: {text_query}"}
            ],
            "temperature": 0.2
        }

        try:
            res = requests.post(target_url, headers=request_headers, json=payload_data)
            if res.status_code == 200:
                engine_output = res.json()['choices'][0]['message']['content']
            else:
                engine_output = "Central matrix engine parsing error."
        except:
            engine_output = " Handshake sync timeout. Check device data connectivity."

        sanitized_output = engine_output.replace("\n", "<br>").replace('"', '\\"')
        self.inject_javascript_response("J.A.R.V.I.S. HUB", sanitized_output, "#ff007f")
        
        self.session_data.append({"query": text_query, "response": engine_output})
        self.save_vault_data()

    @run_on_ui_thread
    def inject_javascript_response(self, display_tag, narrative_text, visual_hex):
        if platform == 'android' and self.native_webview:
            execution_script = f"appendLogNode('{display_tag}', '{narrative_text}', '{visual_hex}');"
            self.native_webview.evaluateJavascript(execution_script, None)

if __name__ == '__main__':
    JarvisCoreEngineApp().run()
