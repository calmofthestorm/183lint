#include <iostream>
#include <fstream>
#include <string>
#include <cassert>

using namespace std;

// REQUIRES: none
// MODIFIES: opens data_file
// EFFECTS:  with name obtained from user
void open_file(ifstream& data_file)
{
  // A string to hold the NAME of the file to open
  string data_filename;

  // Keep prompting for the filename until the user gets it right.
  do {
    cout << "Please enter the data filename: ";
    getline(cin, data_filename); // Note here we're getting a line from cin NOT
                                 // from a file.

    // Try to open the file the user gave us the name of
    data_file.open(data_filename.c_str());
  } while (!data_file);

  // Abort if data_file not good. Assert is a function that takes a single
  // boolean argument and will immediately exit your program if that is ever
  // false with a helpful message. Great for debugging.
  assert(data_file); 
}

// REQUIRES: data_file be open and good.
// MODIFIES: best_score, worst_score, num_scores, sum_of_scores, best_name
// EFFECTS: reads from the file
void read_file(ifstream& data_file, int& best_score, int& worst_score,
               int& num_scores, int& sum_of_scores, string& best_name)
{
  num_scores = sum_of_scores = 0;

  // Read in students until end of file.
  string name;
  int score;
  data_file >> name >> score;
  while (data_file) {
    // Update the best so far.
    if (score > best_score || num_scores == 0) {
      best_score = score;
      best_name = name;
    }

    // Update the worst so far.
    if (score < worst_score || num_scores == 0) {
      worst_score = score;
    }

    // Keep track of sum and count.
    ++num_scores;
    sum_of_scores += score;

    // Read the next student.
    data_file >> name >> score;
  }
}

// REQUIRES: all stats be valid OR num_scores == 0.
// MODIFIES: none
// EFFECTS: prints a summary of the stats to cout.
void print_stats(int best_score, int worst_score, int num_scores,
                 int sum_of_scores, const string& best_name)
{
  cout << "Displaying stats for " << num_scores << " users:\n";
  if (num_scores > 0) {
    cout << "  Best score: " << best_score << " (" << best_name << ")\n";
    cout << "  Worst score: " << worst_score << endl;
    cout << "  Mean score: " << sum_of_scores / static_cast<double>(num_scores)
         << endl;
  }
}

// REQUIRES: None
// MODIFIES: prints prompt to cout and prompts user to enter y/n until they do.
// EFFECTS: returns true if the user chose y false if they chose n
bool askUserYesNo(string prompt) {
  char choice;
  do {
    cout << "\n\n\nRead another file? (y/n): ";
    cin >> choice;
    choice = tolower(choice);
    string junk;
    getline(cin, junk);
  } while (choice != 'y' && choice != 'n');
  return (choice == 'y');
}

int main()
{
  // An ifstream to keep track of the file itself (an ifstream can be read from
  // using get, getline, and >> just like cin).
  ifstream data_file;

  // Statistics from the file.
  int best_score, worst_score, num_scores, sum_of_scores;
  string best_name;

  bool quit = false;
  while (!quit) {
    // Open the file given by the user.
    open_file(data_file);
  
    // Read the data file and save relevant statistics.
    read_file(data_file, best_score, worst_score, num_scores,
              sum_of_scores, best_name);
  
    // Close the file. This will happen automatically when the function that
    // the ifstream was declared in exits, but it is good to be explicit.
    data_file.close();
  
    // Check that we read a name properly if we read anyone.
    if (num_scores > 0) {
      assert(best_name != "");
    }
  
    // Display the stats to the user
    print_stats(best_score, worst_score, num_scores, sum_of_scores, best_name);

    // Give the user the option to read more files.
    quit = !askUserYesNo("\n\n\nRead another file? (y/n): ");
  }

  return 0;
}