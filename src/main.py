# main.py

from collector import stream_alerts
from analyzer import analyze
from responder import block_ip
from notifier import send
# from voice import speak

print("[+] Smart SOC started...")
print("[+] Waiting for security alerts...\n")

for alert in stream_alerts():

    try:
        # Vérifie que alert est bien un dictionnaire
        if not isinstance(alert, dict):
            continue

        rule = alert.get("rule", {})
        level = int(rule.get("level", 0))
        description = rule.get("description", "No description")

        # ===== RECUPERATION IP =====
        ip = "unknown"

        data = alert.get("data", {})

        # Suricata / Wazuh formats possibles
        if "srcip" in data:
            ip = data.get("srcip")

        elif "src_ip" in data:
            ip = data.get("src_ip")

        elif "srcip" in alert:
            ip = alert.get("srcip")

        elif "agent" in alert:
            ip = alert.get("agent", {}).get("ip", "unknown")

        # ===== AFFICHAGE =====
        print("\n==============================")
        print("[+] SECURITY ALERT DETECTED")
        print(f"[+] Level: {level}")
        print(f"[+] Description: {description}")
        print(f"[+] Source IP: {ip}")
        print("==============================")

        # ===== IA seulement alertes importantes =====
        if level >= 7:

            print("\n[+] Sending alert to AI...\n")

            try:
                report = analyze(alert)

                print("===== AI REPORT =====")
                print(report)
                print("=====================")

                # ===== AUTO BLOCK =====
                # if "High" in report or "Critical" in report:
                #     if ip != "unknown":
                #         block_ip(ip)

                # ===== TELEGRAM =====
                send(report)

                # ===== VOICE =====
                # speak("Critical security alert detected")

            except Exception as ai_error:
                print(f"[AI ERROR] {ai_error}")

    except Exception as e:
        print(f"[MAIN ERROR] {e}")
