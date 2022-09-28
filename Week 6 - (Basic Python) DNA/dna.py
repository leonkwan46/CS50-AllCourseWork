import csv
import sys


def main():

    # Check for command-line usage
    if (len(sys.argv)) < 3:
        print("Please Try Again!")
        exit(1)

    # Read database file into a variable
    dna = open(sys.argv[2]).read()
    with open(sys.argv[1], 'r') as file:

        # Read DNA sequence file into a variable
        reader = csv.DictReader(file)
        str_group = reader.fieldnames[1:]
        str_count = {}

        # Find longest match of each STR in DNA sequence
        for STR in str_group:
            index = 0
            curSequence = 0
            longest = 0

            while index < len(dna):
                curSTR = dna[index: index + len(STR)]

                if curSTR == STR:
                    curSequence += 1
                    index += len(STR)
                else:
                    if curSequence > longest:
                        longest = curSequence
                    curSequence = 0
                    index += 1
            str_count[STR] = longest

        # Check database for matching profiles
        for person in reader:
            name = person['name']
            found = True

            for STR in str_group:
                if int(person[STR]) != str_count[STR]:
                    found = False
                    break

            if found:
                print(name)
                exit(2)

        print("No Match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()