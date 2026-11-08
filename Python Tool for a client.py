
# Track A Day 5 Project: Python Tool for a Client

print("=" * 40)
print("       CLIENT TASK MANAGEMENT TOOL")
print("=" * 40)

# Keep the program running until the user quits
while True:
    client_name = input("\nEnter the client name (or type 'quit' to exit): ").strip()

    # Check if the user wants to quit
    if client_name.lower() == "quit":
        print("\nExiting the program. Goodbye!")
        break

    # Ask for the task
    task = input("Enter the task for this client: ").strip()

    # Validate the inputs
    if not client_name or not task:
        print("Error: Client name and task cannot be empty.")
        continue

    # Format the task summary
    summary = f"Client: {client_name}, Task: {task}"

    # Display the summary
    print("\n--- ACTION SUMMARY ---")
    print(summary)

    # Save the entry to tasks.txt
    with open("tasks.txt", "a", encoding="utf-8") as file:
        file.write(summary + "\n")

    print("Task saved successfully to tasks.txt!")

print("\nThank you for using the Client Task Management Tool.")
