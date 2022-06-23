#Import modules
from bs4 import BeautifulSoup
from urllib.request import urlopen
import math
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#Lottery ticket expectation value calculator
class lottery_expectation_calculator:

    def __init__(self):
        self.current_jackpot = None
        self.rollovers = None
        self.expectation_value = None

    #Method which uses BeautifulSoup to scrape national-lottery webpage and find current jackpot
    def get_current_jackpot(self):
        url = "https://www.national-lottery.co.uk/games/lotto?icid=-:mm:-:mdg:lo:dbg:pl:co"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        metas = soup.find_all('meta')
        for meta in metas:
            if 'name="lotto-next-draw-jackpot"' in str(meta):
                jackpot = ((meta['content']).replace(',',''))
                jackpot = int(jackpot.replace('£',''))
                self.current_jackpot = jackpot

    #Method which uses BeautifulSoup to scrape national-lottery webpage and find current number of rollovers
    def get_num_rollovers(self):
        url = "https://www.national-lottery.co.uk/games/lotto?icid=-:mm:-:mdg:lo:dbg:pl:co"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        metas = soup.find_all('meta')
        for meta in metas:
            if 'name="lotto-roll-count"' in str(meta):
                self.rollovers = int(meta['content'])

    #Method to calculate probability of getting num_correct correct numbers in a draw of 6 numbered balls from 59
    def result_probability(self, num_correct):
        return ((math.comb(6,num_correct))*(math.comb(53,(6 - num_correct))))/(math.comb(59,6))

    def get_expectation_value(self):
        #get current jackpot and number of rollovers
        self.get_current_jackpot()
        self.get_num_rollovers()

        #Linear Regression model to predict ticket sales given current jackpot, used if self.rollovers == 5
        lottery_sales_data = pd.read_csv('Lottery_sales_2021.csv')
        lottery_sales_data['log_sales'] = np.log10(lottery_sales_data['Sales'])
        lottery_sales_data['log_jackpot'] = np.log10(lottery_sales_data['Jackpot'])
        #Prepare training data
        y = np.array(lottery_sales_data['log_sales'].copy()).reshape(-1, 1)
        X = np.array(lottery_sales_data['log_jackpot'].copy()).reshape(-1, 1)
        #Instantiate linear regression model
        regression_model = LinearRegression()
        #Train model
        regression_model.fit(X, y)

        #Calculate probabilities of getting n correct numbers
        p_0 = self.result_probability(0)
        p_1 = self.result_probability(1)
        p_2 = self.result_probability(2)
        p_3 = self.result_probability(3)
        p_4 = self.result_probability(4)
        p_5_nobb = ((math.comb(6,5))*(math.comb(52,1)))/(math.comb(59,6))
        p_5_bb = ((math.comb(6,5))*(math.comb(52,0)))/(math.comb(59,6))
        p_6 = self.result_probability(6)

        #If not a rolldown
        if self.rollovers != 5:
            w_0 = 0
            w_1 = 0
            w_2 = 2
            w_3 = 30
            w_4 = 140
            w_5_nobb = 1750
            w_5_bb = 1000000
            w_6 = self.current_jackpot

        #In the event of a rolldown
        else:
            #Predict sales from current jackpot using the linear regression model
            current_jackpot = np.log10(self.current_jackpot).reshape(-1, 1)
            predicted_sales = int(10**(regression_model.predict(current_jackpot)))
            current_jackpot = int(10**(current_jackpot))

            #Prizes calculated as per https://www.lottery.co.uk/lotto/must-be-won-draws
            w_0 = 0
            w_1 = 0
            w_2 = 7
            money_paid_to_2 = predicted_sales * p_2 * 5
            w_3 = (((current_jackpot - money_paid_to_2)*0.85)/(predicted_sales * p_3)) + 30
            w_4 = (((current_jackpot - money_paid_to_2)*0.07)/(predicted_sales * p_4)) + 140
            w_5_nobb = (((current_jackpot - money_paid_to_2)*0.05)/(predicted_sales * p_5_nobb)) + 1750
            w_5_bb = (((current_jackpot - money_paid_to_2)*0.03)/(predicted_sales * p_5_bb)) + 1000000
            w_6 = get_current_jackpot()

        #Calculate expectation value
        self.expectation_value = (p_0 * w_0) + (p_1 * w_1) + (p_2 * w_2) + (p_3 * w_3) + (p_4 * w_4) + (p_5_nobb * w_5_nobb) + (p_5_bb * w_5_bb) + (p_6 * w_6)
        print(f'The expectation value of the UK lottery is currently: £{self.expectation_value}')

lottery_exp_calc = lottery_expectation_calculator()
lottery_exp_calc.get_expectation_value()
