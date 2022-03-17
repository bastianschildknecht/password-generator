from datetime import timedelta
import secrets
import sys
import argparse
import humanize
from colorama import Fore, Style

UPPER_CASE_CHARS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LOWER_CASE_CHARS = list("abcdefghijklmnopqrstuvwxyz")
NUMBER_CHARS = list("0123456789")
SPECIAL_CHARS = list("!@#$%^&*()")

SECONDS_IN_A_MINUTE = 60
SECONDS_IN_AN_HOUR = SECONDS_IN_A_MINUTE * 60
SECONDS_IN_A_DAY = SECONDS_IN_AN_HOUR * 24
SECONDS_IN_A_WEEK = SECONDS_IN_A_DAY * 7
SECONDS_IN_A_YEAR = SECONDS_IN_A_DAY * 365

AGE_OF_THE_UNIVERSE = 13800000000   # 13.8 billion years old

POTENTIAL_BF_ATTACKS_PER_SECOND = 1000000000    # 1 billion attempts per second

def random_char(upper_case: bool, lower_case: bool, numbers: bool, symbols: bool) -> str:
    """
    Generates a random character based on the given parameters.
    """
    # Create a list of all the characters that can be used
    chars = []
    if upper_case:
        chars.extend(UPPER_CASE_CHARS)
    if lower_case:
        chars.extend(LOWER_CASE_CHARS)
    if numbers:
        chars.extend(NUMBER_CHARS)
    if symbols:
        chars.extend(SPECIAL_CHARS)

    # Generate a random character from the list
    return secrets.choice(chars)

def generate_password(length: int, upper_case: bool, lower_case: bool, numbers: bool, symbols: bool) -> str:
    """
    Generates a random character sequence based on the given parameters.
    """
    # Create an empty string to store the generated characters
    password = ""

    # Generate a random character for each position in the sequence
    for _ in range(length):
        password += random_char(upper_case, lower_case, numbers, symbols)

    # Return the generated password
    return password

def generate_strong_password(length: int) -> str:
    """
    Generates a strong password with the given length.
    The password will contain upper case, lower case, numbers, and symbols.
    """
    # Generate a strong password
    password = generate_password(length, True, True, True, True)

    # Return the generated password
    return password

def compute_possibilites(length: int, upper_case: bool, lower_case: bool, numbers: bool, symbols: bool) -> float:
    """
    Computes the number of possible passwords with the given parameters.
    """
    # Compute the number of possible characters
    possibilities = 0
    if upper_case:
        possibilities += len(UPPER_CASE_CHARS)
    if lower_case:
        possibilities += len(LOWER_CASE_CHARS)
    if numbers:
        possibilities += len(NUMBER_CHARS)
    if symbols:
        possibilities += len(SPECIAL_CHARS)

    possibilities = possibilities ** length

    # Return the number of possibilities
    return possibilities

def get_timedelta(seconds: int) -> timedelta:
    """
    Converts seconds to a timedelta.
    """
    # Check if the number is too large to be converted to a timedelta
    if seconds > timedelta.max.total_seconds():
        return timedelta.max

    # Calculate the number of days, hours, minutes, and seconds
    weeks = seconds // SECONDS_IN_A_WEEK
    seconds -= weeks * SECONDS_IN_A_WEEK
    days = seconds // SECONDS_IN_A_DAY
    seconds -= days * SECONDS_IN_A_DAY
    hours = seconds // SECONDS_IN_AN_HOUR
    seconds -= hours * SECONDS_IN_AN_HOUR
    minutes = seconds // SECONDS_IN_A_MINUTE
    seconds -= minutes * SECONDS_IN_A_MINUTE

    # Return the timedelta
    return timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)

def get_natural_time_string(seconds: int) -> str:
    """
    Returns a natural time string given the number of seconds.
    """
    # Check if the number is too large to be converted to a timedelta
    if seconds > timedelta.max.total_seconds():

        years = seconds // SECONDS_IN_A_YEAR

        # Check if the number is small enough to be stated in years
        if years > AGE_OF_THE_UNIVERSE:
            # The number is too large to be stated in years -> state in terms of the age of the universe
            aou = years // AGE_OF_THE_UNIVERSE
            return "%s times the age of the universe" % humanize.intword(aou)
        else:
            # Return the time in terms of years
            return "%s years" % humanize.intword(years)
    
    return humanize.naturaldelta(get_timedelta(seconds))

def main(argc: int, argv: list) -> None:
    """
    Main function.
    """

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="generates a random password with the given length and parameters")
    parser.add_argument("length", type=int, help="the length of the password to generate")
    parser.add_argument("-u", "--upper-case", action="store_true", help="include upper case characters")
    parser.add_argument("-l", "--lower-case", action="store_true", help="include lower case characters")
    parser.add_argument("-n", "--numbers", action="store_true", help="include numbers")
    parser.add_argument("-s", "--symbols", action="store_true", help="include symbols")
    args = parser.parse_args(argv[1:])

    # Check if the length is valid
    if args.length < 1:
        print("The length must be at least 1.")
        sys.exit(1)
    
    # Print header
    print("\nPASSWORD GENERATOR")
    print("==================")

    # If no characters are specified, default to upper case, lower case, numbers, and symbols
    if not args.upper_case and not args.lower_case and not args.numbers and not args.symbols:
        args.upper_case = True
        args.lower_case = True
        args.numbers = True
        args.symbols = True
        print("No characters specified. Defaulting to upper case, lower case, numbers, and symbols.")

    # Print information about the strength of the password
    possibilities = compute_possibilites(args.length, args.upper_case, args.lower_case, args.numbers, args.symbols)
    print("With the given parameters, the generated password is one of %s possible passwords." % (humanize.intword(possibilities)))
    print("It will take an attacker approx. %s to brute force the password." % (get_natural_time_string(possibilities // POTENTIAL_BF_ATTACKS_PER_SECOND)))
    print("It may be much less with more sophisticated attacks (e.g. rainbow tables).\n")

    # Generate the password
    password = generate_password(args.length, args.upper_case, args.lower_case, args.numbers, args.symbols)
    print("The generated password is: " + Fore.GREEN+ "\n%s\n" % (password) + Style.RESET_ALL)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)