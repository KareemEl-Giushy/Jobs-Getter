import requests
from bs4 import BeautifulSoup as bs
import csv
from itertools import zip_longest

titles = []
companies = []
address = []
dates = []
skills = []
links = []
responsibilities = []
requirements = []
PageNumber = 0

job = input("What Job are you looking for? ").strip().lower()
limiter = int(input("Enter How Many Pages To Scan: ").strip())
MakeNewFile = input("Do You Want A New CSV File? Y/n: ").strip().lower()

file_name = "Result"
if MakeNewFile == "yes" or MakeNewFile == "y" or MakeNewFile == "":
    file_name = job
else:
    file_name = "Result"

while True:

    result = requests.get("https://wuzzuf.net/search/jobs/?q={:s}&a=hpb&start={:d}".format(job, PageNumber))

    src = result.content

    soup = bs(src, "lxml")
    # print(soup)

    PageLimit = int(soup.find("strong").text) // 15
    # print(PageLimit)

    job_titles = soup.find_all("h2", {"class":"css-m604qf"})
    company_name = soup.find_all("a", {"class":"css-17s97q8"})
    company_address = soup.find_all("span", {"class":"css-5wys0k"})
    job_posted = soup.select("div.css-1s8r46l div")
    required_skills = soup.find_all("div", {'class': 'css-y4udm8'})
    
    # print(len(job_titles))
    # print(len(job_posted))

    for i in range(len(job_titles)):
        titles.append(job_titles[i].text)
        links.append(job_titles[i].find('a', {'target':'_blank'}).attrs['href'])
        companies.append(company_name[i].text)
        address.append(company_address[i].text)
        dates.append(job_posted[i].text)
        skills.append(required_skills[i].text)
    
    PageNumber += 1
    print(f"Page Switched: {PageNumber}")
    if PageNumber == PageLimit or PageNumber == limiter:
        print("Page Ended Terminate")
        break

i = 0   
for link in links:
    result = requests.get(link)
    soup = bs(result.content, 'html.parser')
    resp = ""
    if soup.find_all(class_="css-ghicub") and soup.find_all(class_="css-ghicub")[0].ul and soup.find_all(class_="css-ghicub")[1].ul and len(soup.find_all(class_="css-ghicub")) >= 2:
        for li in soup.find_all(class_="css-ghicub")[0].ul.find_all("li"):
            resp += li.text + " | "
        responsibilities.append(resp)
        items = ""
        for li in soup.find_all(class_="css-ghicub")[1].ul.find_all("li"):
            items += li.text + " | "
        requirements.append(items)
    else:
        responsibilities.append(None)
        requirements.append(None)
    i += 1
    print(f"Got Job: #{i}")

# print(titles)
# print(companies)
# print(address)
# print(dates)
# print(links)
         
exported = zip_longest(titles, companies, address, dates, skills, responsibilities, requirements,links)

# print(list(exported))

with open(r"D:\Projects\Jobs" + f"\\{file_name}.csv", "w", newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Company", "Address", "Posted In", "Required Skills", "Responsibilities", "Requirements", "Links"])
    writer.writerows(exported)