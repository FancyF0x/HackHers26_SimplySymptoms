import requests

def get_drugs_for_condition(condition):
    # Search the 'indications_and_usage' field for your symptom/condition
    url = f"https://api.fda.gov/drug/label.json?search=indications_and_usage:{condition}&limit=5"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for result in data.get('results', []):
            # Extracting the brand name and generic name
            brand_name = result.get('openfda', {}).get('brand_name', ['Unknown Name'])[0]
            print(f"Suggested Drug: {brand_name}")
    else:
        print("Error fetching data or no results found.")

# Test it
get_drugs_for_condition("coughing")