from Utility import reward_type_to_str
from os.path import join
from json import load

class GetNGramLevels:
    def __init__(self, config, agents):
        self.config = config
        self.agents = agents

    def run(self):
        REWARD_StR = reward_type_to_str(self.config.REWARD_TYPE)

        for a in self.agents:
            NAME = a().NAME
            print(NAME)
            f_name = f'player_agent_game_{self.config.NAME}_director_{NAME}_reward_{REWARD_StR}.json'
            with open(join(self.config.BASE_DIR, f_name), 'r') as f:
                data = load(f)

            play_through = data['data'][0]
            print('Start')
            self.__print_level(play_through[0]['Playthrough'])

            print('\n\nEnd')
            self.__print_level(play_through[-1]['Playthrough'])

            print('\n\n==================================\n\n')

    def __print_level(self, playthrough):
        lvl = list(eval(playthrough[0]['node_name']))
        for i in range(1, len(playthrough)):
            lvl.append(list(eval(playthrough[i]['node_name']))[1])

        print(self.config.level_to_str(lvl))