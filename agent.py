
import random
import json
import os
from datetime import datetime

JOKES = [
    {
        "title": "पढ़ाई का बहाना",
        "dialogue": [
            {"speaker": "Bobby", "text": "यार Sunny, आज मैंने बहुत पढ़ाई की!"},
            {"speaker": "Sunny", "text": "अच्छा! कितनी देर?"},
            {"speaker": "Bobby", "text": "पूरी रात सपने में!"},
            {"speaker": "Sunny", "text": "फिर सुबह किताब क्यों बंद थी?"},
            {"speaker": "Bobby", "text": "क्योंकि सपना खत्म हो गया था!"}
        ],
        "ending": "पढ़ाई भी अब सपनों में होने लगी!"
    },
    {
        "title": "मोबाइल का प्यार",
        "dialogue": [
            {"speaker": "Sunny", "text": "Bobby, दिनभर मोबाइल में क्या देखते रहते हो?"},
            {"speaker": "Bobby", "text": "ज्ञान बढ़ाता हूं भाई!"},
            {"speaker": "Sunny", "text": "तो बताओ, दो का पहाड़ा सुनाओ!"},
            {"speaker": "Bobby", "text": "एक मिनट, गूगल कर लूं?"}
        ],
        "ending": "आजकल ज्ञान भी ऑनलाइन है!"
    },
    {
        "title": "शादी का सवाल",
        "dialogue": [
            {"speaker": "Bobby", "text": "Sunny, शादी के बाद जिंदगी कैसी होती है?"},
            {"speaker": "Sunny", "text": "बिल्कुल फिल्म जैसी!"},
            {"speaker": "Bobby", "text": "रोमांटिक फिल्म?"},
            {"speaker": "Sunny", "text": "नहीं भाई, रोज नया ड्रामा!"}
        ],
        "ending": "शादी यानी रोज एक नया एपिसोड!"
    }
]

def generate_joke():
    joke = random.choice(JOKES)

    script = "\n".join(
        f'{line["speaker"]}: {line["text"]}'
        for line in joke["dialogue"]
    )

    result = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": joke["title"],
        "dialogue": joke["dialogue"],
        "script": script,
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
