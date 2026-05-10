from agent import run_agent

def main():
    print("🤖 Advanced AWS AI Agent Started (type 'exit' to quit)\n")

    while True:
        user_input = input("👉 You: ")

        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break

        response = run_agent(user_input)

        print("🤖 AI:", response)


if __name__ == "__main__":
    main()