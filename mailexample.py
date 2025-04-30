import os
import pickle

# Define the Contact class
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Email: {self.email}"

    def to_dict(self):
        return {'name': self.name, 'phone': self.phone, 'email': self.email}

    @staticmethod
    def from_dict(contact_dict):
        return Contact(contact_dict['name'], contact_dict['phone'], contact_dict['email'])

# Define the ContactBook class that manages the contacts
class ContactBook:
    def __init__(self, filename='contacts.pkl'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def add_contact(self, contact):
        """Add a new contact to the contact book."""
        if self.find_contact_by_name(contact.name):
            print(f"Contact with name '{contact.name}' already exists!")
            return
        self.contacts.append(contact)
        print(f"Contact '{contact.name}' added successfully!")
        self.save_contacts()

    def delete_contact(self, name):
        """Delete a contact by name."""
        contact = self.find_contact_by_name(name)
        if contact:
            self.contacts.remove(contact)
            print(f"Contact '{name}' deleted successfully!")
            self.save_contacts()
        else:
            print(f"No contact found with name '{name}'!")

    def search_contact(self, name):
        """Search for a contact by name."""
        contact = self.find_contact_by_name(name)
        if contact:
            print(contact)
        else:
            print(f"No contact found with name '{name}'!")

    def list_contacts(self):
        """List all contacts."""
        if not self.contacts:
            print("No contacts available.")
        else:
            print("\nContact List:")
            for contact in self.contacts:
                print(contact)

    def find_contact_by_name(self, name):
        """Helper function to find a contact by name."""
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None

    def load_contacts(self):
        """Load contacts from the file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as file:
                try:
                    contacts = pickle.load(file)
                    print(f"Loaded {len(contacts)} contacts.")
                    return contacts
                except Exception as e:
                    print(f"Failed to load contacts: {e}")
                    return []
        return []

    def save_contacts(self):
        """Save the contacts to the file."""
        with open(self.filename, 'wb') as file:
            try:
                pickle.dump(self.contacts, file)
                print("Contacts saved successfully!")
            except Exception as e:
                print(f"Failed to save contacts: {e}")

# Main function to handle user input and control flow
def main():
    contact_book = ContactBook()

    while True:
        print("\n===== Contact Book =====")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Delete Contact")
        print("4. List Contacts")
        print("5. Exit")
        
        choice = input("Please select an option (1-5): ").strip()

        if choice == '1':
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email: ").strip()
            contact = Contact(name, phone, email)
            contact_book.add_contact(contact)

        elif choice == '2':
            name = input("Enter name to search: ").strip()
            contact_book.search_contact(name)

        elif choice == '3':
            name = input("Enter name to delete: ").strip()
            contact_book.delete_contact(name)

        elif choice == '4':
            contact_book.list_contacts()

        elif choice == '5':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()
