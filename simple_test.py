import easyocr
import re

def extract_blood_request(image_path):
    print("Loading the AI model...")
    reader = easyocr.Reader(['en'])
    
    print("Reading the image...")
    results = reader.readtext(image_path, detail=0)
    
    if results:
        # 1. Join all the scattered text chunks into one giant string
        full_text = " ".join(results)
        print("\n--- Raw OCR Text ---")
        print(full_text)
        
        # 2. Hunt for the blood group using our Regex pattern
        pattern = r'(A|B|AB|O)[+-]'
        
        # re.IGNORECASE helps if the OCR accidentally read 'a+' instead of 'A+'
        match = re.search(pattern, full_text, re.IGNORECASE)
        
        print("\n--- Intelligence Layer Output ---")
        if match:
            # We found it! .upper() ensures 'a+' is standardized to 'A+' for the database
            blood_group = match.group(0).upper()
            print(f"Blood Group Needed: {blood_group}")
        else:
            print("Blood Group Needed: NOT FOUND (Requires manual admin check)")
        print("---------------------------------")
        
    else:
        print("No text detected in the image.")

# RUN THE TEST
extract_blood_request('note.jpg')