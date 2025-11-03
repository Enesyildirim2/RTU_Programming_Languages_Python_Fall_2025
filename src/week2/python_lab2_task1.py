"""
Lab 3.1 – Simple Datasets and Aggregates

Goals:
- Create and manipulate Python lists and dictionaries.
- Compute aggregates such as sum, average, max, and min.

Instructions:
1. Create a list `temperatures` with daily temperatures for one week.
2. Create a dictionary `city_population` with at least 5 cities and their populations.
3. Compute:
   - The average temperature.
   - The maximum and minimum population.
   - The total population of all cities.
4. Print your results in a clear, formatted way.
"""

# TODO: Create the datasets - up to you to fill in the data
temperatures = [10, 12, 15, 14, 13, 11, 16]
city_population = {"CityA": 500000, "CityB": 1200000, "CityC": 750000, "CityD": 300000, "CityE": 950000}

# TODO: Compute aggregates
average_temperature = sum(temperatures) / len(temperatures)
largest_city = max(city_population.items(), key=lambda x: x[1])
largest_population = max(city_population.values())
total_population = sum(city_population.values())

# TODO: Print results
print("Average temperature:", average_temperature)
print("Largest city:", largest_city, "-", largest_population)
print("Total population:", total_population)
