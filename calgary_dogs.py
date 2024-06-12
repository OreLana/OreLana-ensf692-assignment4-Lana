# calgary_dogs.py
# Oreoluwa Lana
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd

class DogBreedData:
    def __init__(self, file_path):
        """
        Initializing the DogBreedData class with data from the given Excel file.

        Parameters:
        - file_path (str): The path to the Excel file containing dog breed data.
        """
        self.data = pd.read_excel(file_path, sheet_name='Sheet1') #dataFrame containg the dogs data
        self.data['Breed'] = self.data['Breed'].str.lower()  # make all breed names lowercase
        self.data.set_index(['Year', 'Month'], inplace=True) 

    def get_breed_data(self, dog_breed):
        """
        Get data for a specific dog breed.

        Parameters:
        - breed (str): The name of the dog breed.

        Returns:
        - pd.DataFrame: A DataFrame containing data for the specified breed.
        """
        dog_breed = dog_breed.lower()
        if dog_breed not in self.data['Breed'].values:
            raise KeyError("Dog breed not found in the data. Please try again.")
        # Masking operation to filter the breed data
        breed_data = self.data[self.data['Breed'] == dog_breed]
        return breed_data

class DogBreedAnalysis:
    def __init__(self, breed_data):
        """
        Initialize the DogBreedAnalysis class with data for a specific breed.

        Parameters:
        - breed_data (pd.DataFrame): A DataFrame containing data for the specified breed.
        """
        self.breed_data = breed_data

    def get_years(self):
        """
        Get all years where the breed was listed in the top breeds.

        Returns:
        - str: A string of years separated by spaces.
        """
        years = self.breed_data.index.get_level_values('Year').unique()
        return ' '.join(map(str, years))

    def get_total_registrations(self):
        """
        Calculate the total number of registrations of the breed.

        Returns:
        - int: The total number of registrations.
        """
        return self.breed_data['Total'].sum()

    def get_yearly_percentages(self, overall_data):
        """
        Calculate the percentage of breed registrations out of the total percentage for each year.

        Parameters:
        - overall_data (pd.DataFrame): The entire dataset of dog breeds.

        Returns:
        - dict: A dictionary with years as keys and percentages as values.
        """
        yearly_totals = overall_data.loc[pd.IndexSlice[:, :], :].groupby('Year')['Total'].sum()  # Grouping operation
        breed_yearly_totals = self.breed_data.groupby('Year')['Total'].sum()
        return (breed_yearly_totals / yearly_totals * 100).to_dict()

    def get_overall_percentage(self, overall_total):
        """
        Calculate the percentage of breed registrations out of the total three-year percentage.

        Parameters:
        - overall_total (int): The total number of dog registrations in the dataset.

        Returns:
        - float: The overall percentage of breed registrations.
        """
        total_registrations = self.get_total_registrations()
        return total_registrations / overall_total * 100

    def get_popular_months(self):
        """
        Find the months that were most popular for the breed registrations.

        Returns:
        - str: A string of the most popular months separated by spaces.
        """
        months_data = self.breed_data.reset_index()['Month'].value_counts()  # Masking operation
        max_count = months_data.max()
        popular_months = months_data[months_data == max_count].index.tolist()
        return ' '.join(popular_months)

def main():
    # Import data here
    dog_data = DogBreedData('CalgaryDogBreeds.xlsx')
    
    print("ENSF 692 Dogs of Calgary")
    
    # User input stage
    while True:
        try:
            dog_breed = input("Please enter a dog breed: ").strip()
            breed_data = dog_data.get_breed_data(dog_breed)
            break
        except KeyError as e:
            print(e)
    
    dog_breed = dog_breed.upper()
    
    # Data analysis stage
    analysis = DogBreedAnalysis(breed_data)
    
    years_str = analysis.get_years()
    total_registrations = analysis.get_total_registrations()
    yearly_percentages = analysis.get_yearly_percentages(dog_data.data)
    overall_total = dog_data.data['Total'].sum()
    overall_percentage = analysis.get_overall_percentage(overall_total)
    popular_months_str = analysis.get_popular_months()
    
    # Output results
    print(f"The {dog_breed} was found in the top breeds for years: {years_str}")
    print(f"There have been {total_registrations} {dog_breed} dogs registered total.")
    for year, percentage in yearly_percentages.items():
        print(f"The {dog_breed} was {percentage:.6f}% of top breeds in {year}.")
    print(f"The {dog_breed} was {overall_percentage:.6f}% of top breeds across all years.")
    print(f"Most popular month(s) for {dog_breed} dogs: {popular_months_str}")

if __name__ == '__main__':
    main()
