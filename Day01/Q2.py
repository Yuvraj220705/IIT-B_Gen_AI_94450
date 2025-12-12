def count_even_odd():
    numbers = input("Enter numbers separated by commas: ")

    try:
        # Convert input into a list of integers
        nums = [int(n.strip()) for n in numbers.split(",")]

        # Count even and odd numbers
        even_count = sum(1 for n in nums if n % 2 == 0)
        odd_count = len(nums) - even_count

        # Print results
        print("\n--- Results ---")
        print(f"Input list: {nums}")
        print(f"Total Even Numbers: {even_count}")
        print(f"Total Odd Numbers: {odd_count}")
        print("----------------")

    except ValueError:
        print("Error: Please enter only numbers separated by commas.")

count_even_odd()
