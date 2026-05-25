import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze(alert):
    description = alert.get("rule", {}).get("description", "Alerte sans description")
    
    # NOUVEAU : Extraction améliorée pour attraper l'IP même sur les alertes internes Wazuh
    # On cherche dans "data", puis à la racine, puis dans "agent"
    srcip = alert.get("data", {}).get("srcip", alert.get("srcip", alert.get("agent", {}).get("ip", "IP_Inconnue")))
    destip = alert.get("data", {}).get("destip", alert.get("destip", "IP_Inconnue"))

    # NOUVEAU : On ajoute une règle de contexte pour l'IA concernant le DoS
    prompt = f"""
You are a Senior Cyber Security Analyst. Analyze this alert.

CRITICAL CONTEXT: 
If the alert description mentions "Agent event queue is full", "queue is flooded", or "queue is 90% full", you MUST identify this as a highly likely Denial of Service (DoS / Flood) attack overwhelming the SIEM sensors. The severity MUST be High or Critical.

CRITICAL RULES:
1. You MUST use the exact real IP addresses provided below:
   - Source/Agent IP: {srcip}
   - Target IP: {destip}
2. NEVER use placeholder names like "XYZ" or "IP_Inconnue" if an IP is provided above.
3. You MUST include the precise MITRE ATT&CK ID (e.g., T1498 for Network Denial of Service).
4. Keep the 'Short Voice Alert' to exactly one concise sentence.

Alert Description: {description}

Return your analysis formatted EXACTLY like this:
**Severity:** [Low/Medium/High/Critical]
**Attack Type:** [Name] (MITRE ID: [ID])
**Explanation:** [Your explanation using the real IPs and acknowledging the DoS context]
**Recommended Action:** [Steps to take]
**Short Voice Alert:** [One sentence alert]
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3", # ou le modèle que vous utilisez actuellement
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return result.get("response", "Erreur de format de réponse")
