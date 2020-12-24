#!/usr/bin/env python3
import requests
import json
import sys
import pprint
import collections
import time

owner = 'teic'
repos = ['tei', 'Stylesheets']
max_pages = 6


def main():
    total_tickets = collections.Counter()
    people_repo_tickets = {}
    request_arguments = {
        'state': 'open',
        'per_page': 100,   # The API returns a maximum of 100 at any time.
        #'page': 1, # We will rewrite this in the loop below
    }
    for this_r in repos:
        this_try = 0
        while this_try <= max_pages:
            this_try += 1
            request_arguments['page'] = this_try
            search_result = requests.get(
                f'https://api.github.com/repos/{owner}/{this_r}/issues',
                params=request_arguments,
                )
            if search_result.status_code != 200:
                print(f'There was an error reading from the repository: {this_r}')
                print(f'{search_result}')
                print(search_result.json())
                break
        
            this_json = search_result.json()
            if not this_json:
                #print('continuing')
                continue
            for this_ticket in this_json:
                total_tickets[this_r] += 1
                for this_person in this_ticket['assignees']:
                    if 'name' in this_person:
                        person = f'{this_person["name"]} - ({this_person["login"]})'
                    elif 'login' in this_person:
                        person = f'{this_person["login"]}'
                    else:
                        continue # Can't read some users for some reason
                        #pprint.pprint(this_person)
                        #raise ValueError
                    if person not in people_repo_tickets:
                        people_repo_tickets[person] = collections.Counter()
                    people_repo_tickets[person][this_r] += 1
            time.sleep(0.2) # Try to avoid being banned!
    
    print('Total open tickets read')
    print('-----------------------')
    for this_r, t in total_tickets.items():
        print(f'{this_r:<20} {t}')
    print()
    print("Tickets currently assigned")
    print("--------------------------")
    print()

    for this_p, this_c in people_repo_tickets.items():
        total = sum(this_c.values())
        details = [] 
        for rep, num in this_c.items(): # can rely on order in later versions of Python 3
            details.append(f'{rep} - {num}')
        details_str = ', '.join(details)
        print(f'{this_p:<25} = {total:3}  ({details_str})')
    

        

if __name__ == '__main__':
    sys.exit(main())
