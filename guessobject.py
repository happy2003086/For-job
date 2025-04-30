class QuestionNode:
    def __init__(self, question=None, yes=None, no=None, object_name=None):
        self.question = question  # The question at this node
        self.yes = yes  # The "yes" branch
        self.no = no  # The "no" branch
        self.object_name = object_name  # The object name if it's a leaf node

# Define the decision tree
def build_tree():
    root = QuestionNode("Is it an animal?")
    
    # Animal path
    root.yes = QuestionNode("Does it have four legs?")
    root.yes.yes = QuestionNode(object_name="Dog")
    root.yes.no = QuestionNode(object_name="human")
    
    # Non-animal path
    root.no = QuestionNode("Is it used for transportation?")
    root.no.yes = QuestionNode("Does it require driving to use?")
    root.no.yes.yes = QuestionNode(object_name="Car")
    root.no.yes.no = QuestionNode(object_name="Airplane")
    
    root.no.no = QuestionNode("Can it be eaten?")
    root.no.no.yes = QuestionNode("Is it a type of fruit?")
    root.no.no.yes.yes = QuestionNode(object_name="Apple")
    root.no.no.yes.no = QuestionNode(object_name="Banana")
    
    root.no.no.no = QuestionNode("Does it have a screen?")
    root.no.no.no.yes = QuestionNode("Does it need electricity to work?")
    root.no.no.no.yes.yes = QuestionNode(object_name="TV")
    root.no.no.no.yes.no = QuestionNode(object_name="Laptop")
    
    root.no.no.no.no = QuestionNode("Can you wear it?")
    root.no.no.no.no.yes = QuestionNode(object_name="Shoes")
    
    root.no.no.no.no.no = QuestionNode("Is it used to play sports?")
    root.no.no.no.no.no.yes = QuestionNode(object_name="Football")
    
    return root

# Ask questions recursively
def ask_question(node):
    if node.object_name:
        print(f"The object you're thinking of is: {node.object_name}!")
        return
    
    answer = input(f"{node.question} (yes/no): ").strip().lower()
    if answer == "yes":
        ask_question(node.yes)
    elif answer == "no":
        ask_question(node.no)
    else:
        print("Please respond with 'yes' or 'no'.")
        ask_question(node)

# Main function
def play_game():
    print("Welcome to the 20Q game!")
    root = build_tree()
    ask_question(root)

if __name__ == "__main__":
    play_game()
