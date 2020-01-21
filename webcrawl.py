import requests
import bs4
from selenium import webdriver
import time
import pickle

### scroll to bottom of page for how to search for players

class Op_search():
	def __init__(self,userName,Season):
		self.base_url= 'https://na.op.gg/summoner/userName='
		self.username = userName
		self.season = Season
		self.info = self.opSearch(self.username,self.season)
		
		
	
	def __str__(self):
		return str(self.info)
		
	def save(self):
		count_username=0
		for u in self.username:
			count_season=0
			for s in self.season:
				f = open('Saved-pickles/'+u+' '+s+".pkl","wb")
				print(self.info)
				pickle.dump(self.info[count_username].get(u)[count_season],f)
				count_season+=1
				f.close()
				objects = []
				#Save a pickle file for later 
				with (open('Saved-pickles/'+u+' '+s+".pkl", "rb")) as openfile:
					while True:
						try:
							objects.append(pickle.load(openfile))
						except EOFError:
							break
				#Save a easy to read formate as txt file
				with open('Saved-lookups/'+u+' '+s+'.txt', 'w') as writer:
					writer.write(u+'\n'+' \n')
					for i in objects[0]:
						writer.write(i.get('Name')+' ')
						writer.write(i.get('Win rate'+'winRate')+' ')
						writer.write('Games played: '+str(i.get('gamesWon')+i.get('gamesLost'))+' ')
						writer.write(' \n'+' \n')
			count_username+=1
		
	def opSearch(self,username,season):
		#starts loop with first username then first season then keeps appending info to master list data format returned list[dictionary:list]
		master_list=[]
		driver = webdriver.Chrome()
		for u in self.username:
			url =self.base_url+u
			driver.get(url)
			temp=[]
			for s in self.season:
				#loading page
				driver.find_element_by_id('left_champion').click()
				time.sleep(2)
				driver.find_element_by_class_name(s).click()
				time.sleep(2)
				html = driver.page_source
				soup = bs4.BeautifulSoup(html, 'lxml')
				champion_html = soup.select('div.'+s)[0].find('tbody',{'class':'Body'}).find_all('tr',{'class':'Row'})
				# print(champion_html)
				temp.append(self.gather(champion_html))
			master_list.append({u:temp})
		return master_list
	
	def gather(self,champion_html):	
		master_list=[]
		#Gathers name, win rate, games won and games lost of a champion 
		for champion_block in champion_html:
			#Champion Name
			Name=champion_block.find('td',{'class':'ChampionName'})['data-value']
			# Champion Win rate
			winRate=champion_block.find('td',{'class':'RatioGraph'})['data-value']+'%'
			# Champion games 
			games=champion_block.find('td',{'class':'RatioGraph'}).find_all('div',{'class':'Text'})
			try:
				gamesWon=int(games[0].text[:-1])
			except:
				gamesWon=0
			try: 
				gamesLost=int(games[1].text[:-1])
			except:
				gamesLost=0
			print(Name+'\n'+winRate+'\n'+str(gamesWon+gamesLost)+'\n')
			
			temp={'Name':Name,'winRate':winRate,'gamesWon':gamesWon,'gamesLost':gamesLost}
			master_list.append(temp)
		return master_list



# cls to clear console 

#season 10 = 'season-15' ||| season 9 = 'season-13'
#please input list or you will get errors
###UNCOMMENT EXAMPLE BELOW TO SEE HOW THIS WORKS 
#search=Op_search(['Smartster','SgtNutBuster'],['season-13','season-15'])
# search.save()
