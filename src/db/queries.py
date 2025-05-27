class PromptQueries:
    @property
    def get_prompt(self):
        return "SELECT prompt FROM neuron_prompt WHERE prompt_modul=$1"
