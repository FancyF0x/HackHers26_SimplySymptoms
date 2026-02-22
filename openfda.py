import requests

def get_drugs_for_condition(condition):
    # Search the 'indications_and_usage' field for your symptom/condition
    url = f"https://api.fda.gov/drug/label.json?search=indications_and_usage:{condition}&limit=50"
    
    response = requests.get(url)
    names = []
    seen_names = set()  # To track already added drug names for deduplication
    
    if response.status_code == 200:
        data = response.json()
        for result in data.get('results', []):
            openfda = result.get('openfda', {})
            
            # Hierarchical name retrieval: Brand -> Generic -> Substance
            brand = openfda.get('brand_name', [None])[0]
            generic = openfda.get('generic_name', [None])[0]
            substance = openfda.get('substance_name', [None])[0]
            
            drug_name = brand or generic or substance or "Unknown Medication"

            # Skip if name is missing, generic placeholder, or already seen
            if not drug_name or drug_name == "Unknown Medication" or drug_name.lower() in seen_names:
                continue
            
            # Add to set (lowercase for better deduplication) and results list
            seen_names.add(drug_name.lower())
            
            # Optional: Get the actual indication text to verify relevance
            usage = result.get('indications_and_usage', [''])[0][:100] + "..."
            
            names.append({"name": drug_name, "snippet": usage})
            if len(names) >= 5:  # Limit to top 5 results
                break
    else:
        print(f"Error {response.status_code}: Likely no exact match for that condition.")

    return names
# Test it
drugs = get_drugs_for_condition("migraine")
print(drugs)  # For debugging
# clean_data = [x for x in drugs if x is not None]
for drug in drugs:
    if drug and drug.get('name') != "Unknown Medication":  # Filter out unknown names
        print(f"- {drug['name']}")