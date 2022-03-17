from datetime import timedelta
import secrets
import sys
import argparse
import humanize
from colorama import Fore, Style


UPPER_CASE_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LOWER_CASE_CHARS = set("abcdefghijklmnopqrstuvwxyz")
NUMBER_CHARS = set("0123456789")
SYMBOL_CHARS = set("!@#$%^&*()")

SECONDS_IN_A_YEAR = 365 * 24 * 60 * 60
AGE_OF_THE_UNIVERSE_Y = 13800000000   # 13.8 billion years old

POTENTIAL_BF_ATTACKS_PER_SECOND = 1000000000    # 1 billion attempts per second



def assemble_charset(upper_case: bool, lower_case: bool, numbers: bool, symbols: bool) -> list:
    """
    Assembles the character set based on the given parameters.
    
    Args:
        upper_case: Whether to include upper case characters.
        lower_case: Whether to include lower case characters.
        numbers: Whether to include numbers.
        symbols: Whether to include symbols.

    Returns:
        A list of characters contained in the character set.
    """
    # Create an empty set to store the character set
    charset = set()

    # Add the characters to the set
    if upper_case:
        charset.update(UPPER_CASE_CHARS)
    if lower_case:
        charset.update(LOWER_CASE_CHARS)
    if numbers:
        charset.update(NUMBER_CHARS)
    if symbols:
        charset.update(SYMBOL_CHARS)

    # Return the character set
    return list(charset)



def generate_password(length: int, upper_case: bool, lower_case: bool, numbers: bool, symbols: bool) -> str:
    """
    Generates a random character sequence based on the given parameters.

    Args:
        length: The length of the character sequence to generate.
        upper_case: Whether to include upper case characters.
        lower_case: Whether to include lower case characters.
        numbers: Whether to include numbers.
        symbols: Whether to include symbols.
    
    Returns:
        A random character sequence of the given length based on the given parameters.
    """

    # Construct the character set based on the given parameters
    charset = assemble_charset(upper_case, lower_case, numbers, symbols)

    # Create an empty string to store the generated characters
    password = ""

    # Generate a random character for each position in the sequence
    for _ in range(length):
        password += secrets.choice(charset)

    return password



def compute_possibilities(length: int, upper_case: bool, lower_case: bool, numbers: bool, symbols: bool) -> float:
    """
    Computes the size of the password space based on the given parameters.

    Args:
        length: The length of the password.
        upper_case: Whether to include upper case characters.
        lower_case: Whether to include lower case characters.
        numbers: Whether to include numbers.
        symbols: Whether to include symbols.

    Returns:
        The size of the password space in terms of the number of possible passwords.
    """
    # Compute the number of possible characters
    possible_chars = 0
    if upper_case:
        possible_chars += len(UPPER_CASE_CHARS)
    if lower_case:
        possible_chars += len(LOWER_CASE_CHARS)
    if numbers:
        possible_chars += len(NUMBER_CHARS)
    if symbols:
        possible_chars += len(SYMBOL_CHARS)

    possibilities = possible_chars ** length

    return possibilities



def get_timedelta(seconds: int) -> timedelta:
    """
    Converts seconds to a timedelta object.

    Args:
        seconds: The number of seconds to convert to a timedelta object.
    
    Returns:
        A timedelta object representing the given number of seconds if the number of seconds is not too large.
        The biggest timedelta object otherwise.
    """
    # Check if the number is too large to be converted to a timedelta
    if seconds > timedelta.max.total_seconds():
        return timedelta.max

    # Return the timedelta
    return timedelta(seconds=seconds)



def get_natural_time_string(seconds: int) -> str:
    """
    Returns a natural time string given the number of seconds.

    Args:
        seconds: The number of seconds to convert to a natural time string.

    Returns:
        A human readable string representing the given number of seconds.
        If possible, the time duration is converted to a more relatable time duration.
    """
    # Check if the number is too large to be converted to a timedelta
    if seconds > timedelta.max.total_seconds():

        years = seconds // SECONDS_IN_A_YEAR

        # Check if the number is small enough to be stated in years
        if years > AGE_OF_THE_UNIVERSE_Y:
            # The number is too large to be stated in years -> state in terms of the age of the universe
            aou = years // AGE_OF_THE_UNIVERSE_Y
            return "%s times the age of the universe" % humanize.intword(aou)
        else:
            # Return the time in terms of years
            return "%s years" % humanize.intword(years)
    
    return humanize.naturaldelta(get_timedelta(seconds))



def optional_print(string: str, suppress: bool = False) -> None:
    """
    Prints the given string if the given boolean is True.

    Args:
        string: The string to print.
        suppress: Whether to suppress the string. Defaults to False.
    """
    if not suppress:
        print(string)



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
    parser.add_argument("-q", "--quiet", action="store_true", help="only print password")
    args = parser.parse_args(argv[1:])

    # Check if the length is valid
    if args.length < 1:
        optional_print("The length must be at least 1.", args.quiet)
        sys.exit(1)
    
    # Print header
    optional_print("\nPASSWORD GENERATOR", args.quiet)
    optional_print("==================", args.quiet)

    # If no characters are specified, default to upper case, lower case, numbers, and symbols
    if not args.upper_case and not args.lower_case and not args.numbers and not args.symbols:
        args.upper_case = True
        args.lower_case = True
        args.numbers = True
        args.symbols = True
        optional_print("No characters specified. Defaulting to upper case, lower case, numbers, and symbols.", args.quiet)

    if (not args.quiet):
        # Print information about the strength of the password
        possibilities = compute_possibilities(args.length, args.upper_case, args.lower_case, args.numbers, args.symbols)
        print("With the given parameters, the generated password is one of %s possible passwords." % (humanize.intword(possibilities)))
        print("It will take an attacker approx. %s to brute force the password." % (get_natural_time_string(possibilities // POTENTIAL_BF_ATTACKS_PER_SECOND)))
        print("It may be much less with more sophisticated attacks (e.g. rainbow tables).\n")

    # Generate the password
    password = generate_password(args.length, args.upper_case, args.lower_case, args.numbers, args.symbols)

    # Print the password
    if (not args.quiet):
        print("The generated password is: " + Fore.GREEN+ "\n%s\n" % (password) + Style.RESET_ALL)
    else:
        print(password)



if __name__ == "__main__":
    main(len(sys.argv), sys.argv)