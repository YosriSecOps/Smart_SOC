# collector.py

import json
import time

ALERT_FILE = "/var/ossec/logs/alerts/alerts.json"


def stream_alerts():

    while True:

        try:
            with open(ALERT_FILE, "r", encoding="utf-8", errors="ignore") as f:

                # Aller à la fin du fichier
                f.seek(0, 2)

                while True:

                    line = f.readline()

                    # Pas encore de nouvelle ligne
                    if not line:
                        time.sleep(0.2)
                        continue

                    # Nettoyage
                    line = line.strip()

                    # Ignore lignes vides
                    if not line:
                        continue

                    try:
                        alert = json.loads(line)

                        # Vérifie que c'est bien un dict JSON
                        if isinstance(alert, dict):
                            yield alert

                    except json.JSONDecodeError as e:
                        print(f"[JSON ERROR] {e}")

                    except Exception as e:
                        print(f"[COLLECTOR ERROR] {e}")

        except FileNotFoundError:
            print(f"[ERROR] Alert file not found: {ALERT_FILE}")
            time.sleep(5)

        except PermissionError:
            print(f"[ERROR] Permission denied: {ALERT_FILE}")
            time.sleep(5)

        except Exception as e:
            print(f"[FATAL COLLECTOR ERROR] {e}")
            time.sleep(5)
