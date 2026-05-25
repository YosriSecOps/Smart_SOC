import requests
import subprocess
import json
import os
import time


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:latest"

ALERT_FILE = "/var/ossec/logs/alerts/alerts.json"

SYSTEM_PROMPT = """
You are Neo, an elite autonomous SOC AI analyst.

Environment:
- Ubuntu Linux server
- Wazuh SIEM installed
- Suricata IDS installed
- Local VMware cybersecurity lab
- Kali Linux attacker machine
- Wazuh alerts path: /var/ossec/logs/alerts/alerts.json

Your role:
- analyze cybersecurity threats
- summarize attacks
- detect brute force attempts
- analyze IDS alerts
- identify suspicious IPs
- explain MITRE ATT&CK techniques
- monitor system security
- assist SOC investigations
- explain alerts clearly

Rules:
- prioritize critical threats
- be concise and technical
- never invent logs
- never hallucinate IPs
- explain findings professionally
"""


ALLOWED_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    "uptime",
    "df",
    "free",
    "ip",
    "ss",
    "netstat",
    "tail",
    "cat",
    "grep",
    "journalctl"
]


def ask_llm(prompt):

    payload = {
        "model": MODEL,
        "prompt": SYSTEM_PROMPT + "\n\nUser Request:\n" + prompt,
        "stream": False
    }

    try:
        r = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        r.raise_for_status()

        data = r.json()

        return data.get("response", "[NO RESPONSE]")

    except requests.exceptions.Timeout:
        return "[ERROR] Ollama timeout"

    except requests.exceptions.ConnectionError:
        return "[ERROR] Cannot connect to Ollama"

    except Exception as e:
        return f"[ERROR] {str(e)}"



def run_command(cmd):

    try:

        base = cmd.split()[0]

        if base not in ALLOWED_COMMANDS:
            return "[BLOCKED] Command not allowed"

        result = subprocess.getoutput(cmd)

        return result

    except Exception as e:
        return f"[ERROR] {str(e)}"



def read_alerts(lines=20):

    try:

        cmd = f"tail -n {lines} {ALERT_FILE}"

        raw = subprocess.getoutput(cmd)

        return raw

    except Exception as e:
        return f"[ERROR] {str(e)}"

def analyze_alerts():

    alerts = read_alerts(30)

    prompt = f"""
Analyze these Wazuh alerts.

Tasks:
- summarize attacks
- identify suspicious IPs
- detect brute force attempts
- identify critical alerts
- explain important events

Alerts:
{alerts}
"""

    return ask_llm(prompt)

# =========================
# SYSTEM HEALTH
# =========================

def system_health():

    uptime = run_command("uptime")
    memory = run_command("free -h")
    disk = run_command("df -h")

    return f"""
===== SYSTEM HEALTH =====

UPTIME:
{uptime}

MEMORY:
{memory}

DISK:
{disk}
"""

# =========================
# MAIN LOOP
# =========================

if __name__ == "__main__":

    print("\n[+] Neo SOC AI Agent Started")
    print("[+] Type 'help' for commands\n")

    while True:

        try:

            user = input("SOC> ").strip()

            # EXIT
            if user.lower() in ["exit", "quit"]:
                print("[+] Exiting Neo...")
                break

            # HELP
            elif user.lower() == "help":

                print("""
Available Commands:

help
exit
health
read alerts
analyze alerts
run <command>

Examples:
run ls
run whoami
run ip a
""")

            # SYSTEM HEALTH
            elif user.lower() == "health":

                print(system_health())

            # READ ALERTS
            elif user.lower() == "read alerts":

                print(read_alerts())

            # ANALYZE ALERTS
            elif user.lower() == "analyze alerts":

                print("\n[+] AI analyzing alerts...\n")

                print(analyze_alerts())

            # SAFE COMMANDS
            elif user.startswith("run "):

                cmd = user[4:]

                print(safe_run(cmd))

            # GENERAL AI QUESTIONS
            else:

                print("\n[+] Neo thinking...\n")

                print(ask_llm(user))

        except KeyboardInterrupt:

            print("\n[+] Interrupted")
            break

        except Exception as e:

            print(f"[ERROR] {str(e)}")

