from flask import Flask, render_template,request
#from scrape import find_grades
import mechanize
import cookielib
from bs4 import BeautifulSoup,NavigableString
import html2text
import string
import socket
import httplib
import ssl

def find_grades(username,password):

	def connect(self):		#some code to deal with certificate validation
    		sock = socket.create_connection((self.host, self.port),
                                self.timeout, self.source_address)
    		if self._tunnel_host:
    			self.sock = sock
    			self._tunnel()

    		self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)


	httplib.HTTPSConnection.connect = connect
	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent', 'Chrome')]

	# The site we will navigate into, handling it's session
	br.open('https://academics1.iitd.ac.in')


	# Select the second (index one) form (the first form is a search query box)
	br.select_form(nr=0)

	# User credentials
	br.form['username'] = username
	br.form['password'] = password

	# Login
	br.submit()
	soup = BeautifulSoup(str(br.open(br.geturl()).read()),"lxml")
	link=None
	link1=None
	for i in soup.find_all('a'):
		if 'vgrd' in str(i.get('href')):
			link=i.get('href')
			#break
		if 'grade' in str(i.get('href')):
			link1=i.get('href')
			#break
	if (link is None) and (link1 is None):
		return main(True)
		#return "Invalid Login!!"

	def remove_attrs(soup):
	    for tag in soup.findAll(True):
	        tag.attrs = None
	    return soup

	page = open("table.html",'r')
	template = BeautifulSoup(page.read(),"html5lib")

	if not(link1 is None):

		gradesheet=br.open("https://academics1.iitd.ac.in/Academics/"+link1).read()
		#print
	
		# table_tag = soup.find('table')

		soup = BeautifulSoup(gradesheet,"html5lib")
		soup_without_attributes=remove_attrs(soup)
		final_soup =soup_without_attributes.findAll('table')[0].findAll('table')[1].findAll('table')
		for div in final_soup:
			for x in div.find_all():
			    if len(x.text) == 0:
				x.extract()
		print(final_soup)
		limit=len(final_soup)
		for i in range(2,limit):
			##final_soup[i]
			template.div.append(final_soup[i])

	if not(link is None):
		
		gradesheet=br.open("https://academics1.iitd.ac.in/Academics/"+link).read()
		#print
	
		# table_tag = soup.find('table')

		soup = BeautifulSoup(gradesheet,"html5lib")
		soup_without_attributes=remove_attrs(soup)
		final_soup =soup_without_attributes.findAll('table')[0].findAll('table')[1].findAll('table')[2]
		print (final_soup)		
		for x in final_soup.find_all():
		    if len(x.text) == 0:
			x.extract()

		template.div.append(final_soup)

	return str(template)








app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')



@app.route("/")
def main(invalid_password=False):
    if invalid_password:
	error="Login details do not match"
	return render_template('index.html',error=error)
    else:
    	return render_template('index.html')

@app.route("/",methods=['POST'])
def main_form():
	username=request.form['username']
	password=request.form['password']
	return find_grades(username,password)



@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(port=5050)
