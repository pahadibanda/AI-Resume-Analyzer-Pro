import urllib.request
import re
import json

# Definitive list of target brands, custom slugs, and official hex colors
brands_config = {
    "google": { "name": "Google", "slug": "google", "hex": "#EA4335" },
    "microsoft": { "name": "Microsoft", "slug": "microsoft", "hex": "#F3F3F3" },
    "amazon": { "name": "Amazon", "slug": "amazon", "hex": "#FF9900" },
    "apple": { "name": "Apple", "slug": "apple", "hex": "#FFFFFF" }, # White looks best on dark background
    "meta": { "name": "Meta", "slug": "meta", "hex": "#0668E1" },
    "netflix": { "name": "Netflix", "slug": "netflix", "hex": "#E50914" },
    "nvidia": { "name": "NVIDIA", "slug": "nvidia", "hex": "#76B900" },
    "tesla": { "name": "Tesla", "slug": "tesla", "hex": "#CC0000" },
    "ibm": { "name": "IBM", "slug": "ibm", "hex": "#052FAD" },
    "oracle": { "name": "Oracle", "slug": "oracle", "hex": "#F80000" },
    "adobe": { "name": "Adobe", "slug": "adobe", "hex": "#FF0000" },
    "salesforce": { "name": "Salesforce", "slug": "salesforce", "hex": "#00A1E0" },
    "intel": { "name": "Intel", "slug": "intel", "hex": "#0071C5" },
    "cisco": { "name": "Cisco", "slug": "cisco", "hex": "#1BA0D7" },
    "spotify": { "name": "Spotify", "slug": "spotify", "hex": "#1ED760" },
    "uber": { "name": "Uber", "slug": "uber", "hex": "#FFFFFF" },
    "airbnb": { "name": "Airbnb", "slug": "airbnb", "hex": "#FF5A5F" },
    "linkedin": { "name": "LinkedIn", "slug": "linkedin", "hex": "#004182" },
    "openai": { "name": "OpenAI", "slug": "openai", "hex": "#FFFFFF" },
    # Indian Companies
    "tcs": { "name": "TCS", "slug": "tcs", "hex": "#808080" },
    "infosys": { "name": "Infosys", "slug": "infosys", "hex": "#007CC3" },
    "wipro": { "name": "Wipro", "slug": "wipro", "hex": "#1F2261" },
    "hcl": { "name": "HCL", "slug": "hcl", "hex": "#005691" },
    "techmahindra": { "name": "Tech Mahindra", "slug": "techmahindra", "hex": "#E31B23" },
    "accenture": { "name": "Accenture", "slug": "accenture", "hex": "#A100FF" },
    "capgemini": { "name": "Capgemini", "slug": "capgemini", "hex": "#0070AD" },
    "cognizant": { "name": "Cognizant", "slug": "cognizant", "hex": "#0033A0" },
    "zoho": { "name": "Zoho", "slug": "zoho", "hex": "#E31A22" },
    "flipkart": { "name": "Flipkart", "slug": "flipkart", "hex": "#FFE11B" },
    "phonepe": { "name": "PhonePe", "slug": "phonepe", "hex": "#5F259F" },
    "paytm": { "name": "Paytm", "slug": "paytm", "hex": "#00BAF2" },
    "razorpay": { "name": "Razorpay", "slug": "razorpay", "hex": "#0B72E7" },
    "freshworks": { "name": "Freshworks", "slug": "freshworks", "hex": "#0082F6" },
    "swiggy": { "name": "Swiggy", "slug": "swiggy", "hex": "#FC8019" },
    "zomato": { "name": "Zomato", "slug": "zomato", "hex": "#E23744" },
    "jio": { "name": "Jio", "slug": "jio", "hex": "#E60000" },
    "myntra": { "name": "Myntra", "slug": "myntra", "hex": "#FF1493" }
}

# Fallback paths for companies not in simple-icons
fallbacks = {
    "techmahindra": {
        "title": "Tech Mahindra",
        "hex": "#E31B23",
        "slug_fallback": "mahindra" # Fetch Mahindra logo
    },
    "capgemini": {
        "title": "Capgemini",
        "hex": "#0070AD",
        "path": "M12 2C6.48 2 2 6.48 2 12c0 2.76 1.12 5.26 2.93 7.07L12 11.5l7.07 7.57C20.88 17.26 22 14.76 22 12c0-5.52-4.48-10-10-10zm0 18c-4.41 0-8-3.59-8-8c0-1.85.63-3.55 1.69-4.9L12 13.5l6.31-6.4C19.37 8.45 20 10.15 20 12c0 4.41-3.59 8-8 8z"
    },
    "freshworks": {
        "title": "Freshworks",
        "hex": "#0082F6",
        "path": "M17 8s-3.5 0-6.5 3c-2.5 2.5-2.5 6 0 8.5C13 22 17 22 17 22s0-4-2.5-6.5c-2.5-2.5-3-5.5-3-5.5s3 1.5 5.5 3c2.5 1.5 3.5.5 3.5-.5V8z"
    },
    "myntra": {
        "title": "Myntra",
        "hex": "#FF3F6C",
        "path": "M2 22h3.5v-11l4.5 7.5 4.5-7.5v11H18V2h-3.5L10 10.5 5.5 2H2v20z"
    }
}

results = {}

for key, config in brands_config.items():
    name = config["name"]
    slug = config["slug"]
    hex_val = config["hex"]
    
    # Check if there is an explicit fallback config
    if key in fallbacks and "slug_fallback" not in fallbacks[key]:
        # Direct static injection
        results[key] = {
            "title": fallbacks[key]["title"],
            "hex": fallbacks[key]["hex"],
            "path": fallbacks[key]["path"]
        }
        print(f"Using custom static path for {name}...")
        continue
        
    if key in fallbacks and "slug_fallback" in fallbacks[key]:
        slug = fallbacks[key]["slug_fallback"]
        
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
    print(f"Fetching SVG path for {name} from {url}...")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as res:
            svg_content = res.read().decode('utf-8')
            
            # Extract path d attribute
            path_match = re.search(r'<path[^>]+d="([^"]+)"', svg_content)
            if path_match:
                path_d = path_match.group(1)
                results[key] = {
                    "title": name,
                    "hex": hex_val,
                    "path": path_d
                }
                print(f"-> Success!")
            else:
                print(f"-> Failed to parse path from SVG file.")
    except Exception as e:
        print(f"-> HTTP Error: {e}")

print(f"\nCompleted! Fetched {len(results)} / {len(brands_config)} company logos.")

with open("scratch/logo_data.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved to scratch/logo_data.json")
