
import random
import json
import os
from datetime import datetime

JOKES = [
    {
        "title": "पढ़ाई का बहाना",
        "joke": "टीचर: पढ़ाई क्यों नहीं की?\nस्टूडेंट: मैडम, रात को सपने में पढ़ रहा था!\nटीचर: फिर?\nस्टूडेंट: सुबह उठा तो किताब बंद थी!",
        "ending": "पढ़ाई भी अब सपनों में होने लगी!"
    },
    {
        "title": "मोबाइल का प्यार",
        "joke": "पापा: दिनभर मोबाइल में क्या देखते रहते हो?\nबेटा: ज्ञान बढ़ाता हूं पापा!\nपापा: अच्छा, तो बताओ 2 का पहाड़ा?\nबेटा: गूगल कर लूं?",
        "ending": "आजकल ज्ञान भी ऑनलाइन है!"
    },
    {
        "title": "शादी का सवाल",
        "joke": "दोस्त: भाई, शादी के बाद जिंदगी कैसी है?\nदूसरा: बिल्कुल फिल्म जैसी!\nदोस्त: रोमांटिक?\nदूसरा: नहीं, रोज नया ड्रामा!",
        "ending": "शादी यानी रोज एक नया एपिसोड!"
    }
]

def generate_joke():
    joke = random.choice(JOKES)

    result = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": joke["title"],
        "script": joke["joke"],
        "ending": joke["ending"]
    }

    os.makedirs("generated", exist_ok=True)

    filename = datetime.now().strftime(
        "generated/joke_%Y%m%d_%H%M%S.json"
    )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print("JOKE GENERATED SUCCESSFULLY!")
    print(json.dumps(result, ensure_ascii=False, indent=4))
    print("Saved to:", filename)

if __name__ == "__main__":
    generate_joke()
