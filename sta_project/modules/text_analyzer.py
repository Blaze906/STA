# Logic for the text_analyzer module

def analyze_text(file_path):
    """
    Analyzes a text file to count the total number of words
    and calculate the average word length.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return

    words = content.split()
    total_words = len(words)

    if total_words == 0:
        avg_word_length = 0
    else:
        total_word_length = sum(len(word) for word in words)
        avg_word_length = total_word_length / total_words

    # Get the file name for the report
    import os
    file_name = os.path.basename(file_path)

    # Output formatting
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print(f"║ ANALISI FILE: {file_name:<40} ║")
    print("║                                                           ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    print("║                                                           ║")
    print(f"║ Numero Totale di Parole: {total_words:<29} ║")
    print(f"║ Lunghezza Media Parole: {avg_word_length:<28.2f} caratteri ║") # Ensure 2 decimal places
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")

if __name__ == '__main__':
    # Example usage (for testing directly)
    # Create a dummy file for testing
    dummy_file_path = "dummy_document.txt"
    with open(dummy_file_path, "w", encoding="utf-8") as f:
        f.write("Questo è un file di prova per testare l'analizzatore di testo. Contiene alcune parole di esempio.")

    analyze_text(dummy_file_path)

    # Clean up the dummy file
    import os
    os.remove(dummy_file_path)

    analyze_text("non_existent_file.txt")
