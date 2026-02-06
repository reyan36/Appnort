import json
import os
import requests
from typing import Dict, Optional, List

class Categorizer:
    def __init__(self, groq_api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.groq_api_key = groq_api_key
        self.model = model
        self.rules = {
            "Development": ["python", "java", "vscode", "visual studio", "git", "docker", "node", "sdk", "compiler"],
            "Productivity": ["office", "word", "excel", "powerpoint", "notion", "obsidian", "todo", "calendar"],
            "Games": ["steam", "game", "minecraft", "unity", "unreal", "epic games", "xbox"],
            "Browsers": ["chrome", "firefox", "edge", "brave", "opera", "safari"],
            "Media": ["vlc", "spotify", "music", "video", "player", "adobe", "photoshop", "gimp", "obs"],
            "System": ["driver", "nvidia", "intel", "amd", "realtek", "microsoft visual c++"],
            "Communication": ["zoom", "discord", "skype", "teams", "slack", "whatsapp", "telegram"],
            "Utilities": ["zip", "rar", "cleaner", "antivirus", "vpn", "calculator"]
        }
        self.cache_file = "category_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, str]]:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    # Migration: If old cache (str), convert to dict
                    new_data = {}
                    for k, v in data.items():
                        if isinstance(v, str):
                            new_data[k] = {"category": v, "security": "Unknown"}
                        else:
                            new_data[k] = v
                    return new_data
            except json.JSONDecodeError:
                pass
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=4)
        except IOError:
            print("Failed to save category cache.")

    def categorize(self, program_name: str) -> Dict[str, str]:
        # Check cache first
        if program_name in self.cache:
            entry = self.cache[program_name]
            # Ensure entry is dict
            if isinstance(entry, str):
                entry = {"category": entry, "security": "Unknown"}
            
            # Return if valid and known, or if we have no key to improve it
            if entry["category"] != "Unknown" or not self.groq_api_key:
                return entry
            # Fall through if Unknown and we have key

        category = self._rule_based_categorize(program_name)
        result = {"category": category, "security": "Unknown"}
        
        # We don't AI categorize singly anymore if batching is preferred, 
        # but for backward compatibility or single checks:
        if category == "Unknown" and self.groq_api_key:
            # For now, single AI call (legacy support), but main logic should use batch
            try:
                # We'll use the batch function for single item to get consistent format
                batch_res = self.batch_categorize([program_name])
                if batch_res:
                    result = batch_res.get(program_name, result)
            except Exception as e:
                print(f"AI Categorization error: {e}")
        
        self.cache[program_name] = result
        self._save_cache()
        return result

    def batch_categorize(self, program_names: List[str]) -> Dict[str, Dict[str, str]]:
        if not self.groq_api_key or not program_names:
            return {}

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        folders = list(self.rules.keys())
        prompt = (
            f"Classify the following software programs: {program_names}.\n\n"
            f"TASK 1 - CATEGORY: Assign exactly one category from this list: {folders}. "
            "Match based on primary function. Default to 'Utilities' only if no other category fits.\n\n"
            "TASK 2 - SECURITY RISK: Assign one of [Low, Medium, High] using these criteria:\n"
            "- 'Low': Verified commercial software (AAA games, major browsers, official dev tools, "
            "hardware drivers, productivity suites) from legitimate publishers.\n"
            "- 'Medium': Software with elevated risk potential-P2P/torrent clients, remote access tools, "
            "freeware known to bundle adware, unofficial app stores, or tools commonly misused.\n"
            "- 'High': Confirmed malware, RATs, keyloggers, credential stealers, cracked/pirated software, "
            "hack tools, or anything flagged by major antivirus vendors.\n\n"
            "RULES:\n"
            "- When uncertain about security, lean toward 'Low' for recognized brands, 'Medium' otherwise.\n"
            "- Base judgment on the software's legitimate version, not hypothetical compromised states.\n"
            "- Evaluate each program independently.\n\n"
            "OUTPUT: Return ONLY a valid JSON object. Keys are exact program names; values are objects "
            "with 'category' (string) and 'security' (string) keys.\n"
            "Example: {\"Notepad\": {\"category\": \"Productivity\", \"security\": \"Low\"}, "
            "\"qBittorrent\": {\"category\": \"Utilities\", \"security\": \"Medium\"}}"
        )
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a software analysis engine. Return purely JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                results = json.loads(content)
                
                # Update cache
                for name, data in results.items():
                    # Sanitize
                    cat = data.get("category", "Unknown")
                    sec = data.get("security", "Unknown")
                    clean_entry = {"category": cat, "security": sec}
                    
                    # Fuzzy match name back to original list
                    match_found = False
                    if name in program_names:
                        self.cache[name] = clean_entry
                        match_found = True
                    else:
                        # Case-insensitive match
                        for original in program_names:
                            if original.lower() == name.lower():
                                self.cache[original] = clean_entry
                                match_found = True
                                break
                        
                        # Substring match (if AI simplified the name)
                        if not match_found:
                            for original in program_names:
                                # Check if AI name is part of original (e.g. "Audacity" in "Audacity 3.7.7")
                                # OR original is part of AI name
                                if name.lower() in original.lower() or original.lower() in name.lower():
                                    self.cache[original] = clean_entry
                                    match_found = True
                                    break
                
                self._save_cache()
                return results
            else:
                print(f"Groq API Error: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            print(f"Batch AI Error: {e}")
            return {}

    def _rule_based_categorize(self, program_name: str) -> str:
        program_name_lower = program_name.lower()
        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in program_name_lower:
                    return category
        return "Unknown"

    # _ai_categorize Removed/Deprecated in favor of batch_categorize logic
    def _ai_categorize(self, program_name: str) -> str:
        # Wrapper for backward compat if needed, using batch
        res = self.batch_categorize([program_name])
        return res.get(program_name, {}).get("category", "Unknown")
