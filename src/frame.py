import os
from bs4 import BeautifulSoup

# --- Configuration Paths ---
# These paths are relative to where you run this Python script.
# Assuming this script is located at the root of your project (same level as 'app', 'view', etc.)
NAV_FILE_PATH = os.path.join('view', 'widgets', 'navbar.html')
# Assuming 'footer.html' will also be placed in the 'view/widgets' directory.
FOOTER_FILE_PATH = os.path.join('view', 'widgets', 'footer.html')
TARGET_DIR = os.path.join('view', 'pages')

def read_html_content(file_path):
    """
    Reads the content of an HTML file and returns it.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Source file not found at '{file_path}'. Please ensure the path is correct and the file exists.")
        return None
    except Exception as e:
        print(f"An error occurred while reading '{file_path}': {e}")
        return None

def update_navbar_in_file(target_file_path, nav_content):
    """
    Opens a target HTML file, finds the <nav> tag, replaces its content,
    and saves the modified file.
    """
    try:
        with open(target_file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        nav_tag = soup.find('nav')
        if nav_tag:
            nav_tag.clear() # Remove existing content inside <nav>
            nav_tag.append(BeautifulSoup(nav_content, 'html.parser')) # Add new content
            print(f"Updated <nav> in '{target_file_path}'")
        else:
            print(f"Warning: <nav> tag not found in '{target_file_path}'. Skipping navigation update for this file.")

        with open(target_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        # print(f"Successfully saved changes to '{target_file_path}'") # This is already printed by process_html_files

    except FileNotFoundError:
        print(f"Error: Target file not found at '{target_file_path}'. Skipping update for this file.")
    except Exception as e:
        print(f"An error occurred while processing '{target_file_path}': {e}")

def update_footer_in_file(target_file_path, footer_content):
    """
    Opens a target HTML file, finds the <footer> tag, replaces its content,
    and saves the modified file.
    """
    try:
        with open(target_file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        footer_tag = soup.find('footer')
        if footer_tag:
            footer_tag.clear() # Remove existing content inside <footer>
            footer_tag.append(BeautifulSoup(footer_content, 'html.parser')) # Add new content
            print(f"Updated <footer> in '{target_file_path}'")
        else:
            print(f"Warning: <footer> tag not found in '{target_file_path}'. Skipping footer update for this file.")

        with open(target_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        # print(f"Successfully saved changes to '{target_file_path}'") # This is already printed by process_html_files

    except FileNotFoundError:
        print(f"Error: Target file not found at '{target_file_path}'. Skipping update for this file.")
    except Exception as e:
        print(f"An error occurred while processing '{target_file_path}': {e}")

def process_html_files(nav_html, footer_html, update_nav, update_footer):
    """
    Walks through the target directory and updates HTML files based on user choice.
    """
    print(f"\nSearching for HTML files in '{TARGET_DIR}'...")
    html_files_found = False
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html'):
                html_files_found = True
                full_path = os.path.join(root, file)
                print(f"\nProcessing: {full_path}")
                if update_nav:
                    # Only attempt navbar update if nav_html content was successfully read
                    if nav_html is not None:
                        update_navbar_in_file(full_path, nav_html)
                    else:
                        print(f"Skipping navbar update for '{full_path}' due to missing source content.")
                if update_footer:
                    # Only attempt footer update if footer_html content was successfully read
                    if footer_html is not None:
                        update_footer_in_file(full_path, footer_html)
                    else:
                        print(f"Skipping footer update for '{full_path}' due to missing source content.")
                print(f"Finished processing '{full_path}'.")

    if not html_files_found:
        print(f"No HTML files found in '{TARGET_DIR}'.")
    else:
        print("\nAll selected HTML files processed!")

def main():
    print("--- HTML Content Updater ---")

    # Attempt to read source content once at the start
    nav_html_content = read_html_content(NAV_FILE_PATH)
    footer_html_content = read_html_content(FOOTER_FILE_PATH)

    # If both source files are missing, there's nothing to do
    if nav_html_content is None and footer_html_content is None:
        print("Neither navbar nor footer source files could be read. Please ensure they exist at the configured paths.")
        return

    while True:
        print("\nWhat would you like to update?")
        print("1. Navigation Bar")
        print("2. Footer")
        print("3. Both Navigation Bar and Footer")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        update_nav = False
        update_footer = False

        if choice == '1':
            if nav_html_content is None:
                print("Cannot update navigation bar: Source file is missing or unreadable.")
                continue
            update_nav = True
        elif choice == '2':
            if footer_html_content is None:
                print("Cannot update footer: Source file is missing or unreadable.")
                continue
            update_footer = True
        elif choice == '3':
            if nav_html_content is None and footer_html_content is None:
                print("Cannot update both: Both source files are missing or unreadable.")
                continue
            if nav_html_content is None:
                print("Warning: Navbar source file is missing. Will only attempt to update footer.")
            if footer_html_content is None:
                print("Warning: Footer source file is missing. Will only attempt to update navbar.")
            update_nav = True
            update_footer = True
        elif choice == '4':
            print("Exiting HTML Content Updater. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            continue

        # Proceed with processing based on user's valid choice
        process_html_files(nav_html_content, footer_html_content, update_nav, update_footer)
        print("\nUpdate round complete!")

if __name__ == "__main__":
    main()
