import random

def generate_random_poem():
    subjects = ["The moon", "A gentle breeze", "The ocean waves", "A lonely star", "The whispering trees", 
                "A fleeting shadow", "The morning sun", "A distant memory", "The falling leaves", "A silent night"]
    verbs = ["dances", "sings", "whispers", "shines", "cries", "dreams", "fades", "glows", "calls", "wanders"]
    adjectives = ["soft", "bright", "melancholic", "serene", "mysterious", "gentle", "fading", "radiant", "silent", "echoing"]
    adverbs = ["silently", "gracefully", "softly", "endlessly", "brightly", "wistfully", "gently", "quietly", "boldly", "dreamily"]

    poem = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(adverbs)} in the {random.choice(adjectives)} night."
    return poem

while True:
    print(generate_random_poem())
    user_input = input("Generate another poem? (y/n): ")
    if user_input.lower() != 'y':
        break