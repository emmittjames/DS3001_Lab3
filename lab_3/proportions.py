import pandas as pd
import networkx as nx
from collections import defaultdict

county_data = pd.read_csv("counties_with_adjancencies.csv")

graph = nx.Graph()
for idx, row in county_data.iterrows():
    graph.add_node(row['county'], population=row['totalpopulation'], democrat=row['democrat'], republican=row['republican'], other=row['other'])
    neighbors = row[5:].dropna().values
    for neighbor in neighbors:
        graph.add_edge(row['county'], neighbor)



def grow_district(graph, start_county, target_population_range):
    current_population = graph.nodes[start_county]['population']
    district = [start_county]
    candidates = list(graph.neighbors(start_county))
    while current_population < target_population_range[0]:
        if not candidates:
            break
        candidate = max(candidates, key=lambda x: graph.nodes[x]['republican'])
        candidates.remove(candidate)
        current_population += graph.nodes[candidate]['population']
        district.append(candidate)
        candidates.extend([n for n in graph.neighbors(candidate) if n not in district])
    return district, current_population


def gerrymander(graph, districts, target_population_range, max_targeted_districts, party):
    result = defaultdict(list)
    unassigned_counties = set(graph.nodes)

    for i in range(1, districts + 1):
        if not unassigned_counties:
            break

        if i <= max_targeted_districts:
            starting_county = max(unassigned_counties, key=lambda x: graph.nodes[x][party])
        else:
            starting_county = min(unassigned_counties, key=lambda x: graph.nodes[x][party])

        result[i].append(starting_county)
        unassigned_counties.remove(starting_county)
        district_population = graph.nodes[starting_county]['population']

        while district_population < target_population_range[0] and unassigned_counties:
            next_county = None
            min_diff = float('inf')

            for county in unassigned_counties:
                new_population = district_population + graph.nodes[county]['population']
                if target_population_range[0] <= new_population <= target_population_range[1]:
                    next_county = county
                    break

                diff = abs(new_population - target_population_range[0])
                if diff < min_diff:
                    min_diff = diff
                    next_county = county

            if next_county:
                result[i].append(next_county)
                unassigned_counties.remove(next_county)
                district_population += graph.nodes[next_county]['population']
            else:
                break

    return result



districts = 11
target_population_range = (770000, 805000)
max_republican_districts = 4
max_democrat_districts = 4

gerrymandered_districts_republican = gerrymander(graph, districts, target_population_range, max_republican_districts, 'republican')
gerrymandered_districts_democrat = gerrymander(graph, districts, target_population_range, max_democrat_districts, 'democrat')



def calculate_new_proportions(district, graph):
    total_democrat_votes = 0
    total_republican_votes = 0
    total_other_votes = 0
    total_population = 0

    for county in district:
        county_data = graph.nodes[county]
        total_democrat_votes += county_data['population'] * county_data['democrat']
        total_republican_votes += county_data['population'] * county_data['republican']
        total_other_votes += county_data['population'] * county_data['other']
        total_population += county_data['population']

    if total_population != 0:
        new_democrat = total_democrat_votes / total_population
        new_republican = total_republican_votes / total_population
        new_other = total_other_votes / total_population
    else:
        new_democrat = 0
        new_republican = 0
        new_other = 0

    return new_democrat, new_republican, new_other, total_population



# First, we need to extract the districts from the gerrymandered_districts dictionary
districts_counties_republican = [gerrymandered_districts_republican[i] for i in range(1, 12)]
districts_counties_democrat = [gerrymandered_districts_democrat[i] for i in range(1, 12)]

total_population_sum = 0

for i, district in enumerate(districts_counties_republican, start=1):
    new_democrat, new_republican, new_other, total_population = calculate_new_proportions(district, graph)
    print(f"District {i}:")
    print(f"  Counties: {', '.join(district)}")
    print(f"  Democrat proportion: {new_democrat:.2%}")
    print(f"  Republican proportion: {new_republican:.2%}")
    print(f"  Other proportion: {new_other:.2%}")
    print(f"  Total population: {total_population}")
    print()

    total_population_sum += total_population

print(f"Sum of total populations of all gerrymandered districts: {total_population_sum}")

for i, district in enumerate(districts_counties_democrat, start=1):
    new_democrat, new_republican, new_other, total_population = calculate_new_proportions(district, graph)
    print(f"District {i}:")
    print(f"  Counties: {', '.join(district)}")
    print(f"  Democrat proportion: {new_democrat:.2%}")
    print(f"  Republican proportion: {new_republican:.2%}")
    print(f"  Other proportion: {new_other:.2%}")
    print(f"  Total population: {total_population}")
    print()

    total_population_sum += total_population

print(f"Sum of total populations of all gerrymandered districts: {total_population_sum}")




