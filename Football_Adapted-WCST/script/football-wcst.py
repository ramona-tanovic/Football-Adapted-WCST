# Import necessary libraries from PsychoPy
from psychopy import visual, event, core, gui, data
import csv  # To save experiment results to a CSV file
import random  # Import random for shuffling positions
import os  # For handling file paths
import time  # To measure reaction times

# Define the main experiment class
class FootballWCSTExperiment:
    def __init__(self):
        # Set up the base directory (where this script is located)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # Define the directory for saving results
        self.results_dir = os.path.join(self.base_dir, "results")
        # Define the directory where scenarios are stored
        self.scenarios_dir = os.path.join(self.base_dir, "scenarios")

        # Ensure the results directory exists (create it if not)
        os.makedirs(self.results_dir, exist_ok=True)

        # Define experiment rules (order is fixed and repeats)
        self.rules = ['selfish', 'team-player', 'hold the possession']
        # Define available roles for participants
        self.roles = ['Attacker', 'Midfielder', 'Defender']
        # Number of trials and scenarios per trial
        self.num_trials = 9  # Total of 9 trials
        self.scenarios_per_trial = 10  # Each trial has 10 scenarios

        # Set up participant information dialog box
        self.setup_experiment_info()

    def setup_experiment_info(self):
        """
        This function sets up a dialog box to collect participant details 
        and provides consent information.
        """
        # Experiment name (constant, not editable by participants)
        expName = 'Football-Adapted WCST'
        # Participant details to be filled in the dialog box
        self.expInfo = {
            'participant': '',  # Participant ID (typed in)
            'timestamp': data.getDateStr(),  # Automatically gets date and time
            'expName': expName,  # Constant experiment name
            'age': '',  # Dropdown for age selection
            'gender': '',  # Dropdown for gender selection
            'years of playing football': ''  # Dropdown for football experience
        }

        # Options for dropdown fields
        age_options = [str(x) for x in range(10, 31)]  # Ages 10 to 30
        gender_options = ['Male', 'Female', 'Other']  # Gender options
        football_years_options = [str(x) for x in range(1, 31)]  # 1 to 30 years

        # Create a custom dialog box for participant details
        dlg = gui.Dlg(title="Participant Details and Consent")
        dlg.addField("Participant ID (remember this):", "")
        dlg.addField("Age:", choices=age_options)
        dlg.addField("Gender:", choices=gender_options)
        dlg.addField("Years of playing football:", choices=football_years_options)
        dlg.addText(
            "\nCONSENT INFORMATION:\n"
            "By confirming this dialog box, you consent to participate in this experiment. "
            "All your data will remain anonymous and will only be used for research purposes.\n\n"
            "You must remember your Participant ID if you wish to retrieve or delete your data later."
        )

        # Show dialog and get user input
        participant_data = dlg.show()
        if dlg.OK:
            self.expInfo['participant'] = participant_data[0]
            self.expInfo['age'] = participant_data[1]
            self.expInfo['gender'] = participant_data[2]
            self.expInfo['years of playing football'] = participant_data[3]
        else:
            # If the dialog is canceled, exit the program
            core.quit()

    def load_scenarios(self, role):
        """
        Load scenario images for the selected role and for macro scenarios.
        """
        # Define role-specific and macro directories
        role_dir = os.path.join(self.scenarios_dir, role.lower())  # Role-specific
        macro_dir = os.path.join(self.scenarios_dir, 'macro')  # Macro folder

        # Helper function to fetch scenario images based on the correct naming convention
        def get_scenario_images(base_dir, scenario_folder):
            """
            Given the base directory and scenario folder (e.g., 'a1', 'a2', etc.),
            returns the full paths to the images with suffixes '_s', '_t', '_h', and 'main'.
            """
            # Construct the base path to the scenario folder
            scenario_path = os.path.join(base_dir, scenario_folder)
    
            # Check if the scenario folder exists (optional, for debugging)
            if not os.path.exists(scenario_path):
                print(f"Error: The folder {scenario_path} does not exist.")
    
            # Return dictionary of image paths (handling all suffixes for the given scenario)
            return {
                'main': os.path.join(scenario_path, f"{scenario_folder}.png"),  # e.g., a1.png
                'selfish': os.path.join(scenario_path, f"{scenario_folder}_s.png"),  # e.g., a1_s.png
                'team': os.path.join(scenario_path, f"{scenario_folder}_t.png"),  # e.g., a1_t.png
                'hold': os.path.join(scenario_path, f"{scenario_folder}_h.png"),  # e.g., a1_h.png
            }

        # Create a list of all scenarios for the experiment
        scenarios = []
        for trial_num in range(self.num_trials):  # Loop through trials
            trial_scenarios = []
            for scenario_idx in range(self.scenarios_per_trial):  # 10 scenarios per trial
                if scenario_idx < 5:  # First 5 from the role-specific folder
                    scenario_folder = f"{role[0].lower()}{scenario_idx+1}"  # E.g., a1, a2, ...
                    trial_scenarios.append(get_scenario_images(role_dir, scenario_folder))
                else:  # Next 5 from the macro folder
                    scenario_folder = f"m{scenario_idx-4}"  # E.g., m1, m2, ...
                    trial_scenarios.append(get_scenario_images(macro_dir, scenario_folder))
            scenarios.append(trial_scenarios)
        return scenarios

    def create_rule_sequence(self):
        """
        Creates a sequence where the rules 'selfish', 'team-player', 'hold the possession' repeat
        in the order 10 times each, and the pattern is repeated 3 times.
        """
        rule_sequence = []
        pattern = ['selfish', 'team-player', 'hold the possession']
        
        for _ in range(3):  # Repeat the pattern 3 times
            for rule in pattern:
                rule_sequence.extend([rule] * 10)  # Repeat each rule 10 times
        
        return rule_sequence



    def run_experiment(self):
        """
        Main experiment loop, including role selection, instructions, 
        scenario presentation, and response recording.
        """
        # Create a fullscreen window for the experiment
        win = visual.Window(size=(1920, 1080), color=(0, 0, 0), fullscr=True, units='pix')

        # Instructions screen
        instructions = visual.TextStim(win, name='instructions',
            text="Overview:\n"
            "In this task, you will see a card on the screen and several options to choose from. Your goal is to figure out the correct option based on an unseen rule.\n\n"
            "How to Play:\n"
            "Look at the scenario displayed on the screen. Choose the option that matches the rule you think is being used. After making your choice, you will receive feedback to let you know if you were correct or incorrect.\n\n"
            "Figuring Out the Rule:\n"
            "The rule might be based on SELFISH PLAY, TEAM-PLAYER PLAY, or HOLD THE POSSESION. The rule can change during the task. Pay attention to feedback to adapt to new rules.\n\n"
            "Stay Focused:\n"
            "If you notice your answers are wrong repeatedly, try changing your approach. Don’t stick to an old rule—use the feedback to adjust.\n\n"
            "Timing:\n"
            "Take your time to think about your choice, but don't overthink it. There’s no penalty for mistakes—this is about learning and adapting.\n\n"
            "Enjoy the Process:\n"
            "There are no right or wrong ways to figure things out—just do your best. The task is designed to be challenging, so don’t worry if it feels tricky.\n\n"
            "Press 'space' to continue! :)",
            color=(-1, -1, -1), height=30, wrapWidth=1200
        )
        instructions.draw()  # Draw instructions on the screen
        win.flip()  # Update the screen to show instructions
        event.waitKeys(keyList=['space'])  # Wait for space key to continue

        # Role Selection
        role_selection_text = visual.TextStim(win, text="Choose your role by clicking one button:",
                                              color=(-1, -1, -1), height=40, pos=(0, 200))
        role_buttons = [visual.Rect(win, width=300, height=100, pos=(-400 + i * 400, 0),
                                     fillColor=(-0.5, -0.5, -0.5)) for i in range(3)]
        role_labels = [visual.TextStim(win, text=role, color=(1, 1, 1), pos=button.pos)
                       for button, role in zip(role_buttons, self.roles)]

        # Mouse interaction for role selection
        mouse = event.Mouse(win=win)
        selected_role = None
        while selected_role is None:
            role_selection_text.draw()
            for button, label in zip(role_buttons, role_labels):
                button.draw()
                label.draw()
            win.flip()
            if mouse.getPressed()[0]:
                for button, role in zip(role_buttons, self.roles):
                    if button.contains(mouse):
                        selected_role = role
                        break
            if 'escape' in event.getKeys():
                core.quit()

        # Load scenarios for the selected role
        scenarios = self.load_scenarios(selected_role)

        # Prepare CSV file with naming convention: expName_participant_timestamp
        result_file_path = os.path.join(self.results_dir, f"{self.expInfo['expName']}_{self.expInfo['participant']}_{self.expInfo['timestamp']}.csv")
        with open(result_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'Participant','Age','Gender','Experience [years]',
                'Role', 'Trial', 'Scenario', 'Correct_Rule', 
                'Selected_Rule', 'Reaction_Time', 'Correct', 
                'Perseverative_Error', 'Non_Perseverative_Error', 'Scenario_Shown',
                'Scenario_Persevering_Click', 'Feedback'
            ])
            writer.writeheader()

            # Experiment loop
            rule_sequence = self.create_rule_sequence()  # Create sequence where each rule repeats 10 times
            
            previous_rule = None
            for trial_num in range(self.num_trials):
                for scenario_num, scenario in enumerate(scenarios[trial_num]):
                    # Determine the rule for this trial based on the sequence
                    correct_rule = rule_sequence[trial_num * self.scenarios_per_trial + scenario_num]

                    # Display scenario and options
                    main_image = visual.ImageStim(win, image=scenario['main'], pos=(0, 200), size=(800, 400))
                    option_images = {
                        'selfish': visual.ImageStim(win, image=scenario['selfish'], pos=(-400, -200), size=(300, 200)),
                        'team-player': visual.ImageStim(win, image=scenario['team'], pos=(0, -200), size=(300, 200)),
                        'hold': visual.ImageStim(win, image=scenario['hold'], pos=(400, -200), size=(300, 200))
                    }
                    
                    # Randomize the positions of the response images
                    options = list(option_images.items())  # Create a list of (rule, image) tuples
                    random.shuffle(options)  # Shuffle the list randomly

                    # Update the positions of the option images after shuffling
                    for i, (rule, img) in enumerate(options):
                        img.pos = (-400 + i * 400, -200)  # Reassign positions based on shuffled order

                    # Draw and show the images
                    main_image.draw()
                    for img in option_images.values():
                        img.draw()
                    win.flip()

                    # Record response
                    mouse.clickReset()
                    selected_option = None
                    start_time = time.time()
                    while selected_option is None:
                        if mouse.getPressed()[0]:
                            for rule, img in option_images.items():
                                if img.contains(mouse):
                                    selected_option = rule
                                    break
                        if 'escape' in event.getKeys():
                            core.quit()
                    reaction_time = time.time() - start_time
                    
                    is_correct = selected_option == correct_rule

                    feedback_message = "Correct!" if is_correct else "Wrong."
                    feedback_color = (0, 1, 0) if is_correct else (1, 0, 0)

                    feedback = visual.TextStim(win, text=feedback_message, color=feedback_color, height=50)
                    feedback.draw()
                    win.flip()
                    core.wait(1)  # Show feedback for 1 second

                    # Categorize response
                    is_correct = selected_option == correct_rule
                    perseverative_error = False
                    non_perseverative_error = False
                    if not is_correct:
                        if selected_option == previous_rule:
                            perseverative_error = True
                        else:
                            non_perseverative_error = True

                    # Record data
                    writer.writerow({
                        'Participant': self.expInfo['participant'],
                        'Age': self.expInfo['age'],
                        'Gender': self.expInfo['gender'],
                        'Experience [years]': self.expInfo['years of playing football'],
                        'Role': selected_role,
                        'Trial': trial_num + 1,
                        'Scenario': f"Trial-{trial_num+1}_Scenario-{scenario_num+1}",
                        'Correct_Rule': correct_rule,
                        'Selected_Rule': selected_option,
                        'Reaction_Time': reaction_time,
                        'Correct': int(is_correct),
                        'Perseverative_Error': int(perseverative_error),
                        'Non_Perseverative_Error': int(non_perseverative_error),
                        'Scenario_Shown': scenario['main'],  # Which scenario was shown
                        'Scenario_Persevering_Click': previous_rule,  # Previous rule selected
                        'Feedback': feedback_message
                    })
                    previous_rule = correct_rule
                    core.wait(0.5)

        # Close experiment
        win.close()
        core.quit()


# Run the experiment
if __name__ == "__main__":
    experiment = FootballWCSTExperiment()
    experiment.run_experiment()
