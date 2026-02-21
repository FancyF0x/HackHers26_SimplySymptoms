import requests

def get_drugs_for_condition(condition):
    # Search the 'indications_and_usage' field for your symptom/condition
    url = f"https://api.fda.gov/drug/label.json?search=indications_and_usage:{condition}&limit=5"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        names = []
        for result in data.get('results', []):
            # Extracting the brand name and generic name
            brand_name = result.get('openfda', {}).get('brand_name', ['Unknown Name'])[0]
            names.append(brand_name)
    else:
        print("Error fetching data or no results found.")

    return names
# Test it
drugs = get_drugs_for_condition("headache")
print(drugs)  # For debugging
clean_data = [x for x in drugs if x is not None]
for drug in clean_data:
    if drug and drug != "Unknown Name":  # Filter out unknown names
        print(f"- {drug}")