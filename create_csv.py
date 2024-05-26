"""
template script for writing to a csv file
doc link: https://python-adv-web-apps.readthedocs.io/en/latest/csv.html#:~:text=files%20with%20Python.-,The%20csv%20module%20in%20Python,any%20script%20that%20uses%20it.&text=Note%20that%20using%20methods%20from,open()%20. 
"""
import csv

def run_example():
    # open new file for writing - will erase file if it already exists -
    csvfile = open('example.csv', 'w', newline='', encoding='utf-8')
    # make a new variable - c - for Python's CSV writer object -
    c = csv.writer(csvfile)
    # write a column headings row - do this only once -
    c.writerow( ['name','address','job','age','income'] )
    # call some function that returns a list --
    # for purposes of the template, here is a list of lists -
    the_list = [
        ['Ana', 'Gainesville, Florida', 'chef', 30, 21212.45],
        ['Bob', 'Chicago, Illinois', 'writer', 22, 1233.56],
        ['Ted', 'Miami, Florida', 'driver', 26, 1092.234],
        ['Carol', 'Portland, Oregon', 'executive', 50, 90312.67]
    ]
    # use a for-loop to write each row into the CSV file
    for item in the_list:
        # write one row to csv — item MUST BE a LIST
        c.writerow(item)
    # save and close the file
    csvfile.close()

def create_data_table_csv(data_table):
    # open new file for writing - will erase file if it already exists -
    csvfile = open('data_table.csv', 'w', newline='', encoding='utf-8')
    # make a new variable - c - for Python's CSV writer object -
    c = csv.writer(csvfile)
       # use a for-loop to write each row into the CSV file
    for instance in data_table:
        # write one row to csv — item MUST BE a LIST
        c.writerow(instance)
    # save and close the file
    csvfile.close()

#* Run example script
# run_example()
