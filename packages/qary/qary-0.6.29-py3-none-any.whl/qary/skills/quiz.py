""" Rule-based chatbot (FSM) for administering adaptive quizzes """
import logging
import os

from qary.constants import DATA_DIR
from qary.skills.base import ContextBot
from qary.etl.utils import squash_wikititle as normalize_text
from qary.etl.dialog import TurnsPreparation, compose_statement, load_dialog_turns

# FIXME: make this a config option and dont default to a test file
DEFAULT_QUIZ = os.path.join(DATA_DIR, 'testsets/dialog_parser.input.v3.dialog.yml')
DIALOG_TREE_END_STATE_NAMES = (None, False, 0, '', ''.encode(), '0', 'none', 'None')
DIALOG_TREE_END_BOT_STATEMENTS = (None, 'none', )

WELCOME_STATE_NAME = '__WELCOME__'
FINISH_STATE_NAME = '__FINISH__'
DEFAULT_STATE_NAME = '__default__'
DEFAULT_BOT_USERNAME = 'bot'
EXIT_STATE_NAME = None
EXIT_BOT_STATEMENTS = ['Session is already over! Type "quit" to exit or press "Enter" for a new session']
EXIT_STATE_TURN_DICT = {'state': EXIT_STATE_NAME, DEFAULT_BOT_USERNAME: EXIT_BOT_STATEMENTS}


log = logging.getLogger(__name__)


class Skill(ContextBot):
    r"""Skill for Quiz"""

    def __init__(self, datafile=DEFAULT_QUIZ, turns_list=None, use_nlp=False):
        """ If datafile is not given, the turns list of dicts can directly be passed to seed the data
        """
        super().__init__()
        self.datafile = datafile
        self.turns = {}
        self.use_nlp = use_nlp
        # if turns is passed, then you should not set the datafile
        if turns_list:
            self.turns_input = turns_list
        else:
            self.turns_input = load_dialog_turns(datafile)
        if self.turns_input:
            # Do more complex operations using the helper '_TurnsPreparation' class
            turns_preparation = TurnsPreparation(turns_list=self.turns_input, use_nlp=self.use_nlp)
            self.turns = turns_preparation.prepare_turns()
        else:  # some sort of error
            log.error('An empty turns_list and/or datafile was passed to quiz.Skill.__init__()')
        self.state = ''  # State names must be strings
        self.current_turn = {}  # None or empty dict used to indicate start of quiz that bot says something first?
        return

    def get_nxt_cndn_match_mthd_dict(self, nxt_cndn):
        """Creates a dict with the match_method keyword being the key and a list of next_states which use
        that keyword as a value. This is needed because there is a priority in which the match_method
        keywords are handled

        Args:
            nxt_cndn (dict): dict with the intent being the key and the value being another dict
                with a key value pair for the next state and the 'match_method' for that intent

        Returns:
            object: A dictionary which looks like :
                    { match_method1: [intent1: next_state1], } where the list is a list of all the
                    next_conditions that use that match method

        """
        nxt_cndn_match_mthd_dict = {
            'EXACT': [],
            'LOWER': [],
            'CASE_SENSITIVE_KEYWORD': [],
            'KEYWORD': [],
            'NORMALIZE': [],
            None: [],
        }
        for intent, nxt_state_dict in nxt_cndn.items():
            match_method = nxt_state_dict['match_method']
            next_state = nxt_state_dict['next_state']
            nxt_cndn_match_mthd_dict[match_method].append((intent, next_state))
        return nxt_cndn_match_mthd_dict

    def check_for_match(self, statement, next_state_option, match_condition):
        intent = next_state_option[0]
        match_found = False
        if match_condition == 'EXACT':
            if statement == intent:
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'LOWER':
            if statement.lower() == intent.lower():
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'CASE_SENSITIVE_KEYWORD':
            if intent in statement:
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'KEYWORD':
            if intent.lower() in statement.lower():
                self.state = next_state_option[1]
                match_found = True
        elif match_condition == 'NORMALIZE':
            if normalize_text(statement) == normalize_text(intent):
                self.state = next_state_option[1]
                match_found = True
        return match_found

    def reply(self, statement, context=None):
        r"""Except for the welcome state, all other states are mere recordings of the quiz responses
        """
        responses = super().reply(statement, context=context)
        if statement in DIALOG_TREE_END_BOT_STATEMENTS:
            statement = None

        # First check to see if we are in the time before the welcome state
        if self.state in DIALOG_TREE_END_STATE_NAMES:
            # First figure out the welcome state name using a magical special WELCOME_STATE_NAME string
            # as the key. This will allow you to access the actual welcome turn
            self.state = self.turns[WELCOME_STATE_NAME]
            self.current_turn = self.turns[self.state]
            response_text = compose_statement(self.current_turn['bot'])
        else:
            nxt_cndn = self.current_turn['next_condition']
            context
            nxt_cndn_match_mthd_dict = self.get_nxt_cndn_match_mthd_dict(nxt_cndn)
            # for match_method_keyword in ['EXACT', '']
            match_found = False
            for next_state_option in nxt_cndn_match_mthd_dict['EXACT']:
                match_found = self.check_for_match(statement, next_state_option, 'EXACT')
                if match_found:
                    break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['LOWER']:
                    match_found = self.check_for_match(statement, next_state_option, 'LOWER')
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['CASE_SENSITIVE_KEYWORD']:
                    match_found = self.check_for_match(
                        statement, next_state_option, 'CASE_SENSITIVE_KEYWORD'
                    )
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['KEYWORD']:
                    match_found = self.check_for_match(statement, next_state_option, 'KEYWORD')
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['NORMALIZE']:
                    match_found = self.check_for_match(statement, next_state_option, 'NORMALIZE')
                    if match_found:
                        break
            if not match_found:
                self.state = nxt_cndn_match_mthd_dict[None][0][1]
            self.current_turn = self.turns.get(self.state, EXIT_STATE_TURN_DICT)
            response_text = compose_statement(self.current_turn.get(DEFAULT_BOT_USERNAME, EXIT_BOT_STATEMENTS))

        return responses + [(1.0, response_text)]
