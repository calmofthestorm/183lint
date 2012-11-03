/* ============================================================
* Copyright 2012 Adam Schnitzer
*
* Implementation of the Sieve of Eratosthenes.
* ============================================================
* This is an efficient algorithm to find all prime numbers from 2
* to a specified end value. The algorithm works by using a vector
* of all possible value from 2 to n. The algorithm then steps through
* the array, updating whether or not the value is prime.
*
* Vector was chosen over array, because a vector of boolean values is
* automatically bitwise, saving a significant amount of memory.
* ============================================================
* The sieve is implemented using the following method:
*
* Input: (n), an integer greater than 2
*
* (numbers), an array of boolean values, with values corresponding with 2 to
* (n). All values are initialized to true.
*
* for each value (i) of (numbers), from 2 to n:
* if the current element of (number)[i] is true:
* for all remaining elements of the array, from
* [i] to (n), which are multiples of [i], shall
* be false.
*
* All values of (numbers) from 2 to n, which are true, are prime.
* ============================================================ */

#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

const unsigned long long max_end_value = UINT_MAX;

// Requires: end_value > 2,
// end_value < UINT_MAX,
// is_prime is empty
// Modifies: is_prime
// Effects: end_value bools are added to is_prime. Each bool corresponds
// with a number. If the bool corresponding to the number is true,
// that number is prime.
// eg. is_prime.at(7) == true // because 7 is prime
void RunSieve(unsigned int end_value, vector<bool> &is_prime);

// Requires: end_value > 2,
// is_prime.size() >= end_value, is_prime contains
// valid prime numbers in the format is_prime.at(7) == true
// Modifies: nothing
// Effects: prompts user for desired output type. Then prints output in
// either ListPrintPrimes or PrettyPrintPrimes format.
void RunPrintPrimes(vector<bool> &is_prime, unsigned int end_value);


// Effects: prompts the user for a valid end_value for RunSieve(). Returns
// end value which corresponds with requirements for RunSieve().
unsigned int PromptEndValue();

// Requires: end_value > 2,
// is_prime.size() >= end_value,
// is_prime contains valid prime numbers in the format:
// is_prime.at(7) == true
// Modifies: nothing
// Effects: Prints "The prime numbers until X are:" where X is end_value.
// followed by a list of the prime numbers from 2 to X inclusive,
// with one prime per line.
void ListPrintPrimes(unsigned int end_value, const vector<bool> &is_prime);

// Requires: end_value > 2,
// is_prime.size() >= end_value, is_prime contains
// valid prime numbers in the format is_prime.at(7) == true.
// primes_per_line is between 1 and 10 inclusive, or not included.
// Modifies: nothing
// Effects: Prints out the primes from two to end_value inclusive. The header
// message will be: "Prime numbers to X are:"
// --------------------------------
// Where X is end_value. There are primes_per_line primes per line.
void PrettyPrintPrimes(unsigned int end_value, const vector<bool> &is_prime,
                       int primes_per_line = 5);

void RunSieve(unsigned int end_value, vector<bool> &is_prime)
{
    // square_root truncated because primes will be found before the square root
    unsigned int square_root = static_cast<int>(sqrt((double)end_value));

    // reserves memory for all values, and initializes vector to true
    is_prime.reserve(end_value + 1);
    is_prime.insert(is_prime.begin(), end_value + 1, true);

    // see the top of the file for an overview of the algorithm used
    for (unsigned int i = 2; i <= square_root; ++i) {
        if (is_prime.at(i)) {
            for (unsigned int k = i * i; k <= end_value; k += i) {
                is_prime.at(k) = false;
            }
        }
    }
}

void RunPrintPrimes(vector<bool> &is_prime, unsigned int end_value)
{
    int print_type = 0;
    cout << endl << "Your calculation has completed!" << endl
        << "Enter '1' if you would like the primes printed in a list." << endl
        << "Enter '2' if you would like pretty print" << endl << endl;

    cin >> print_type;
    bool in_bounds = print_type == 1 || print_type == 2;

    while (!cin.good() || !in_bounds) {
        cout << endl << "\tERROR: Invalid Input. Try again" << endl;
        cin.clear();
        string read_buffer;
        getline(cin, read_buffer);

        cin >> print_type;
        in_bounds = print_type == 1 || print_type == 2;
    }

    // simple list
    if (print_type == 1) {
        ListPrintPrimes(end_value, is_prime);
        // pretty print
    } else {
        int num_per_line = 0;
        cout << "How many numbers per line? or enter 0 for default" << endl;
        while (!(cin >> num_per_line) || num_per_line < 0) {
            cout << endl << "\tERROR: Invalid Input. Try again" << endl;
            cin.clear();
            string read_buffer;
            getline(cin, read_buffer);
        }

        // user specified primes per line
        if (num_per_line != 0) {
            PrettyPrintPrimes(end_value, is_prime, num_per_line);
            // default primes per line
        } else {
            PrettyPrintPrimes(end_value, is_prime);
        }
    }
}

unsigned int PromptEndValue()
{
    long end_value;
    cout << "Enter the end value for the sieve. Must be less than "
        << max_end_value << ": ";

    cin >> end_value;
    bool in_bounds = end_value < max_end_value && end_value > 2;

    while (!cin.good() || !in_bounds) {
        cout << endl << "\tERROR: Invalid Input. Try again" << endl;
        // algorithm for bad input: clears flag on cin, then clears the buffer
        cin.clear();
        string read_buffer;
        getline(cin, read_buffer);

        cin >> end_value;
        in_bounds = end_value < max_end_value && end_value > 2;
    }

    return end_value;
}

void ListPrintPrimes(unsigned int end_value, const vector<bool> &is_prime)
{
    cout << "The prime numbers until " << end_value << " are:" << endl;
    // iterates through whole vector, checking if the current bool is true
    // if true, it means i is a prime number
    for (unsigned int i = 2; i <= end_value; ++i) {
        if (is_prime.at(i)) {
            cout << i << endl;
        }
    }
}

void PrettyPrintPrimes(unsigned int end_value, const vector<bool> &is_prime,
                       int primes_per_line)
{
    cout << "Prime numbers to " << end_value << " are:" << endl
        << "--------------------------------" << endl;

    int in_line = 0;

    for (unsigned int i = 2; i <= end_value; ++i) {
        if (is_prime.at(i)) {
            // meaning there are primes_per_line values in current line
            if (in_line % primes_per_line == 0) {
                cout << endl;
            }
            cout << setw(primes_per_line);
            cout << i << " ";
            in_line += 1;
        }
    }
}

int main()
{
    unsigned int end_value = PromptEndValue();

    cout << endl << "Your calculation is processing. Please be patient."
        << endl << "This can take several minutes." << endl;

    vector<bool> is_prime;
    RunSieve(end_value, is_prime);

    RunPrintPrimes(is_prime, end_value);

    return 0;
}
