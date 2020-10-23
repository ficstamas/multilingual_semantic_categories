"""
Removed
- foodweb
- land_form
- spring
- summer
- fall
- winter
- thanksgiving
- valentine
- virtues
Renamed
- grammar -> linguistics
- music_theory -> music
- mythical_beast -> mythical_monster
- postal -> post_office
- vacation -> holiday
Merged
- happiness -> happy
- sciences -> science
"""

SEARCH_TERMS = {
    "adjectives_for_people": "people",
    "carpart": "car",
    "clothe": "clothes",
    "cooking_tool": "cooking",
    "negative_word": "bad",
    "positive_word": "good",
}

ALLOWED_RELATIONS = {
    "adjectives_for_people": ["/r/HasProperty"],
    "animal": ["/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "april_fool": ["/r/RelatedTo", "/r/FormOf", "/r/Synonym"],
    "art": ["/r/RelatedTo", "/r/IsA", "/r/HasProperty"],
    "astronomy": ["/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "baseball": ["/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "bathroom": ["/r/AtLocation", "/r/UsedFor", "/r/PartOf", "/r/RelatedTo"],
    "beach": ["/r/AtLocation", "/r/RelatedTo", "/r/Synonym"],
    "big": ["/r/RelatedTo", "/r/Synonym", "/r/SimilarTo"],
    "biome": ["/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "bird": ["/r/RelatedTo", "/r/Synonym", "/r/IsA", "/r/CapableOf", "/r/PartOf"],
    "birthday": ["/r/RelatedTo", "/r/Synonym"],
    "boat": ["/r/AtLocation", "/r/RelatedTo", "/r/Synonym", "/r/IsA", "/r/AtLocation"],
    "body_of_water": ["/r/IsA", "/r/RelatedTo"],
    "body": ["/r/RelatedTo", "/r/PartOf", "/r/AtLocation", "/r/Antonym"],
    "building": ["/r/RelatedTo", "/r/PartOf", "/r/AtLocation", "/r/IsA"],
    "camping": ["/r/RelatedTo", "/r/Synonym"],
    "car": ["/r/IsA", "/r/CapableOf"],
    "carpart": ["/r/PartOf"],
    "carnival": ["/r/AtLocation", "/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "castle": ["/r/AtLocation", "/r/RelatedTo", "/r/Synonym"],
    "cat": ["/r/AtLocation", "/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "christmas": ["/r/RelatedTo", "/r/Synonym"],
    "circus": ["/r/RelatedTo", "/r/Synonym", "/r/AtLocation"],
    "clothe": ["/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "color": ["/r/RelatedTo", "/r/IsA", "/r/MannerOf"],
    "computer": ["/r/RelatedTo", "/r/Synonym", "/r/PartOf", "/r/UsedFor", "/r/IsA", "/r/AtLocation", "/r/CapableOf"],
    "constitution": ["/r/RelatedTo", "/r/Synonym"],
    "container": ["/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "cooking_tool": ["/r/UsedFor"],
    "cooking": ["/r/HasContext", "/r/IsA", "/r/RelatedTo", "/r/Synonym"],
    "country": ["/r/IsA"],
    "dance": ["/r/MannerOf", "/r/RelatedTo", "/r/Synonym", "/r/IsA"],
    "dentist": ["/r/RelatedTo", "/r/Synonym", "/r/AtLocation", "/r/CapableOf"],
    "dessert": ["/r/RelatedTo", "/r/Synonym", "/r/IsA", "/r/InstanceOf"],
    "doctor": ["/r/RelatedTo", "/r/Synonym", "/r/AtLocation", "/r/IsA", "/r/CapableOf", "/r/UsedFor"],
    "dog": ["/r/RelatedTo", "/r/Synonym", "/r/AtLocation", "/r/CapableOf", "/r/IsA"],
    "driving": ["/r/RelatedTo", "/r/Synonym", "/r/HasContext", "/r/UsedFor"],
    "election": ["/r/RelatedTo", "/r/Synonym", "/r/DerivedFrom", "/r/IsA"],
    "emotion": ["/r/IsA", "/r/RelatedTo"],
    "energy": ["/r/IsA", "/r/RelatedTo"],
    "family": ["/r/RelatedTo", "/r/IsA", "/r/AtLocation", "/r/PartOf"],
    "farm": ["/r/RelatedTo", "/r/IsA", "/r/AtLocation"],
    "fish": ["/r/RelatedTo", "/r/IsA", "/r/AtLocation", "/r/HasA"],
    "flower": ["/r/RelatedTo", "/r/IsA", "/r/PartOf", "/r/CapableOf"],
    "food": ["/r/RelatedTo", "/r/IsA", "/r/UsedFor"],
    "fruit": ["/r/RelatedTo", "/r/IsA"],
    "furniture": ["/r/RelatedTo", "/r/IsA"],
    "geography": ["/r/HasContext", "/r/RelatedTo", "/r/DerivedFrom"],
    "linguistics": ["/r/DerivedFrom", "/r/RelatedTo", "/r/HasContext"],
    "happy": ["/r/MotivatedByGoal", "/r/RelatedTo"],
    "holiday": ["/r/IsA", "/r/RelatedTo"],
    "house": ["/r/RelatedTo", "/r/IsA", "/r/HasA", "/r/AtLocation", "/r/PartOf", "/r/UsedFor"],
    "housing": ["/r/IsA", "/r/RelatedTo"],
    "insect": ["/r/IsA", "/r/RelatedTo"],
    "job": ["/r/RelatedTo", "/r/IsA"],
    "kitchen": ["/r/RelatedTo", "/r/UsedFor", "/r/AtLocation"],
    "language": ["/r/IsA", "/r/RelatedTo"],
    "leader": ["/r/IsA", "/r/RelatedTo"],
    "legal": ["/r/SimilarTo", "/r/RelatedTo"],
    "mammal": ["/r/IsA", "/r/RelatedTo"],
    "many": ["/r/SimilarTo", "/r/RelatedTo"],
    "math": ["/r/RelatedTo", "/r/IsA", "/r/Synonym"],
    "measurement": ["/r/RelatedTo", "/r/IsA", "/r/Synonym"],
    "metal": ["/r/RelatedTo", "/r/IsA", "/r/Synonym"],
    "military": ["/r/RelatedTo", "/r/SimilarTo", "/r/Synonym"],
    "money": ["/r/RelatedTo", "/r/AtLocation", "/r/IsA"],
    "musical_instrument": ["/r/RelatedTo", "/r/AtLocation", "/r/IsA"],
    "music": ["/r/RelatedTo", "/r/IsA", "/r/HasProperty", "/r/ReceivesAction"],
    "mythical_monster": ["/r/IsA"],
    "negative_word": ["/r/HasProperty", "/r/RelatedTo"],
    "new_year": ["/r/RelatedTo"],
    "ocean": ["/r/RelatedTo", "/r/AtLocation", "/r/UsedFor"],
    "office": ["/r/RelatedTo", "/r/AtLocation", "/r/IsA"],
    "people": ["/r/RelatedTo", "/r/CapableOf", "/r/IsA", "/r/Desires", "/r/ReceivesAction", "/r/UsedFor"],
    "pirate": ["/r/Synonym", "/r/IsA", "/r/RelatedTo"],
    "plant": ["/r/IsA", "/r/RelatedTo", "/r/AtLocation"],
    "positive_word": ["/r/HasProperty", "/r/RelatedTo"],
    "post_office": ["/r/AtLocation", "/r/RelatedTo", "/r/UsedFor"],
    "reptile": ["/r/IsA", "/r/RelatedTo"],
    "restaurant": ["/r/RelatedTo", "/r/AtLocation", "/r/IsA"],
    "roadway": ["/r/IsA", "/r/RelatedTo"],
    "rock": ["/r/IsA", "/r/RelatedTo", "/r/AtLocation"],
    "room": ["/r/IsA", "/r/RelatedTo", "/r/AtLocation"],
    "school": ["/r/IsA", "/r/RelatedTo", "/r/AtLocation", "/r/UsedFor"],
    "science": ["/r/IsA", "/r/RelatedTo", "/r/DerivedFrom", "/r/UsedFor"],
    "sewing": ["/r/RelatedTo", "/r/IsA", "/r/Causes"],
    "shape": ["/r/IsA"],
    "sport": ["/r/IsA"],
    "store": ["/r/AtLocation", "/r/RelatedTo", "/r/IsA"],
    "time": ["/r/RelatedTo", "/r/IsA", "/r/HasProperty"],
    "tool": ["/r/IsA"],
    "transportation": ["/r/IsA", "/r/RelatedTo"],
    "tree": ["/r/IsA", "/r/RelatedTo", "/r/UsedFor", "/r/CapableOf"],
    "vegetable": ["/r/IsA", "/r/RelatedTo"],
    "water": ["/r/AtLocation", "/r/RelatedTo", "/r/IsA"],
    "weapon": ["/r/IsA"],
    "weather": ["/r/IsA", "/r/RelatedTo"],
    "yard": ["/r/AtLocation", "/r/IsA"]
}
