# Foster Database System

This is a full stack communication and data management tool created from scratch for the North Alabama Foster Closet (NAFC).

## Background:
The foster care system in the United States is ridden with many systematic faults, resulting in problems such as significant high school/college dropout, poverty, and homelessness rates. NAFC is an organization that seeks to support the foster care system by distributing much-needed physical resources to foster families, including clothes, infant care, school supplies, bedding, and more. This significantly reduces the costs of foster care and allows families to focus on other important things like children’s emotional needs and guidance.

NAFC's use of one universal form as a means of communication and records was feasible when the organization was serving few families, but that number has increased significantly. Facing many limitations, the organization sought an online application for more streamlined communication to and from families, tracking requests and service, and collecting data for grants – many times, these local organizations actually fail to obtain large grants due to lack of quality, convincing data about their work. This, overall, would also allow NAFC to devote more time/resources to increase their outreach and take up other large-scale projects. 

I worked with NAFC over multiple years to design and create a web application that fulfills all of the organization's needs.


## Technologies used:
- Django web framework for a Python backend
- HTML, CSS, JavaScript, JQuery, and Django Template Language front end
- PostgreSQL database


## Application sections:
The **accounts** and **adminManagement** modules implement a user and admin account system that creates editable and easy-access profiles for families and children, eliminating the redundancy of filling out the same information repeatedly on the single-form system.

The **irequests** module implements an item request system; the application gives automated alerts when a user submits a new request, generates a request report printout for collecting items, lets both the family and provider monitor the progress/status of a request, and generates messages to be sent to families when items have been collected. 

The **adminManagement** module also provides better data management functionality, such as customizable spreadsheets for viewing and easy editing, and search and filter capabilities.

## Application preview:
### User perspective
Homepage from user point of view:

![](https://i.imgur.com/yHsEbib.png)

**1. ACCOUNT MANAGEMENT**

The user may edit any of their information, including personal info, the type of care they provide, and info about their children. The following shows the page for editing information about the type of care the user provides:

![](https://i.imgur.com/VgB5MaZ.png)

New information can also be added, such as adding a new child into the user's account:

![](https://i.imgur.com/zVHDYel.png)

**2. REQUESTS**

The process for a family to make a request for items has four parts:

A) Verify general family information:

![](https://i.imgur.com/oxggj0K.png)

B) Verify children's information and select the child this request is for:

![](https://i.imgur.com/rjEhXfk.png)

C) Select needed items to request:

![](https://i.imgur.com/KMAKMdn.png)

D) Select preferred method of attaining the items:

![](https://i.imgur.com/OK4h9cX.png)

The user can also view their history of requests, including live status indicators of how much progress NAFC has made for each request:

![](https://i.imgur.com/nVc9C3c.png)



### Admin perspective
Admin accounts have all the options of normal users that were shown above, in addition to management functions. This is the section of the homepage with admin-only capabilities:

![](https://i.imgur.com/fbmo8Gr.png)

**1. ACCOUNT MANAGEMENT**

Admins can view tables/spreadsheets of many data sets in the system, including all users. Clicking column headers sorts the data in that column:

![](https://i.imgur.com/rFFspb7.png)

It's possible to edit this information as necessary. In the above image, simply by clicking on the table cell, the admin is editing the value of the "Remind Update List" column for the user "Ken Bowman," and the "Address" field for the user "George Ferry." There is also an option to view/edit the user's information, as an admin, through the user's homepage perspective:

![](https://i.imgur.com/XxylXQM.png)


**2. REQUESTS**

A) The admin is given a page to view all requests in the system with sorting, filtering, and grouping options:

![](https://i.imgur.com/vi6DkOn.png)

In the image above, the option to "Generate pending requests printout" will export a Word document checklist of requested items along with all relevant family and children information, making it easy for NAFC volunteers to collect items in their warehouse. This printout generation also progresses the live request tracker of the pending requests to "being collected."

B) The admin can then alert the family that their items are ready for pickup through a built-in messaging portal. This step will progress the live tracker of requests under the status of "being collected" to "ready for pickup":

![](https://i.imgur.com/YlLNBIJ.png)

As a backup in the event the email system faces an error, a system-wide notice is sent on each page of the application, and a page is provided for the admin to visit and re-initialize the service GMail account that the system uses.

![](https://i.imgur.com/pS8KLsg.png)

C) The admin can add an entry to the distribution log to maintain a record of the quantities of each item given. This step will set the live tracker of requests under the status of "ready for pickup" to "fulfilled":

![](https://i.imgur.com/1hknSPQ.png)

D) The admin may also edit the fields in the form through which families make requests. The fields can be re-ordered, grouped, linked, and changed in type:

![](https://i.imgur.com/yRaRhnw.png)

**3. LOGS**

Admins may view and edit multiple different data sets or logs on the system, as shown above with the distribution log and set of users. Other logs include the volunteer hours log, donor log, and set of children's data. This is the view of the volunteer hours log:

![](https://i.imgur.com/ohhyRg8.png)

Clicking on cells in the table allows information to be edited.
