from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class GameplayTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_h1(self, text):
        self.assertIn(text, self.browser.find_element_by_tag_name('h1').text)
    
    def get_input_element(self):
        return self.browser.find_element_by_id('answer_box')

    def send_answer(self, text):
        self.get_input_element().send_keys(text)
        self.get_input_element().send_keys(Keys.ENTER)

    def test_winning_the_game(self):
        # want to play the game
        # open the browser and go on the game website
        self.browser.get('http://localhost:8080/')

        # start page opens
        # "Central Corridor" room
        # read the text
        self.assertIn('Gothons From Planet Percal #25', self.browser.title)
        self.check_h1('Central Corridor')

        # type the right phrase 'tell a joke' and hit enter
        self.send_answer('tell a joke')

        # see the "Laser Weapon Armory" room page
        # read the text
        # type the right phrase '0132' and hit enter
        self.check_h1('Laser Weapon Armory')
        self.send_answer('0132')

        # see "The Bridge" room page
        # read the text
        # type the right phrase 'slowly place the bomb'
        self.check_h1('The Bridge')
        self.send_answer('slowly place the bomb')

        # see "Escape Pod" room page
        # read the text
        # type the right phrase '2'
        self.check_h1('Escape Pod')
        self.send_answer('2')

        # see "The End" room page
        # text says "You won!"
        self.check_h1('The End')
        winning_text = self.browser.find_element_by_id('room_description').text
        self.assertIn("You won!", winning_text)

        # you see "Play again"
        # click!
        

        # you see the game

if __name__ == '__main__':
    unittest.main()
