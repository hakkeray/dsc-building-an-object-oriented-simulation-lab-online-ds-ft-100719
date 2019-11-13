
"""
r0, the average number of people a contagious person infects before
they are no longer contagious (because they got better or they died)
mortality_rate, the percentage chance a person infected with a disease will die from it.
The main workflow of this simulation is as follows:


Create a Simulation class with the following attributes:

population
virus_name
num_time_steps
r0
percent_pop_vaccinated
Create methods for our Simulation class that will cover each step of the simulation.

In order for our simulation to work, you'll need to define some rules for it:

Each infected person will "interact" with 100 random people from the population. If the person the infected individual interacts with is sick, vaccinated, or has had the disease before, nothing happens. However, if the person the infected individual interacts with is healthy, unvaccinated, and has not been infected yet, then that person becomes infected.

At the end of each round, the following things happen:

All currently infected people either get better from the disease or die, with the chance of death corresponding to the mortality rate of the disease.
All people that were newly infected during this round become the new infected for the next round.
The simulation continues for the set number of time steps. Any time someone dies or gets infected, log it in a text file called simulation_logs.txt. Once the simulation is over, write some code to quickly parse the text logs into data and quickly visualize the results, so that you can run multiple simulations and answer questions like:

If vaccination rates for {disease x} dropped by 5%, how many more people become infected in an epidemic? How many more die?
What does the spread of {disease x} through a population look like?
If this all seems a bit daunting, don't worry! You'll be provided with much more detail as you build this step-by-step during the lab.

With that, go ahead and take a look at this cool simulation lab!
"""


# import numpy as np
# import pandas as pd
# from tqdm.autonotebook import tqdm
# np.random.seed(0)

class Person(object):

    def __init__(self):
        self.is_alive = True
        self.is_infected = False
        self.has_been_infected = False
        self.newly_infected = False
        self.is_vaccinated =  False

    def get_vaccinated(self, pct_vaccinated):
        if np.random.random() > (1 - pct_vaccinated):
            self.is_vaccinated = True


class Simulation(object):

    def __init__(self, population_size, disease_name, r0, mortality_rate,  total_time_steps, pct_vaccinated, num_initial_infected):
        self.r0 = r0 / 100
        self.disease_name = disease_name
        self.mortality_rate = mortality_rate
        self.total_time_steps = total_time_steps
        self.current_time_step = 0
        self.total_infected_counter = 0
        self.current_infected_counter = 0
        self.dead_counter = 0
        self.population = []
        # This attribute is used in a function that is provided for you in order to log statistics from each time_step.
        # Don't touch it!
        self.time_step_statistics_df = pd.DataFrame()

        # Create a for loop the size of the population
        for i in range(population_size):
            # Create new person
            new_person = Person()
            # We'll add infected persons to our simulation first.
            # Check if the current number of infected are equal to the
            # num_initial_infected parameter.
            # If not, set new_person to be infected
            if self.current_infected_counter != num_initial_infected:
                new_person.is_infected = True
                # don't forget to increment both infected counters!
                self.total_infected_counter += 1
                self.current_infected_counter += 1
            # if new_person is not infected, determine if they are vaccinated or not by using their `get_vaccinated` method
            # Then, append new_person to self.population
            else:
                new_person.get_vaccinated(pct_vaccinated)
            self.population.append(new_person)

        print("-" * 50)
        print("Simulation Initiated!")
        print("-" * 50)
        self._get_sim_statistics()



    def _get_sim_statistics(self):
    # In the interest of time, this method has been provided for you.  No extra code needed.
        num_infected = 0
        num_dead = 0
        num_vaccinated = 0
        num_immune = 0
        for i in self.population:
            if i.is_infected:
                num_infected += 1
            if not i.is_alive:
                num_dead += 1
            if i.is_vaccinated:
                num_vaccinated += 1
                num_immune += 1
            if i.has_been_infected:
                num_immune += 1
        assert num_infected == self.current_infected_counter
        assert num_dead == self.dead_counter


        print("")
        print("Summary Statistics for Time Step {}".format(self.current_time_step))
        print("")
        print("-" * 50)
        print("Disease Name: {}".format(self.disease_name))
        print("R0: {}".format(self.r0 * 100))
        print("Mortality Rate: {}%".format(self.mortality_rate * 100))
        print("Total Population Size: {}".format(len(self.population)))
        print("Total Number of Vaccinated People: {}".format(num_vaccinated))
        print("Total Number of Immune: {}".format(num_immune))
        print("Current Infected: {}".format(num_infected))
        print("Deaths So Far: {}".format(num_dead))



def infected_interaction(self, infected_person):
    num_interactions = 0
    while num_interactions < 100:
        # Randomly select a person from self.population
        random_person = np.random.choice(self.population)
        # This only counts as an interaction if the random person selected is alive.  If the person is dead, do nothing,
        # and the counter doesn't increment, repeating the loop and selecting a new person at random.
        # check if the person is alive.
        if random_person.is_alive:
            # CASE: Random person is not vaccinated, and has not been infected before, making them vulnerable to infection
            if random_person.is_vaccinated == False and random_person.has_been_infected == False:
                # Generate a random number between 0 and 1
                random_number = np.random.random()
                # If random_number is greater than or equal to (1 - self.r0), set random person as newly_infected
                if random_number >= (1 - self.r0):
                    random_person.newly_infected = True
            # Don't forget to increment num_interactions, and make sure it's at this level of indentation
            num_interactions += 1

# Adds this function to our Simulation class
Simulation.infected_interaction = infected_interaction



def _resolve_states(self):
    """
    Every person in the simulation falls into 1 of 4 states at any given time:
    1. Dead
    2. Alive and not infected
    3. Currently infected
    4. Newly Infected

    States 1 and 2 need no resolving, but State 3 will resolve by either dying or surviving the disease, and State 4 will resolve
    by turning from newly infected to currently infected.

    This method will be called at the end of each time step.  All states must be resolved before the next time step can begin.
    """
    # Iterate through each person in the population
    for person in self.population:
        # We only need to worry about the people that are still alive
        if person.is_alive:
            # CASE: Person was infected this round.  We need to stochastically determine if they die or recover from the disease
            # Check if person is_infected
            if person.is_infected:
                # Generate a random number
                random_number = np.random.random()
                # If random_number is >= (1 - self.mortality_rate), set the person to dead and increment the simulation's death
                # counter
                if random_number >= (1 - self.mortality_rate):
                    # Set is_alive and in_infected both to False
                    person.is_alive = False
                    person.is_infected = False
                    # Don't forget to increment self.dead_counter, and decrement self.current_infected_counter
                    self.dead_counter += 1
                    self.current_infected_counter -= 1
                else:
                    # CASE: They survive the disease and recover.  Set is_infected to False and has_been_infected to True
                    person.is_infected = False
                    person.has_been_infected = True
                    # Don't forget to decrement self.current_infected_counter!
                    self.current_infected_counter -= 1
            # CASE: Person was newly infected during this round, and needs to be set to infected before the start of next round
            elif person.newly_infected:
                # Set is_infected to True, newly_infected to False, and increment both self.current_infected_counter and
                # self.total_infected_counter
                person.is_infected = True
                person.newly_infected = False
                self.current_infected_counter += 1
                self.total_infected_counter += 1

Simulation._resolve_states = _resolve_states





def _time_step(self):
    """
    Compute 1 time step of the simulation. This function will make use of the helper methods we've created above.

    The steps for a given time step are:
    1.  Iterate through each person in self.population.
        - For each infected person, call infected_interaction() and pass in that person.
    2.  Use _resolve_states() to resolve all states for the newly infected and the currently infected.
    3. Increment self.current_time_step by 1.
    """
    # Iterate through each person in the population
    for person in self.population:
        # Check only for people that are alive and infected
        if person.is_alive and person.is_infected:
            # Call self.infected_interaction() and pass in this infected person
            self.infected_interaction(person)

    # Once we've made it through the entire population, call self._resolve_states()
    self._resolve_states()

    # Now, we're almost done with this time step.  Log summary statistics, and then increment self.current_time_step by 1.
    self._log_time_step_statistics()
    self.current_time_step += 1

# Adds this function to our Simulation class
Simulation._time_step = _time_step





def _log_time_step_statistics(self, write_to_file=False):
    # This function has been provided for you, you do not need to write any code for it.
    # Gets the current number of dead,
    # CASE: Round 0 of simulation, need to create and Structure DataFrame
#     if self.time_step_statistics_df == None:
#         import pandas as pd
#         self.time_step_statistics_df = pd.DataFrame()
# #         col_names = ['Time Step', 'Currently Infected', "Total Infected So Far" "Alive", "Dead"]
# #         self.time_step_statistics_df.columns = col_names
#     # CASE: Any other round
#     else:
        # Compute summary statistics for currently infected, alive, and dead, and append them to time_step_snapshots_df
    row = {
        "Time Step": self.current_time_step,
        "Currently Infected": self.current_infected_counter,
        "Total Infected So Far": self.total_infected_counter,
        "Alive": len(self.population) - self.dead_counter,
        "Dead": self.dead_counter
    }
    self.time_step_statistics_df = self.time_step_statistics_df.append(row, ignore_index=True)

    if write_to_file:
        self.time_step_statistics_df.to_csv("simulation.csv", mode='w+')

Simulation._log_time_step_statistics = _log_time_step_statistics





def run(self):
    """
    The main function of the simulation.  This will run the simulation starting at time step 0, calculating
    and logging the results of each time step until the final time_step is reached.
    """

    for _ in tqdm(range(self.total_time_steps)):
        # Print out the current time step
        print("Beginning Time Step {}".format(self.current_time_step))
        # Call our `_time_step()` function
        self._time_step()

    # Simulation is over--log results to a file by calling _log_time_step_statistics(write_to_file=True)
    self._log_time_step_statistics(write_to_file=True)

# Adds the run() function to our Simulation class.
Simulation.run = run


# sim = Simulation(2000, 'Ebola', 2, 0.5, 20, .85, 50)
# sim.run()

# results = pd.read_csv('simulation.csv')
# results
