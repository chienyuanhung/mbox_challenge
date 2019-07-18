# import the libraries
import re
import numpy as np

# read mbox_full, store in a file 'lines'
file = 'Resources/mbox.full'

with open(file, 'r') as text:
    lines = text.readlines()


# divide file into email sections 
len_lines = len(lines)
e_sections = []
sub_section = []
for i in np.arange((len_lines)):
    sub_section.append(lines[i])
    try:
        if re.findall(r"^From\s",lines[i+1]):
            e_sections.append(sub_section)
            sub_section = []
    except IndexError:
        e_sections.append(sub_section)
        break

# function to get the index of the sentence which fit the pattern
def find_pattern(list, pattern):
    # find the lengt of the list
    len_list = np.arange(len(list))
    # find the index for the sentence that fit the pattern
    for i in len_list:
        if re.findall(pattern,list[i]):
            return i

# find the header section for each email
def find_header(list):
    # length of the list
    l = len(list)
    # header contains "From:", "Date:", "Subject:" and end with "/n" before the main body (if any) 
    # index for "From:", "Date:", "Subject:"
    i = find_pattern(list, r"^From:")
    j = find_pattern(list, r"^Date:")
    k = find_pattern(list, r"^Subject:")
    # find the end of the header
    # the last index for "From:", "Date:", "Subject:"
    m = max([i, j , k]) 
    # number of lines after the last index for the first empty line (\n) to appear
    try:
        n = find_pattern(list[m:l], r"^\n")
        # number of lines after the first empty line for the main body
        p = find_pattern(list[(m+n):l], r"\b")
        return list[0: (m+n+p)]
    # if no main body for the email
    except TypeError: 
        return list[0: (m+n)]

# function for find the footer 
# footer starting one line before the pattern "\d\.\d\.",  such as the string "1.4.0.gg2b" and end at the end of the email
def find_footer(list):
    # length of the list
    l = len(list)
    # the index for the starting length of the footer
    i = find_pattern(list, r"^\d\.\d\.")
    # if no footer pattern found in the email, return empty list
    if i == None:
        return []
    else:
        return list[(i-1):l]

# function to reverse email
def getreverse_mail(list):
    # get header and footer
    header = find_header(list)
    footer = find_footer(list)
    # length of the email
    sec_len = len(list)
    # length of header
    h_len = len(header)
    # length of footer
    f_len = len(footer)
    body_start_index = h_len
    body_end_index = sec_len-f_len
    body = list[body_start_index : body_end_index]
    reverse_body = body[::-1]
    reverse_mail = header + reverse_body + footer
    return reverse_mail

# reverse the email content
reverse_emails = []
for section in e_sections:
    reverse_emails.append(getreverse_mail(section))

# convert reverse_email into i-dimension list
reverse_email_all = []
for i in range(len(reverse_emails)):
    for j in range(len(reverse_emails[i])):
            reverse_email_all.append(reverse_emails[i][j])

# write into reverse_email.txt
file = open("Results/reverse_email.txt", "w") 

for i in reverse_email_all:
    file.write(i)
    
file.close() 

